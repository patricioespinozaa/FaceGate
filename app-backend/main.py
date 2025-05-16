# -*- coding: utf-8 -*-
from app import app
from flask import Flask, jsonify, request
import pandas as pd
import time

from utils import get_embedding, cosine_distance, euclidean_distance
import os

<<<<<<< HEAD
@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict():
    # Obtener RUT desde el formulario
    rut = request.form.get('rut')

    # Obtener imagen enviada desde el frontend
    uploaded_image = request.files.get('imagen')
    
    # Simulación de conexión a la base de datos
    
    df = pd.read_csv('DB_UCampus/DB.csv')
    # Obtener fila con el RUT proporcionado
    # estudiante debe abordar el caso en que no se encuentra el RUT en la base de datos
    estudiante = df[df['RUT'] == rut] 
    nombre = estudiante['Nombre'].values[0] if not estudiante.empty else None
    image_path = estudiante['Path'].values[0] if not estudiante.empty else None
    
    # 0. Si no se encuentra el RUT en la base de datos, se considera que no se puede realizar la comparación
    if nombre is None or image_path is None:
=======
@app.route('/facegate/app-ia/predict', methods=['POST']) # Cambiado
def predict():
    # Simulación de conexión a la base de datos
    # db = connect_to_database()
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
>>>>>>> origin/backend_main
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
<<<<<<< HEAD
        return jsonify(json_respuesta)

    # Realizar la predicción de ambas imagenes con VGGFace2
    
    # Obtener el embedding de la imagen subida
    uploaded_image_bytes = uploaded_image.read()
    embedding_uploaded_image = get_embedding(uploaded_image_bytes)

    # 0.1 Si no se detecta rostro en la imagen subida, se considera que no se puede realizar la comparación
    if embedding_uploaded_image is None:
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
    
    # Obtener el embedding de la imagen de la base de datos
    image_path = os.path.join('DB_UCampus', image_path)
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    embedding_db_image = get_embedding(image_bytes)

    # Comparar los embeddings obtenidos de ambas imagenes con distancia euclidiana
    distancia_coseno = cosine_distance(embedding_uploaded_image, embedding_db_image)
    distancia_euclidiana = euclidean_distance(embedding_uploaded_image, embedding_db_image)

    # Entregar una respuesta JSON al frontend con el resultado de la comparación, indicando el RUT y nombre de la persona.
    # 1. Si la distancia es menor a 0.5, se considera que son la misma persona
    if distancia_euclidiana < 0.5:
=======

    # 1. Si la distancia es menor a 0.5, se considera que son la misma persona
    rut = 123456789
    rut = str(rut)
    nombre = "Juan Pérez"
    distancia_coseno = 0.3
    distancia_euclidiana = 0.4
    if distancia_coseno < 0.5:
>>>>>>> origin/backend_main
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
<<<<<<< HEAD
    if distancia_euclidiana > 0.5:
=======
    rut = 123456789
    rut = str(rut)
    nombre = "Juan Pérez"
    distancia_coseno = 0.6
    distancia_euclidiana = 0.7
    if distancia_coseno > 0.5:
>>>>>>> origin/backend_main
        json_respuesta = {
            "status": "error",
            "message": "Acceso denegado",
            "data": {
                "rut": rut,
                "nombre": nombre,
                "distancia_coseno": distancia_coseno,
                "distancia_euclidiana": distancia_euclidiana
            }
<<<<<<< HEAD
=======
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
>>>>>>> origin/backend_main
        }
    return jsonify(json_respuesta)



if __name__ == "__main__":
<<<<<<< HEAD
    app.run(port=8902)     # Este puerto ya lo estamos usando, hay que cambiarlo
=======
    app.run(port=8902)     # Considerar el puerto para backend
>>>>>>> origin/backend_main
