

# -*- coding: utf-8 -*-
from app import app
from utils import get_prediction
from flask import Flask, jsonify, request
import time

AUTH_SECRET = "piagrupo3"

@app.route('/facegate/app-ia/predict', methods=['POST']) # Cambiado
def predict():
    # Obtener RUT
    
    # Extraer imagen de la DB de acuerdo al RUT
    # Extraer nombre de la DB de acuerdo al RUT

    # Obtener la fotografia subida al frontend

    # Realizar la predicción de ambas imagenes con VGGFace2

    # Comparar los embeddings obtenidos de ambas imagenes con distancia coseno y euclidiana

    # Si la distancia es menor a 0.5, se considera que son la misma persona
    # Si la distancia es mayor a 0.5, se considera que son personas distintas

    # Entregar una respuesta JSON al frontend con el resultado de la comparación, indicando el RUT y nombre de la persona.


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
    app.run(port=8902)     # Considerar el puerto para backend