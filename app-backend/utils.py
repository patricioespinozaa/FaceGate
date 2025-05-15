# -*- coding: utf-8 -*-
import io
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision import models
from facenet_pytorch import InceptionResnetV1  # o usa otro modelo de VGGFace2 si ya lo tienes

# Preprocesamiento: mismo tamaño que VGGFace espera
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((160, 160)),  # InceptionResnetV1 espera 160x160
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return transform(image).unsqueeze(0)  # Batch size = 1

# Obtener embeddings desde la imagen
def get_embedding(image_bytes, model):
    tensor = transform_image(image_bytes)
    with torch.no_grad():
        embedding = model(tensor)
    return embedding.squeeze(0)  # (512,)
    
# Medidas de distancia
def cosine_distance(a, b):
    return 1 - F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def euclidean_distance(a, b):
    return torch.norm(a - b).item()