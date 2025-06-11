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

def delete_uploaded_imagen(path_uploaded):
    """
    Elimina la imagen una vez que se obtienen los embeddings.

    Args:
        name_image: Nombre de imagen guardada en uploads.

    path_uploaded, filename_uploaded = save_uploaded_image(uploaded_image, rut)
    """
    os.remove(path_uploaded)
    print("Imagen removida")
