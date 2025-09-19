# app/routers/fec.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import utils
from .. import schemas, models, security, database, services

router = APIRouter(
    prefix="/fec",
    tags=["FEC"],
    dependencies=[Depends(security.get_current_driver)]
)

@router.get("/{fec_number}", response_model=schemas.FEC)
def get_fec_details(fec_number: int, db: Session = Depends(database.get_db), current_driver: models.Driver = Depends(security.get_current_driver)):
    """
    Obtiene los detalles completos de un FEC (la ruta del día).
    Llama a la capa de servicio para ejecutar la lógica de negocio.
    """
    try:
        fec = services.get_fec_details_for_driver(db, fec_number=fec_number, driver_id=current_driver.driver_id)
        return fec
    except HTTPException as e:
        raise e

@router.patch("/{fec_id}/route", response_model=schemas.FEC, status_code=status.HTTP_200_OK)
def update_fec_route(
    fec_id: int,
    route_data: schemas.OptimizedRouteData,
    db: Session = Depends(database.get_db),
    current_driver: models.Driver = Depends(security.get_current_driver)
):
    # --- AÑADIR ESTAS LÍNEAS PARA DEPURACIÓN ---
    print(f"--- Recibida petición para actualizar ruta del FEC ID: {fec_id} ---")
    print(f"--- Datos recibidos: {route_data.model_dump_json(indent=2)} ---")
    # ---------------------------------------------
    try:
        updated_fec = services.update_fec_route_details(
            db=db,
            fec_id=fec_id,
            route_data=route_data,
            driver_id=current_driver.driver_id
        )

        return utils.fec_model_to_schema(updated_fec)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al actualizar la ruta del FEC: {e}"
        )