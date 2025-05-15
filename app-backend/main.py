

# -*- coding: utf-8 -*-
from app import app
from utils import get_prediction
from flask import Flask, jsonify, request
import time

AUTH_SECRET = "piagrupo3"

@app.route('/ejercicio4/app1-ia/predict', methods=['POST'])
def predict():
    token = requests.headers.get("X-Auth-Token")
    if token == AUTH_SECRET:
        file = request.files['file']
        img_bytes = file.read()
        start_time = time.time()
        resultados = get_prediction(image_bytes=img_bytes)
        duration = f"{time.time() - start_time:.4f}"
        json_respuesta = {
                'resultados': resultados,
                'tiempo': duration
        }
        print("responder: {}".format(json_respuesta))
    return jsonify(json_respuesta)



if __name__ == "__main__":
    app.run(port=8902)