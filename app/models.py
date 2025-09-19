# app/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime

class Driver(SQLModel, table=True):
    __tablename__ = "drivers"

    driver_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=100, unique=True)
    hashed_password: str = Field(max_length=255)
    num_unity: Optional[str] = Field(default=None, max_length=50)
    vehicle_plate: Optional[str] = Field(default=None, max_length=20)
    phone_number: Optional[str] = Field(default=None, max_length=20)

    deliveries: List["Delivery"] = Relationship(back_populates="driver")
    fecs: List["FEC"] = Relationship(back_populates="driver")
    tracking_points: List["TrackingPoint"] = Relationship(back_populates="driver")

class Salesperson(SQLModel, table=True):
    __tablename__ = "salespersons"

    salesperson_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20)

    clients: List["Client"] = Relationship(back_populates="salesperson")

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    phone: Optional[str] = Field(default=None, max_length=20)
    gps_location: Optional[str] = Field(default=None, max_length=100)
    salesperson_id: Optional[int] = Field(default=None, foreign_key="salespersons.salesperson_id")

    salesperson: Optional["Salesperson"] = Relationship(back_populates="clients")
    deliveries: List["Delivery"] = Relationship(back_populates="client")

class FEC(SQLModel, table=True):
    __tablename__ = "fecs"

    fec_id: Optional[int] = Field(default=None, primary_key=True)
    fec_number: int = Field(index=True)
    fec_date: date = Field(default_factory=date.today)
    status: str = Field(default="active", max_length=50)

    driver_id: Optional[int] = Field(default=None, foreign_key="drivers.driver_id")
    optimized_order_list_json: Optional[str] = None
    suggested_journey_polyline: Optional[str] = None

    deliveries: List["Delivery"] = Relationship(back_populates="fec")
    driver: Optional["Driver"] = Relationship(back_populates="fecs")

class Delivery(SQLModel, table=True):
    __tablename__ = "deliveries"

    # --- IDs y Relaciones ---
    delivery_id: Optional[int] = Field(default=None, primary_key=True)
    fec_id: Optional[int] = Field(default=None, foreign_key="fecs.fec_id")
    driver_id: Optional[int] = Field(default=None, foreign_key="drivers.driver_id")
    client_id: Optional[int] = Field(default=None, foreign_key="clients.client_id")
    invoice_id: Optional[str] = Field(default=None, max_length=100, index=True)

    # --- Estado y Prioridad ---
    status: str = Field(default="pending", max_length=50)
    priority: Optional[int] = None

    # --- Tiempos y Duraciones ---
    # Guardamos los tiempos como DateTime para poder hacer cálculos precisos
    start_time: datetime = Field(default_factory=datetime.utcnow)
    delivery_time: datetime = None
    accepted_next_at: datetime = None
    
    # Estos son campos que se podrían calcular, pero los almacenaremos
    # por flexibilidad y rendimiento.
    actual_duration: Optional[str] = Field(default=None, max_length=50)
    estimated_duration: Optional[str] = Field(default=None, max_length=50)

    # --- Coordenadas y Distancia ---
    start_latitud: float
    start_longitud: float
    end_latitud: Optional[float] = None
    end_longitud: Optional[float] = None
    distance: Optional[float] = None

    # --- Campos de Incidencia ---
    cancellation_reason: Optional[str] = Field(default=None, max_length=255)
    cancellation_notes: Optional[str] = Field(default=None, max_length=1000)

    # --- Vínculos de SQLAlchemy para una navegación fácil en el código ---
    fec: Optional["FEC"] = Relationship(back_populates="deliveries")
    driver: Optional["Driver"] = Relationship(back_populates="deliveries")
    client: Optional["Client"] = Relationship(back_populates="deliveries")
    tracking_points: List["TrackingPoint"] = Relationship(back_populates="delivery")

class TrackingPoint(SQLModel, table=True):
    __tablename__ = "tracking_points"
    
    point_id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    event_type: Optional[str] = Field(default=None, max_length=50)

    driver_id: Optional[int] = Field(default=None, foreign_key="drivers.driver_id")
    delivery_id: Optional[int] = Field(default=None, foreign_key="deliveries.delivery_id")

    driver: Optional["Driver"] = Relationship(back_populates="tracking_points")
    delivery: Optional["Delivery"] = Relationship(back_populates="tracking_points")