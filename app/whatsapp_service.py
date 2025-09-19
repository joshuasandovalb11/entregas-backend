# app/whatsapp_service.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SMSMASIVOS_API_KEY = os.getenv("SMSMASIVOS_API_KEY")
WHATSAPP_INSTANCE_ID = os.getenv("WHATSAPP_INSTANCE_ID")
API_URL = "https://api.smsmasivos.com.mx/whatsapp/send"

def send_completion_whatsapp(salesperson_phone: str, client_id: int, invoice_id: str, client_name: str):
    """
    Envía una notificación por WhatsApp al vendedor cuando se completa una entrega.
    """
    if not SMSMASIVOS_API_KEY or not WHATSAPP_INSTANCE_ID:
        print("ADVERTENCIA: Faltan las variables SMSMASIVOS_API_KEY o WHATSAPP_INSTANCE_ID en el .env.")
        print("No se enviarán notificaciones de WhatsApp.")
        return False

    try:
        completion_time = datetime.now()
        formatted_time = completion_time.strftime("%I:%M %p")

        message = (
            f"✅ *Pedido Entregado*\n\n"
            f"🔢 *Cliente #:* {client_id}\n"
            f"👤 *Nombre:* {client_name}\n"
            f"🧾 *Factura #:* {invoice_id}\n"
            f"🕒 *Hora:* {formatted_time}"
        )

        headers = {
            'apikey': SMSMASIVOS_API_KEY
        }
        
        payload = {
            'instance_id': WHATSAPP_INSTANCE_ID,
            'type': 'text',
            'number': salesperson_phone,
            'country_code': '52',
            'message': message,
        }

        print(f"Enviando notificación de WhatsApp a {salesperson_phone}...")
        
        response = requests.post(url=API_URL, headers=headers, data=payload)
        response.raise_for_status()
        
        response_data = response.json()
        
        if response_data.get("success") is True:
            print(f"ÉXITO: WhatsApp enviado a {salesperson_phone}. Respuesta: {response_data}")
            return True
        else:
            print(f"ERROR: La API de WhatsApp devolvió un error. Respuesta: {response_data}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Falló la conexión con la API de SMSMASIVOS. Razón: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Ocurrió un error inesperado al enviar el WhatsApp. Razón: {e}")
        return False