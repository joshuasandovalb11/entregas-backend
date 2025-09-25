# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Estructura DRIVER
class Driver(BaseModel):
    driver_id: int
    username: str
    num_unity: str
    vehicle_plate: str
    phone_number: str

    class Config:
        from_attributes = True

# Estructura SalesPerson
class Salesperson(BaseModel):
    name: str
    phone: str

# Estructura CLIENT
class Client(BaseModel):
    client_id: int
    name: str
    phone: Optional[str] = None 
    gps_location: str
    salesperson: Optional[Salesperson] = None

# Estructura DELIVERY - CORREGIDA
class Delivery(BaseModel):
    delivery_id: int
    driver_id: int
    client_id: int
    start_time: datetime
    delivery_time: Optional[str] = None
    actual_duration: Optional[str] = None
    estimated_duration: Optional[str] = None
    estimated_distance: Optional[str] = None
    start_latitude: float
    start_longitude: float
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    invoice_id: Optional[str] = None
    client: Optional[Client] = None
    status: Optional[str] = None # "pending", "in_progress", etc.
    distance: Optional[float] = None
    priority: Optional[int] = None
    cancellation_reason: Optional[str] = None
    cancellation_notes: Optional[str] = None

    class Config:
        from_attributes = True

# Estructura FEC
class FEC(BaseModel):
    fec_id: int
    fec_number: int
    driver_id: int
    fec_date: datetime
    deliveries: List[Delivery] = []
    status: str
    optimized_order_list_json: Optional[str] = None
    suggested_journey_polyline: Optional[str] = None
    optimized_order_id_list: Optional[List[int]] = Field(default=None, alias="optimizedOrderId_list")
    suggested_journey_polyline: Optional[str] = Field(default=None, alias="suggestedJourneyPolyline")

    class Config:
        from_attributes = True
        populate_by_name = True

# Estructura TRACKINGPOINT
class TrackingPoint(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime
    eventType: str
    deliveryId: Optional[int] = None
    estimatedDuration: Optional[str] = None
    estimatedDistance: Optional[str] = None

# Estructura LOCATION
class Location(BaseModel):
    latitude: float
    longitude: float

# Estructura AUTHSTATE
class LoginRequest(BaseModel):
    username: str
    password: str

# Schema para la respuesta del login
class Token(BaseModel):
    access_token: str
    token_type: str

# Estructura IncidentReport
class IncidentReport(BaseModel):
    reason: str
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class OptimizedRouteData(BaseModel):
    optimized_order_list_json: str
    suggested_journey_polyline: str