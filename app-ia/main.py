# -*- coding: utf-8 -*-
from app import app
from flask import jsonify, request, Response, send_from_directory
from typing import Optional, Dict, Any
from utils import get_embedding, cosine_distance, euclidean_distance
from datetime import datetime
import os
import mysql.connector
import shutil

# API port
port: int = 8911

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict() -> Response:
    rut: Optional[str] = request.form.get('rut')
    uploaded_image = request.files.get('imagen')

    if uploaded_image is None:
        return jsonify({
            "status": "error",
            "message": "No image received",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        })

    # Read database
    # Simulate database connection
    conn = mysql.connector.connect(
    host="localhost",
    user="grupo3",
    password="piagrupo3",
    database="ucampus_db"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, path_foto FROM ucampus WHERE rut = %s", (rut,))
    result = cursor.fetchone()

    # 0. If RUT is not found in the database, comparison cannot be done
    if result is None:
        return jsonify({
            "status": "error",
            "message": "Rut no encontrado",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        })

    name: str = result['nombre']
    image_path: str = result['path_foto']

    """return jsonify({
            "status": "error",
            "message": "fuerza leon",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
    })"""

    # Save the uploaded image to a location
    filename_uploaded = f"uploaded_{rut}_{datetime.now().timestamp()}.jpeg"
    path_uploaded = os.path.join('DB_UCampus', 'uploads', filename_uploaded)
    os.makedirs(os.path.dirname(path_uploaded), exist_ok=True)
    uploaded_image.save(path_uploaded)

    carpeta_destino = os.path.join('..', 'app-front', 'static', 'img')
    nombre_foto = os.path.basename(image_path)
    full_image_path = os.path.join(image_path)

    destino = os.path.join(carpeta_destino, nombre_foto)

    shutil.copy(full_image_path, destino)

    uploaded_url_path = filename_uploaded.replace('\\', '/')
    db_url_path = image_path.replace('DB_UCampus/', '').replace('\\', '/')

    # Perform prediction with VGGFace2 embeddings
    with open(path_uploaded, 'rb') as f:
        uploaded_bytes = f.read()
    embedding_uploaded = get_embedding(uploaded_bytes)

    # 0.1 If no face detected in the uploaded image, cannot compare
    if embedding_uploaded is None:
        return jsonify({
            "status": "error",
            "message": "Rostro no detectado, acerquese a la cámara",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            },
            "images": {
                "uploaded_url": f"/static/uploads/{uploaded_url_path}",
                "db_url": f"/static/{db_url_path}"
            }
        })

    # Get embedding from the database image
    full_image_path = os.path.join(image_path)
    with open(full_image_path, 'rb') as f:
        db_bytes = f.read()
    embedding_db = get_embedding(db_bytes)

    cosine_dist = cosine_distance(embedding_uploaded, embedding_db)
    euclidean_dist = euclidean_distance(embedding_uploaded, embedding_db)

    # Return JSON response with comparison result, RUT, and name
    # 1. If cosine distance <= 0.5, consider the same person (access granted)
    # 2. If cosine distance > 0.5, consider different people (access denied)


    db_url_img = f"../app-front/static/img/{nombre_foto}"
    response = {
        "status": "success" if cosine_dist <= 0.5 else "error",
        "message": "Acceso permitido" if cosine_dist <= 0.5 else "Acceso denegado",
        "data": {
            "rut": rut,
            "nombre": name,
            "distancia_coseno": cosine_dist,
            "distancia_euclidiana": euclidean_dist
        },
        "images": {
            "uploaded_url": f"/static/uploads/{uploaded_url_path}",
            "db_url":  f"../app-front/static/img/{nombre_foto}",
	    "hola": "hola"
        }
    }

    return jsonify(response)

#@app.route('/static/<path:filename>')
#def serve_static(filename) -> Response:
#   
#    Serve static files from the DB_UCampus directory.
#    
#    return send_from_directory('DB_UCampus', filename)
#
if __name__ == '__main__':
    app.run(port=port, debug=True)
