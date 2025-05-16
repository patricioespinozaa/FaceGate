# -*- coding: utf-8 -*-
import io
from PIL import Image
import torch
import torch.nn.functional as F
from facenet_pytorch import InceptionResnetV1, MTCNN
from torchvision import transforms
from app import model

# Inicializar el detector de rostros MTCNN
mtcnn = MTCNN(image_size=160, margin=0)

# Obtener embeddings desde la imagen 
def get_embedding(image_bytes):
    # Detección del rostro
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    face = mtcnn(image)
    if face is None:
        return None
    face = face.unsqueeze(0)  
    with torch.no_grad():
        embedding = model(face)
    return embedding.squeeze(0)

# Medidas de distancia
def cosine_distance(a, b):
    return 1 - F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def euclidean_distance(a, b):
    return torch.norm(a - b).item()