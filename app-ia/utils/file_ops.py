import os
import shutil
from datetime import datetime

from datetime import datetime
import os
import shutil

def save_uploaded_image(uploaded_image, rut: str) -> tuple[str, str]:
    """
    Guarda una imagen subida por el usuario en el directorio local `DB_UCampus/uploads/`.

    Args:
        uploaded_image: Objeto de imagen recibido (por ejemplo, desde Flask).
        rut (str): RUT del usuario, usado para generar un nombre único de archivo.

    Returns:
        tuple[str, str]: Una tupla con:
            - La ruta completa donde se guardó la imagen.
            - El nombre del archivo guardado.
    """
    filename = f"uploaded_{rut}_{datetime.now().timestamp()}.jpeg"
    path = os.path.join('DB_UCampus', 'uploads', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    uploaded_image.save(path)
    return path, filename


def copy_db_image_to_frontend(image_path: str) -> str:
    """
    Copia una imagen existente (de la base de datos) al directorio de imágenes del frontend.

    Args:
        image_path (str): Ruta original de la imagen a copiar.

    Returns:
        str: Nombre del archivo copiado (sin ruta), útil para construir rutas de acceso en el frontend.
    """
    carpeta_destino = os.path.join('..', 'app-front', 'static', 'img')
    os.makedirs(carpeta_destino, exist_ok=True)
    nombre_foto = os.path.basename(image_path)
    destino = os.path.join(carpeta_destino, nombre_foto)
    if not os.path.exists(destino):
        shutil.copy(image_path, destino)
    return nombre_foto

def delete_uploaded_imagen(path_uploaded: str):
    """
    Elimina la imagen una vez que se obtienen los embeddings.

    Args:
        path_upload: Nombre de imagen guardada en uploads.
    """
    os.remove(path_uploaded)
    print("Imagen removida")

def update_recientes(path_reciente, rut: str):
    """
    Se actualiza la carpeta recientes de la entidad correspondiente.

    Args:
        path_reciente: Nombre de la carpeta reciente de la entidad correspondiente.
    """
    carpeta_recientes = os.path.join('..', 'data', 'recientes', rut)
    archivos = [f for f in os.listdir(carpeta_recientes) if os.path.isfile(os.path.join(carpeta_recientes, f))]
    
    if len(archivos) < 5:
        shutil.copy(path_reciente, carpeta_recientes)
    else:
        #aquí falta ver cada cuanto tiempo se aceptará una nueva foto
        archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta_recientes, x)))
        os.remove(os.path.join(carpeta_recientes, archivos[0]))
        shutil.copy(path_reciente, carpeta_recientes)
