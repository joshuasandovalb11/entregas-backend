# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .. import schemas, models, security, database

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    """
    Endpoint de login:
    - Recibe 'username' y 'password'
    - Valida credenciales
    - Retorna token JWT si son correctas
    """

    statement = select(models.Driver).where(models.Driver.username == form_data.username)
    result = db.exec(statement)
    driver = result.first()

    if not driver or not security.verify_password(form_data.password, driver.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        data={"sub": str(driver.driver_id)}
    )

    return {"access_token": access_token, "token_type": "bearer"}
