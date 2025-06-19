from config.settings import DB_CREDENTIALS
import mysql.connector
from typing import Optional, Dict, Any
import datetime

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
    cursor.execute("""
        SELECT 
            status,
            uploaded_image_path,
            db_image_path,
            timestamp,
            notes
        FROM audit_log
        WHERE rut = %s AND timestamp >= NOW() - INTERVAL 5 SECOND
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