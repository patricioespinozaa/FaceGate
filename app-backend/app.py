# -*- coding: utf-8 -*-
import json
from flask import Flask
from facenet_pytorch import InceptionResnetV1

app = Flask(__name__)

# Cargar modelo InceptionResnetV1 preentrenado con VGGFace2
model = InceptionResnetV1(pretrained='vggface2').eval()

# Si tienes etiquetas o datos adicionales, cárgalos aquí
FILENAME_FACE_CLASSES = 'face_class_index.json'  

try:
    face_class_index = json.load(open(FILENAME_FACE_CLASSES))
except FileNotFoundError:
    face_class_index = None
