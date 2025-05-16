# -*- coding: utf-8 -*-
import io
from PIL import Image
import torch
import torch.nn.functional as F
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms

# Inicializar el detector de rostros MTCNN (una sola vez)
mtcnn = MTCNN(image_size=160, margin=0)

# Obtener embeddings desde la imagen (con detección de rostro)
def get_embedding(image_bytes, model):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    face = mtcnn(image)
    if face is None:
        raise ValueError("❌ No se detectó ninguna cara en la imagen.")
    face = face.unsqueeze(0)  # Agregar dimensión de batch
    with torch.no_grad():
        embedding = model(face)
    return embedding.squeeze(0)  # (512,)

# Medidas de distancia
def cosine_distance(a, b):
    return 1 - F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def euclidean_distance(a, b):
    return torch.norm(a - b).item()

print("Ejecutado utils.py")