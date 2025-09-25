# app/services.py

import logging
from sqlmodel import Session
from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status

from app import models
from . import repositories, schemas, sms_service, whatsapp_service, utils

logger = logging.getLogger(__name__)


def log_tracking_events_for_driver(db: Session, events: List[schemas.TrackingPoint], driver_id: int):
    """
    Procesa una lista de eventos de tracking de forma resiliente.
    Guarda cada punto de GPS y maneja los errores de lógica de negocio de forma individual,
    sin revertir todo el lote de datos.
    """
    affected_fec_ids = set()

    for event in events:
        try:
            # Logica anti-duplicados
            if event.deliveryId and event.eventType in ["start_delivery", "end_delivery"]:
                
                if repositories.check_if_event_exists(db, delivery_id=event.deliveryId, event_type=event.eventType):
                    
                    logger.warning(f"Evento duplicado ignorado: {event.eventType} para delivery_id {event.deliveryId}")
                    continue
            
            repositories.create_tracking_point(db, point=event, driver_id=driver_id)

            if event.deliveryId:
                delivery = repositories.get_delivery_by_id(db, delivery_id=event.deliveryId, driver_id=driver_id)
                if delivery:
                    if delivery.fec_id:
                        affected_fec_ids.add(delivery.fec_id)
                    
                    location_data = schemas.Location(latitude=event.latitude, longitude=event.longitude)

                    if event.eventType == "start_delivery":
                        repositories.update_delivery_status(
                            db,
                            delivery=delivery,
                            new_status="in_progress",
                            timestamp=event.timestamp,
                            location=location_data,
                            estimated_duration=event.estimatedDuration,
                            estimated_distance=event.estimatedDistance,
                        )
                    elif event.eventType == "end_delivery":
                        repositories.update_delivery_status(db, delivery=delivery, new_status="completed", timestamp=event.timestamp, location=location_data)
                        
                        if (delivery.client and
                            delivery.client.salesperson and
                            delivery.client.salesperson.phone and
                            delivery.invoice_id):
                            
                            # whatsapp_service.send_completion_whatsapp(
                            #     salesperson_phone=delivery.client.salesperson.phone,
                            #     client_id=delivery.client.client_id,
                            #     invoice_id=delivery.invoice_id,
                            #     client_name=delivery.client.name
                            # )
                            sms_service.send_completion_sms(
                                salesperson_phone=delivery.client.salesperson.phone,
                                client_id=delivery.client.client_id,
                                invoice_id=delivery.invoice_id,
                            )
                        else:
                            logger.warning(f"ADVERTENCIA: Faltan datos del vendedor para la entrega {delivery.delivery_id}. No se envió WhatsApp.")

        except Exception as e:
            logger.error(f"Error procesando la lógica para el evento {event}. Error: {e}", exc_info=True)

    if affected_fec_ids:
        for fec_id in affected_fec_ids:
            try:
                fec_to_check = db.get(models.FEC, fec_id)
                if fec_to_check and fec_to_check.status != "completed":
                    all_deliveries = repositories.get_all_deliveries_for_fec(db, fec_id=fec_id)
                    is_fec_completed = all(d.status in ["completed", "cancelled"] for d in all_deliveries)
                    if is_fec_completed:
                        logger.info(f"Todas las entregas del FEC {fec_id} están completas. Actualizando estado.")
                        repositories.update_fec_status(db, fec=fec_to_check, new_status="completed")
            except Exception as e:
                logger.error(f"Error al verificar el estado final del FEC {fec_id}. Error: {e}", exc_info=True)

    try:
        db.commit()
    except Exception as e:
        logger.critical("FALLO CRÍTICO al intentar hacer commit a la base de datos. Se hará rollback.", exc_info=True)
        db.rollback()
        raise e

