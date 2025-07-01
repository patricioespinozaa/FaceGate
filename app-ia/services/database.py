import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import DB_CREDENTIALS
import mysql.connector
from typing import Optional, Dict, Any
from datetime import datetime
import time 

def get_user_by_rut(rut: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves user information from the database by RUT.

    Args:
        rut (str): The RUT (unique identifier) of the user to search for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the user's name and photo path if found,
                                  otherwise None.
    """
    conn = mysql.connector.connect(**DB_CREDENTIALS)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, path_foto, path_carpeta_recientes FROM ucampus WHERE rut = %s", (rut,))
    result = cursor.fetchone()
    return result

def get_result_by_rut(rut: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene el último resultado de verificación para un RUT desde la tabla audit_log.

    Args:
        rut (str): El RUT (identificador único) del usuario.

    Returns:
        Optional[Dict[str, Any]]: Un diccionario que contiene el estado de la verificación,
                                  las rutas de la imagen capturada y la imagen de referencia,
                                  y la fecha/hora del intento si existe.
                                  Si no hay registro, retorna un estado 'pending'.
    """
    
    conn = mysql.connector.connect(**DB_CREDENTIALS)
    cursor = conn.cursor(dictionary=True)
    time.sleep(1)
    cursor.execute("""
        SELECT 
            status,
            uploaded_image_path,
            db_image_path,
            timestamp,
            notes
        FROM audit_log
        WHERE rut = %s 
        ORDER BY timestamp DESC
        LIMIT 1
    """, (rut,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return {
            "status": result['status'],
            "uploaded_image_url": f"/facegate/app-front/static/{result['uploaded_image_path']}",
            "db_image_url": f"/facegate/app-front/static/img/{result['db_image_path']}",
            "timestamp": str(result['timestamp']),
            "notes": str(result['notes'])
        }
    else:
        return {"status": "pending"}

def log_attempt(rut, status, cosine_distance=None, euclidean_distance=None,
                uploaded_image_path=None, db_image_path=None, notes=None) -> int:
    conn = mysql.connector.connect(**DB_CREDENTIALS)
    cursor = conn.cursor()

    sql = """
    INSERT INTO audit_log 
    (rut, status, cosine_distance, euclidean_distance, uploaded_image_path, db_image_path, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        rut, status, cosine_distance, euclidean_distance,
        uploaded_image_path, db_image_path, notes
    ))
    conn.commit()
    attempt_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return attempt_id

def insert_user_embeddings(rut: str, embeddings: str) -> None:
    """
    Inserts or updates user embeddings in the database.

    Args:
        rut (str): The RUT (unique identifier) of the user.
        embeddings (str): The embeddings data to be stored as a string.
    """
    conn = mysql.connector.connect(**DB_CREDENTIALS)
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute("SELECT COUNT(*) FROM ucampus WHERE rut = %s", (rut,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        # Update existing user's embeddings
        cursor.execute("UPDATE ucampus SET embeddings = %s WHERE rut = %s", (embeddings, rut))
    else:
        # Insert new user with embeddings
        cursor.execute("INSERT INTO ucampus (rut, embeddings) VALUES (%s, %s)", (rut, embeddings))

    conn.commit()
    cursor.close()
    conn.close()

import json
from typing import Optional, Dict, Any
import mysql.connector

def get_user_embeddings(rut: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves user embeddings from the database by RUT, and returns them as a parsed dictionary.

    Args:
        rut (str): The RUT (unique identifier) of the user to search for.

    Returns:
        Optional[Dict[str, Any]]: The parsed embeddings JSON as a Python dictionary if found,
                                  otherwise None.
    """
    conn = mysql.connector.connect(**DB_CREDENTIALS)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT embeddings FROM ucampus WHERE rut = %s", (rut,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result['embeddings']:
        try:
            parsed_json = json.loads(result['embeddings'])
            return parsed_json
        except json.JSONDecodeError:
            print(f"❌ Error al decodificar el JSON de embeddings del RUT {rut}")
            return None

    return None


def update_recent_embeddings_json(embeddings_json: Dict[str, Any], new_embedding: list[float]) -> Dict[str, Any]:
    """
    Actualiza el diccionario de embeddings eliminando la fecha más antigua
    (exceptuando la key 'db') y añadiendo una nueva entrada con la fecha actual
    en formato 'dd/mm/yyyy'.

    Args:
        embeddings_json (Dict[str, Any]): Diccionario de embeddings actuales.
        new_embedding (list[float]): Embedding nuevo a insertar.

    Returns:
        Dict[str, Any]: Diccionario de embeddings actualizado.
    """
    # Filtrar claves que son fechas (excluye 'db')
    fecha_keys = [k for k in embeddings_json if k != "db"]

    # Convertir las claves al formato datetime para ordenarlas
    fechas_ordenadas = sorted(fecha_keys, key=lambda k: datetime.strptime(k, "%d/%m/%Y"))

    # Si hay 5 o más fechas, eliminar la más antigua
    if len(fechas_ordenadas) >= 5:
        key_to_remove = fechas_ordenadas[0]
        embeddings_json.pop(key_to_remove)

    # Agregar nueva fecha como clave en formato 'dd/mm/yyyy'
    nueva_fecha = datetime.now().strftime("%d/%m/%Y")
    embeddings_json[nueva_fecha] = new_embedding

    return embeddings_json

def should_update_embeddings(embeddings_json: Dict[str, Any]) -> bool:
    """
    Verifica si el diccionario de embeddings tiene menos de 5 entradas.
    Si la fecha actual coincide con la fecha más reciente, no se actualiza. -> False
    Si la fecha actual no coincide, se actualiza el más reciente -> True

    Args:
        embeddings_json (Dict[str, Any]): Diccionario de embeddings actuales.

    Returns:
        bool: True si hay menos de 5 entradas, False en caso contrario.
    """
    # Filtrar claves que son fechas (excluye 'db')
    fecha_keys = [k for k in embeddings_json if k != "db"]

    # Si hay menos de 5 fechas, se debe actualizar
    if len(fecha_keys) < 5:
        return True

    # Obtener la fecha más reciente
    fechas_ordenadas = sorted(fecha_keys, key=lambda k: datetime.strptime(k, "%d/%m/%Y"))
    fecha_mas_reciente = fechas_ordenadas[-1]

    # Verificar si la fecha actual coincide con la más reciente
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    return fecha_actual != fecha_mas_reciente

import json
if __name__ == "__main__":
    # Ejemplo de uso
    rut = "20918356-0"
    
    # Obtener embeddings para un usuario
    user_embeddings = get_user_embeddings(rut)

    print(f"Cantidad de llaves: {len(user_embeddings)}")
    print(f"Keys: {list(user_embeddings.keys())}")

    print(f"DB Embedding: {user_embeddings['db'][0:5]}")
    
    # Probar actualización de embeddings
    new_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]  
    updated_embeddings = update_recent_embeddings_json(user_embeddings, new_embedding)
    print(f"Updated Embeddings: {json.dumps(updated_embeddings, indent=2)}")
    insert_user_embeddings(rut, json.dumps(updated_embeddings))

    # Verificar actualizacion
    user_embeddings = get_user_embeddings(rut)
    print(f"Cantidad de llaves después de actualización: {len(user_embeddings)}")
    print(f"Keys después de actualización: {list(user_embeddings.keys())}")
    print(f"DB Embedding después de actualización: {user_embeddings['db'][0:5]}")
