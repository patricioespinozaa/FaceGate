

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
    # Casos: 
    
    # 0. Si no se encuentra el RUT en la base de datos, se considera que no se puede realizar la comparación
    rut = None
    if rut is None:
        json_respuesta = {
            "status": "error",
            "message": "Rut no encontrado",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        }

    # 1. Si la distancia es menor a 0.5, se considera que son la misma persona
    rut = 123456789
    rut = str(rut)
    nombre = "Juan Pérez"
    distancia_coseno = 0.3
    distancia_euclidiana = 0.4
    if distancia_coseno < 0.5:
        json_respuesta = {
            "status": "success",
            "message": "Acceso permitido",
            "data": {
                "rut": rut,
                "nombre": nombre,
                "distancia_coseno": distancia_coseno,
                "distancia_euclidiana": distancia_euclidiana
            }
        }

    # 2. Si la distancia es mayor a 0.5, se considera que son personas distintas
    rut = 123456789
    rut = str(rut)
    nombre = "Juan Pérez"
    distancia_coseno = 0.6
    distancia_euclidiana = 0.7
    if distancia_coseno > 0.5:
        json_respuesta = {
            "status": "error",
            "message": "Acceso denegado",
            "data": {
                "rut": rut,
                "nombre": nombre,
                "distancia_coseno": distancia_coseno,
                "distancia_euclidiana": distancia_euclidiana
            }
        }

    # 3. Si no se detecta rostro en la imagen subida, se considera que no se puede realizar la comparación
    detectar_rostro = False
    if not detectar_rostro:
        json_respuesta = {
            "status": "error",
            "message": "Rostro no detectado, acerquese a la cámara",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        }
    return jsonify(json_respuesta)



if __name__ == "__main__":
    app.run(port=8902)     # Considerar el puerto para backend