def create_incident_report(db: Session, delivery_id: int, incident_data: schemas.IncidentReport, driver_id: int):
    """Gestiona la lógica de negocio para reportar una incidencia."""
    delivery = repositories.get_delivery_by_id(db, delivery_id=delivery_id, driver_id=driver_id)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La entrega no fue encontrada o no pertenece a este conductor."
        )
    
    if delivery.status in ["completed", "cancelled"]:
        logger.warning(f"Se intentó reportar una incidencia sobre una entrega ya finalizada (ID: {delivery_id}, Estado: {delivery.status})")
        return delivery
    
    end_delivery_event = schemas.TrackingPoint(
        latitude=incident_data.latitude,
        longitude=incident_data.longitude,
        timestamp=datetime.now(timezone.utc),
        eventType="end_delivery",
        deliveryId=delivery_id
    )
    repositories.create_tracking_point(db, point=end_delivery_event, driver_id=driver_id)
    logger.info(f"Evento 'end_delivery' creado para la incidencia de la entrega ID: {delivery_id}")

    try:
        current_timestamp = datetime.now(timezone.utc)
        location_data = None
        if incident_data.latitude is not None and incident_data.longitude is not None:
            location_data = schemas.Location(latitude=incident_data.latitude, longitude=incident_data.longitude)

        updated_delivery_model = repositories.report_incident_for_delivery(
            db,
            delivery=delivery, 
            incident=incident_data,
            timestamp=current_timestamp,
            location=location_data
        )

        db.commit()
        db.refresh(updated_delivery_model)
        return utils.delivery_model_to_schema(updated_delivery_model)
    except Exception as e:
        db.rollback()
        raise e
    
def get_fec_details_for_driver(db: Session, fec_number: int, driver_id: int):
    """
    Orquesta la obtención y enriquecimiento de los detalles de un FEC para un conductor.
    """
    fec = repositories.get_fec_by_number_and_driver(db, fec_number=fec_number, driver_id=driver_id)
    
    if not fec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El FEC con número '{fec_number}' no fue encontrado para este conductor."
        )

    if fec.status == "pending":
        repositories.update_fec_status(db, fec, "in_progress")
        db.commit()
        db.refresh(fec)
        logger.info(f"El FEC ID: {fec.fec_id} ha sido actualizado a 'in_progress'.")
    
    if fec.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"El FEC {fec_number} ya fue completado y no puede ser iniciado de nuevo."
        )

    if repositories.are_all_deliveries_finalized(db, fec.fec_id):
        repositories.update_fec_status(db, fec, "completed")
        db.commit()
        db.refresh(fec)
        logger.info(f"El FEC ID: {fec.fec_id} ha sido actualizado a 'completed'.")
        
    # needs_commit = False
    # for delivery in fec.deliveries:
    #     if (delivery.start_latitud is None or delivery.start_latitud == 0) and delivery.client and delivery.client.gps_location:
            
    #         coords = utils.parse_gps_location(delivery.client.gps_location)
            
    #         if coords:
    #             delivery.start_latitud, delivery.start_longitud = coords
    #             db.add(delivery)
    #             needs_commit = True
    #             logger.info(f"Coordenadas actualizadas para la entrega ID: {delivery.delivery_id}")

    # if needs_commit:
    #     db.commit()
    #     db.refresh(fec)
        
    return utils.fec_model_to_schema(fec)

def update_fec_route_details(db: Session, fec_id: int, route_data: schemas.OptimizedRouteData, driver_id: int):
    """Servicio para actualizar la ruta optimizada de un FEC."""
    fec = db.get(models.FEC, fec_id)
    if not fec or fec.driver_id != driver_id:
        raise HTTPException(status_code=404, detail="FEC no encontrado o no pertenece al conductor.")
    
    repositories.update_fec_route(
        db, 
        fec=fec, 
        optimized_order_list_json=route_data.optimized_order_list_json, 
        polyline=route_data.suggested_journey_polyline
    )
    db.commit()
    db.refresh(fec)
    
    return fec