import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
from PIL import Image
from torchvision.transforms import ToPILImage
import torch
from models.face_model import model, mtcnn
from services.database import insert_user_embeddings
from typing import Optional, Dict, Any

import json


def get_embedding(image_bytes: bytes, save_path: Optional[str] = None) -> Optional[torch.Tensor]:
    """
    Extract the face embedding from image bytes.

    Args:
        image_bytes (bytes): Image data in bytes.
        save_path (Optional[str]): Optional path to save the cropped face image.

    Returns:
        Optional[torch.Tensor]: The embedding tensor if a face is detected, else None.
    """
    # Read and convert image to RGB
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Detect face
    face = mtcnn(image)
    if face is None:
        return None

    # Optionally save the detected face image
    if save_path is not None:
        pil_face = ToPILImage()(face)  # Convert tensor to PIL image
        pil_face.save(save_path)       # Save to specified path

    # Prepare face tensor for model
    face = face.unsqueeze(0)

    # Get embedding without gradient calculation
    with torch.no_grad():
        embedding = model(face)

    return embedding.squeeze(0)

def update_embeddings_in_db():
    """
    Recorre la carpeta `../../data/ucampus/`, interpreta cada archivo como una imagen 
    nombrada con el RUT (sin extensión), genera el embedding y lo guarda en la base de datos 
    en formato JSON bajo la columna `embeddings`.
    """
    base_path = os.path.join('..', '..', 'data', 'ucampus')
    image_files = [f for f in os.listdir(base_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"🔍 Encontradas {len(image_files)} imágenes en {base_path}")

    for filename in image_files:
        rut, _ = os.path.splitext(filename)  
        image_path = os.path.join(base_path, filename)
        print(f"🔄 Procesando imagen: {filename} (RUT: {rut})")

        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        embedding = get_embedding(image_bytes)

        if embedding is None:
            print(f"🚫 No se detectó rostro en la imagen de {rut}")
            continue

        embedding_json = json.dumps({"db": embedding.tolist()})

        try:
            insert_user_embeddings(rut, embedding_json)
            print(f"✅ Embeddings actualizados para {rut}")
        except Exception as e:
            print(f"❌ Error al insertar embeddings para {rut}: {e}")

    print("✅ Proceso de actualización completado.")



if __name__ == "__main__":
    """
    Al ejecutar el script en el servidor con 
    'python embeddings.py', se actualizarán los embeddings 'db' de la base de datos
    para cada entidad
    """
    #update_embeddings_in_db()
