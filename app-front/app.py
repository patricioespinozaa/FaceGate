# -*- coding: utf-8 -*- 
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__,
            static_url_path='/facegate/app-front/static',
            static_folder='static',
            template_folder='templates')

socketio = SocketIO(app, cors_allowed_origins="*")
