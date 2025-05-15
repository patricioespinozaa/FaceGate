# -*- coding: utf-8 -*-
from flask import Flask
from facenet_pytorch import InceptionResnetV1

app = Flask(__name__)

# Cargar modelo VGGFace2 (ej. InceptionResnetV1 preentrenado)
model = InceptionResnetV1(pretrained='vggface2').eval()
