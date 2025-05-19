# -*- coding: utf-8 -*-
from app import app
from flask import jsonify, request, Response
import pandas as pd
from typing import Optional, Dict, Any
from utils import get_embedding, cosine_distance, euclidean_distance
import os

# API port
port: int = 8902  # Needs to be changed

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict() -> Response:
    """
    Process a face recognition prediction request.

    Returns:
        Response: JSON response with prediction results or error messages.
    """
    # Get RUT from the form
    rut: Optional[str] = request.form.get('rut')

    # Get the image sent from the frontend
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

    # Simulate database connection
    df = pd.read_csv('DB_UCampus/DB_local.csv')

    # Find row matching the provided RUT
    student = df[df['Rut'] == rut]
    name: Optional[str] = student['Nombre'].values[0] if not student.empty else None
    image_path: Optional[str] = student['path'].values[0] if not student.empty else None

    # 0. If RUT is not found in the database, comparison cannot be done
    if name is None or image_path is None:
        json_response: Dict[str, Any] = {
            "status": "error",
            "message": "Rut no encontrado",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        }
        return jsonify(json_response)

    # Perform prediction with VGGFace2 embeddings

    # Get embedding from the uploaded image
    uploaded_image_bytes: bytes = uploaded_image.read()
    embedding_uploaded_image = get_embedding(uploaded_image_bytes)

    # 0.1 If no face detected in the uploaded image, cannot compare
    if embedding_uploaded_image is None:
        json_response = {
            "status": "error",
            "message": "Rostro no detectado, acerquese a la cámara",
            "data": {
                "rut": None,
                "nombre": None,
                "distancia_coseno": None,
                "distancia_euclidiana": None
            }
        }
        return jsonify(json_response)

    # Get embedding from the database image
    image_path = os.path.join('DB_UCampus', image_path)
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    embedding_db_image = get_embedding(image_bytes)

    # Compare embeddings using cosine and euclidean distances
    cosine_dist = cosine_distance(embedding_uploaded_image, embedding_db_image)
    euclidean_dist = euclidean_distance(embedding_uploaded_image, embedding_db_image)

    # Return JSON response with comparison result, RUT, and name
    # 1. If cosine distance <= 0.5, consider the same person (access granted)
    if cosine_dist <= 0.5:
        json_response = {
            "status": "success",
            "message": "Acceso permitido",
            "data": {
                "rut": rut,
                "nombre": name,
                "distancia_coseno": cosine_dist,
                "distancia_euclidiana": euclidean_dist
            }
        }
        return jsonify(json_response)

    # 2. If cosine distance > 0.5, consider different people (access denied)
    if cosine_dist > 0.5:
        json_response = {
            "status": "error",
            "message": "Acceso denegado",
            "data": {
                "rut": rut,
                "nombre": name,
                "distancia_coseno": cosine_dist,
                "distancia_euclidiana": euclidean_dist
            }
        }
    return jsonify(json_response)


if __name__ == "__main__":
    app.run(port=port)