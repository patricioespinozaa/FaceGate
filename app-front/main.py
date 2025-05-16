# -*- coding: utf-8 -*-
import os
import json
from app import app
from flask import request, redirect, url_for, render_template, jsonify


@app.route('/Facegate/')
def index_form():
    return render_template('index.html')

@app.route('/Facegate/send_rut', methods=['POST'])
def receive_rut():
    data = request.get_json()
    rut = data.get('rut', '')
    print(f'Received RUT: {rut}')
    return jsonify({'message': f'RUT {rut} received successfully'})

if __name__ == "__main__":
    app.run(port=8001)
