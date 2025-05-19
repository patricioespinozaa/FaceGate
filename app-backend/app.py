# -*- coding: utf-8 -*-
import json
from typing import Optional, Dict, Any
from flask import Flask

app: Flask = Flask(__name__)

# Load the InceptionResnetV1 model pretrained with VGGFace2
from facenet_pytorch import InceptionResnetV1

model: InceptionResnetV1 = InceptionResnetV1(pretrained='vggface2').eval()

# Labels or additional classes for face recognition
FILENAME_FACE_CLASSES: str = 'face_class_index.json'

face_class_index: Optional[Dict[str, Any]] = None

try:
    with open(FILENAME_FACE_CLASSES) as f:
        face_class_index = json.load(f)
except FileNotFoundError:
    face_class_index = None