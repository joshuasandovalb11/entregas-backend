# app/repositories.py

from typing import List
from sqlmodel import Session, func, select
from . import models, schemas
import datetime
from math import atan2, cos, radians, sin, sqrt

def check_if_event_exists(db: Session, delivery_id: int, event_type: str) -> bool:
    """
    Verifica si ya existe un evento específico ('start_delivery' o 'end_delivery')
    para una entrega. Devuelve True si ya existe, False si no.
    """
    statement = select(models.TrackingPoint).where(
        models.TrackingPoint.delivery_id == delivery_id,
        models.TrackingPoint.event_type == event_type
    )
    existing_event = db.exec(statement).first()
    return existing_event is not None

def create_tracking_point(db: Session, point: schemas.TrackingPoint, driver_id: int):
    """Guarda un nuevo punto de GPS en la tabla 'tracking_points'."""
    db_point = models.TrackingPoint(
        latitude=point.latitude,
        longitude=point.longitude,
        timestamp=point.timestamp,
        event_type=point.eventType,
        driver_id=driver_id,
        delivery_id=point.deliveryId
    )
    db.add(db_point)
    return db_point

def get_delivery_by_id(db: Session, delivery_id: int, driver_id: int) -> models.Delivery | None:
    """Busca una entrega por su ID, asegurándose de que pertenezca al conductor correcto."""
    statement = select(models.Delivery).where(
        models.Delivery.delivery_id == delivery_id,
        models.Delivery.driver_id == driver_id
    )
    return db.exec(statement).first()

def calculate_total_distance(db: Session, delivery_id: int) -> float:
    """Calcula la distancia total recorrida para una entrega sumando la distancia entre sus tracking points."""
    points = db.exec(
        select(models.TrackingPoint)
        .where(models.TrackingPoint.delivery_id == delivery_id)
        .order_by(models.TrackingPoint.timestamp)
    ).all()

    if len(points) < 2:
        return 0.0

    total_distance = 0.0
    R = 6371.0

    for i in range(len(points) - 1):
        lat1, lon1 = radians(points[i].latitude), radians(points[i].longitude)
        lat2, lon2 = radians(points[i+1].latitude), radians(points[i+1].longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        total_distance += distance

    return round(total_distance, 2)

def _finalize_delivery_details(
    db: Session,
    delivery: models.Delivery,
    timestamp: datetime,
    location: schemas.Location | None = None,
):
    """Función auxiliar para rellenar los detalles finales de una entrega."""
    delivery.delivery_time = timestamp
    if location:
        delivery.end_latitude = location.latitude
        delivery.end_longitude = location.longitude

    if delivery.start_time:
        duration_seconds = (
            timestamp.replace(tzinfo=None) - delivery.start_time.replace(tzinfo=None)
        ).total_seconds()
        delivery.actual_duration = str(int(duration_seconds))

    delivery.distance = calculate_total_distance(db, delivery.delivery_id)

def update_delivery_status(
    db: Session, 
    delivery: models.Delivery, 
    new_status: str, 
    timestamp: datetime,
    location: schemas.Location = None,
    estimated_duration: str | None = None,
    estimated_distance: str | None = None,
):
    delivery.status = new_status
    if new_status == "in_progress":
        delivery.start_time = timestamp
        if location:
            delivery.start_latitude = location.latitude
            delivery.start_longitude = location.longitude
        if estimated_duration:
            delivery.estimated_duration = estimated_duration
        if estimated_distance:
            delivery.estimated_distance = estimated_distance

    elif new_status == "completed":
        _finalize_delivery_details(db, delivery, timestamp, location)

    db.add(delivery)
    return delivery

def update_fec_route(db: Session, fec: models.FEC, optimized_order_list_json: str, polyline: str):
    """Guarda la ruta optimizada y la polilínea en el FEC."""
    fec.optimized_order_list_json = optimized_order_list_json
    fec.suggested_journey_polyline = polyline
    db.add(fec)
    
def get_all_deliveries_for_fec(db: Session, fec_id: int) -> List[models.Delivery]:
    """Obtiene todas las entregas asociadas a un FEC."""
    statement = select(models.Delivery).where(models.Delivery.fec_id == fec_id)
    return db.exec(statement).all()

def update_fec_status(db: Session, fec: models.FEC, new_status: str):
    """Actualiza el estado de un FEC."""
    fec.status = new_status
    db.add(fec)

def report_incident_for_delivery(
    db: Session, 
    delivery: models.Delivery, 
    incident: schemas.IncidentReport, 
    timestamp: datetime,
    location: schemas.Location = None
) -> models.Delivery:
    """Actualiza una entrega con datos de incidencia, incluyendo timestamps, ubicación y distancia."""
    delivery.status = "cancelled"
    delivery.cancellation_reason = incident.reason
    delivery.cancellation_notes = incident.notes
    
    _finalize_delivery_details(db, delivery, timestamp, location)

    db.add(delivery)
    return delivery

def get_fec_by_number_and_driver(db: Session, fec_number: int, driver_id: int) -> models.FEC | None:
    """Busca un FEC por su número y el ID del conductor."""
    statement = select(models.FEC).where(
        models.FEC.fec_number == fec_number,
        models.FEC.driver_id == driver_id
    )
    return db.exec(statement).first()

def are_all_deliveries_finalized(db: Session, fec_id: int) -> bool:
    """
    Verifica si todas las entregas de un FEC tienen un estado final (completed o cancelled).
    Cuenta las entregas que todavía están pendientes o en progreso.
    """
    statement = select(func.count(models.Delivery.delivery_id)).where(
        models.Delivery.fec_id == fec_id,
        models.Delivery.status.in_(["pending", "in_progress"])
    )
    pending_deliveries_count = db.exec(statement).one()
    
    return pending_deliveries_count == 0

def update_delivery_acceptance_time(db: Session, delivery: models.Delivery, timestamp: datetime):
    """
    Actualiza el campo accepted_next_at de una entrega.
    Solo lo actualiza si no ha sido establecido previamente para evitar sobrescrituras.
    """
    if delivery.accepted_next_at is None:
        delivery.accepted_next_at = timestamp
        db.add(delivery)
    return delivery