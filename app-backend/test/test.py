from pathlib import Path
from facenet_pytorch import InceptionResnetV1
import torch
import os
import sys

# Funciones auxiliares
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import get_embedding, cosine_distance, euclidean_distance

# Rutas de imágenes
img1_path = 'test/src/20918356-0.jpg'
img2_path = 'test/src/Foto_Patricio.jpg'

# Leer imágenes como bytes
img1_bytes = Path(img1_path).read_bytes()
img2_bytes = Path(img2_path).read_bytes()

# Modelo preentrenado
model = InceptionResnetV1(pretrained='vggface2').eval()

try:
    # Obtener embeddings
    emb1 = get_embedding(img1_bytes, model)
    emb2 = get_embedding(img2_bytes, model)

    # Calcular distancias
    cos_dist = cosine_distance(emb1, emb2)
    euc_dist = euclidean_distance(emb1, emb2)

    # Mostrar resultados
    print(f'Distancia coseno:     {cos_dist:.4f}')
    print(f'Distancia euclidiana: {euc_dist:.4f}')

    # Interpretación
    if cos_dist < 0.5:
        print("✅ Mismo rostro (coseno)")
    else:
        print("❌ Rostros distintos (coseno)")

    if euc_dist < 1.0:
        print("✅ Mismo rostro (euclidiana)")
    else:
        print("❌ Rostros distintos (euclidiana)")

except ValueError as e:
    print(e)
