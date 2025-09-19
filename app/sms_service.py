# app/sms_service.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SMSMASIVOS_API_KEY = os.getenv("SMS_API_KEY")
API_URL = "https://api.smsmasivos.com.mx/sms/send"

def send_completion_sms(salesperson_phone: str, client_id: int, invoice_id: str):
    """
    Envía un SMS al vendedor notificando la finalización de una entrega
    usando la API de SMSMASIVOS.
    """
    if not SMSMASIVOS_API_KEY:
        print("ADVERTENCIA: Falta la variable SMS_API_KEY en el archivo .env. No se enviarán SMS.")
        return False

    try:
        completion_time = datetime.utcnow()
        formatted_time = completion_time.strftime("%I:%M %p")
        message = (
            f"Entrega Completada\n"
            f"Cliente: {client_id}\n" 
            f"Factura: {invoice_id}\n"
            f"Hora: {formatted_time} (UTC)"
        )

        headers = {
            'apikey': SMSMASIVOS_API_KEY
        }
        
        payload = {
            'message': message,
            'numbers': salesperson_phone,
            'country_code': '52',
            'sandbox': '1'
        }

        print(f"Enviando SMS de prueba a {salesperson_phone}...")
        
        response = requests.post(url=API_URL, headers=headers, data=payload)
        
        response.raise_for_status()
        
        response_data = response.json()
        
        if response_data.get("success") is True:
            print(f"ÉXITO: La API de SMSMASIVOS aceptó el mensaje. Respuesta: {response_data}")
            return True
        else:
            print(f"ERROR: La API de SMSMASIVOS devolvió un error. Respuesta: {response_data}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Falló la conexión con la API de SMSMASIVOS. Razón: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Ocurrió un error inesperado al enviar el SMS. Razón: {e}")
        return False