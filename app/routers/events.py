# app/routers/events.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from .. import schemas, models, security, database, services

router = APIRouter(
    prefix="/deliveries", # Agruparemos todo bajo /deliveries
    tags=["Deliveries & Events"],
    dependencies=[Depends(security.get_current_driver)] # ¡Todos estos endpoints están protegidos!
)

@router.post("/events/log", status_code=status.HTTP_202_ACCEPTED)
def log_tracking_events(
    events: List[schemas.TrackingPoint], 
    db: Session = Depends(database.get_db), 
    current_driver: models.Driver = Depends(security.get_current_driver)
):
    """
    Recibe y registra una lista de eventos de tracking (GPS, inicio/fin de entrega).
    """
    try:
        services.log_tracking_events_for_driver(db, events=events, driver_id=current_driver.driver_id)
        return {"status": "ok", "message": "Eventos recibidos para procesamiento."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al procesar los eventos."
        )

@router.post("/{delivery_id}/incident", response_model=schemas.Delivery)
def report_incident(
    delivery_id: int,
    incident_data: schemas.IncidentReport,
    db: Session = Depends(database.get_db),
    current_driver: models.Driver = Depends(security.get_current_driver)
):
    """
    Reporta una incidencia para una entrega específica.
    """
    try:
        updated_delivery = services.create_incident_report(
            db,
            delivery_id=delivery_id,
            incident_data=incident_data,
            driver_id=current_driver.driver_id
        )
        return updated_delivery
    except HTTPException as e:
        # Re-lanzamos las excepciones HTTP que vienen del service (ej. 404)
        raise e
    except Exception as e:
        # Capturamos cualquier otro error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al reportar la incidencia."
        )