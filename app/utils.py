# app/utils.py

from . import models, schemas
from datetime import datetime
import json
from typing import List, Optional, Tuple

def parse_gps_location(gps_string: Optional[str]) -> Optional[Tuple[float, float]]:
    """
    Convierte un string de coordenadas 'lat,lng' en una tupla de floats.
    Devuelve None si el string es inválido.
    """
    if not gps_string:
        return None
    try:
        parts = gps_string.split(',')
        if len(parts) != 2:
            return None
        lat = float(parts[0].strip())
        lng = float(parts[1].strip())
        return lat, lng
    except (ValueError, IndexError):
        return None

def fec_model_to_schema(fec_model: models.FEC) -> schemas.FEC:
    """
    Convierte un modelo FEC de la base de datos a un schema compatible con React Native.
    Maneja las diferencias de nomenclatura y parsea el JSON de la ruta optimizada.
    """
    date_str = fec_model.fec_date.isoformat() if fec_model.fec_date else ""
    
    deliveries = []
    if fec_model.deliveries:
        for delivery in fec_model.deliveries:
            deliveries.append(delivery_model_to_schema(delivery))
            
    optimized_order_id_list = []
    if fec_model.optimized_order_list_json:
        try:
            parsed_list = json.loads(fec_model.optimized_order_list_json)
            if isinstance(parsed_list, list) and all(isinstance(i, int) for i in parsed_list):
                optimized_order_id_list = parsed_list
        except (json.JSONDecodeError, TypeError):
            print(f"ADVERTENCIA: No se pudo parsear optimized_order_list_json: {fec_model.optimized_order_list_json}")
            optimized_order_id_list = []


    return schemas.FEC(
        fec_id=fec_model.fec_id,
        fec_number=fec_model.fec_number,
        driver_id=fec_model.driver_id,
        fec_date=fec_model.fec_date,
        deliveries=deliveries,
        status=fec_model.status,
        optimized_order_list_json=fec_model.optimized_order_list_json,
        suggested_journey_polyline=fec_model.suggested_journey_polyline,
        optimizedOrderId_list=optimized_order_id_list 
    )

def delivery_model_to_schema(delivery_model: models.Delivery) -> schemas.Delivery:
    """
    Convierte un modelo Delivery de la base de datos a un schema compatible con React Native.
    """
    client_schema = None
    if delivery_model.client:
        salesperson_schema = None
        if delivery_model.client.salesperson:
            salesperson_schema = schemas.Salesperson(
                name=delivery_model.client.salesperson.name,
                phone=delivery_model.client.salesperson.phone or ""
            )
        
        client_schema = schemas.Client(
            client_id=delivery_model.client.client_id,
            name=delivery_model.client.name,
            phone=delivery_model.client.phone,
            gps_location=delivery_model.client.gps_location or "",
            salesperson=salesperson_schema
        )
    
    return schemas.Delivery(
        delivery_id=delivery_model.delivery_id,
        driver_id=delivery_model.driver_id,
        client_id=delivery_model.client_id,
        start_time=delivery_model.start_time,
        delivery_time=delivery_model.delivery_time.isoformat() if delivery_model.delivery_time else None,
        actual_duration=delivery_model.actual_duration,
        estimated_duration=delivery_model.estimated_duration,
        estimated_distance=delivery_model.estimated_distance,
        start_latitude=delivery_model.start_latitude,
        start_longitude=delivery_model.start_longitude,
        end_latitude=delivery_model.end_latitude,
        end_longitude=delivery_model.end_longitude,
        invoice_id=delivery_model.invoice_id,
        client=client_schema,
        status=delivery_model.status,
        distance=delivery_model.distance,
        priority=delivery_model.priority,
        cancellation_reason=delivery_model.cancellation_reason,
        cancellation_notes=delivery_model.cancellation_notes
    )