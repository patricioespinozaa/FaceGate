# -*- coding: utf-8 -*-
import json
from torchvision import models
from flask import Flask

app = Flask(__name__)
model = models.resnet50(weights='IMAGENET1K_V2')
model.eval()

FILENAME_IMAGENET_CLASSES = 'imagenet_class_index.json'

imagenet_class_index = json.load(open(FILENAME_IMAGENET_CLASSES))