from config.settings import DB_CREDENTIALS
import mysql.connector
from typing import Optional, Dict, Any

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
