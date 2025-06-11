# -*- coding: utf-8 -*-
import json
import os
from typing import Optional, Dict, Any
from flask import Flask
from flask_cors import CORS

#app: Flask = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'DB_UCampus')
app: Flask = Flask(__name__, static_url_path='/static', static_folder=db_path)
CORS(app, resources={r"/facegate/*": {"origins": "http://localhost:8910"}})