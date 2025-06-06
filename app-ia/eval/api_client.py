# api_client.py
import requests
from dotenv import load_dotenv
import os

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import API_URL

print(f"API URL: {API_URL}")

def send_image_to_api(image_path: str, claimed_rut: str) -> dict | None:
    """Envía una imagen y un RUT a la API y retorna la respuesta como JSON."""
    try:
        with open(image_path, "rb") as img_file:
            files = {"imagen": img_file}
            data = {"rut": claimed_rut}
            response = requests.post(API_URL, files=files, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"❌ API error for '{image_path}' with RUT '{claimed_rut}': {e}")
        return None
