# -*- coding: utf-8 -*- 
from flask import Flask

app = Flask(__name__,
            static_url_path='/facegate/app-front/static',
            static_folder='static',
            template_folder='templates')
