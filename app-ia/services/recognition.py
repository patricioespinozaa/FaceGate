import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.database import get_user_by_rut, log_attempt

from services.database import get_user_embeddings
from services.database import update_recent_embeddings_json
from services.database import should_update_embeddings
from services.database import insert_user_embeddings

from models.embeddings import get_embedding
from models.distances import cosine_distance, euclidean_distance, tensor_to_list_dict
from utils.file_ops import save_uploaded_image, copy_db_image_to_frontend, update_recientes, delete_uploaded_imagen, save_uploaded_image_to_frontend
from flask import jsonify, current_app
from PIL import Image
import io
import glob
import json

THRESHOLD = 0.50
#  systemctl --user restart server_app-ia

def process_request(uploaded_image, rut: str):
    """
    Procesa una solicitud de reconocimiento facial comparando una imagen subida con 
    la imagen registrada en la base de datos correspondiente al RUT entregado.

    Args:
        uploaded_image (Any): Imagen enviada por el usuario a través del formulario.
        rut (str): RUT utilizado para buscar en la base de datos.

    Returns:
        flask.Response: Respuesta JSON con el estado de la verificación facial, 
        nombre del usuario, distancias de comparación (coseno y euclidiana), y 
        rutas relativas de las imágenes usadas.
    
    Flujo:
    - Recupera al usuario desde la base de datos por su RUT.
    - Guarda la imagen subida y copia la imagen del usuario al frontend.
    - Calcula embeddings de ambas imágenes usando el modelo facial.
    - Calcula distancia coseno y euclidiana entre embeddings.
    - Devuelve una respuesta con el resultado de la verificación.
    """
    
    user = get_user_by_rut(rut)
    path_uploaded, filename_uploaded = save_uploaded_image_to_frontend(uploaded_image, rut)

    if not user:
        attempt_id = log_attempt(rut,
                                 'error',
                                 uploaded_image_path=f"uploads/{filename_uploaded}",
                                 notes="Rut no encontrado")
        return jsonify({
            "status": "error",
            "attempt_id": attempt_id,
            "message": "Rut no encontrado",
            "images": {
                "uploaded_url": f"/facegate/app-front/static/uploads/{filename_uploaded}",
                "db_url": "/facegate/app-front/static/img/plain.png"
            }

        })

    uploaded_image.seek(0)
    img_data = uploaded_image.read()

    img = Image.open(io.BytesIO(img_data))

    MAX_SIZE = 300

    width, height = img.size
    if max(width, height) > MAX_SIZE:
        ratio = MAX_SIZE / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=90)
    optimized_bytes = img_buffer.getvalue()

    embedding_uploaded = get_embedding(optimized_bytes)

    name, image_path, folder_path = user['nombre'], user['path_foto'], user['path_carpeta_recientes']

    nombre_foto = copy_db_image_to_frontend(image_path) # Borrar?

    if embedding_uploaded is None:
        attempt_id = log_attempt(
            rut, 'error',
            uploaded_image_path=f"uploads/{filename_uploaded}",
            db_image_path=nombre_foto,
            notes="Rostro no detectado"
        )
        #delete_uploaded_imagen(path_uploaded)
        return jsonify({
            "status": "error",
            "attempt_id": attempt_id,
            "message": "Acceso denegado",
            "data": {
                "rut": rut,
                "nombre": name
                },
            "images": {
                "uploaded_url": f"/facegate/app-front/static/uploads/{filename_uploaded}",
                "db_url": f"/facegate/app-front/static/img/{nombre_foto}"
            }
        })

    # Obtener las embeddings de la db
    embeddings_json = get_user_embeddings(rut)

    # Embedding imagen Ucampus
    embedding_ucampus = embeddings_json['db']
    euclidean_dist = euclidean_distance(embedding_uploaded, embedding_ucampus)
    cosine_dist = cosine_distance(embedding_uploaded, embedding_ucampus)

    # Filtrar key 'db'
    embeddings_recientes = [
        emb for key, emb in embeddings_json.items() if key != 'db'
    ]

    # Calculamos las distancias para la carpeta recientes 
    recientes_cos_dist =  [
        cosine_distance(embedding_uploaded, emb)
        for emb in embeddings_recientes
    ]
    
    # Promedio de las recientes
    prom_cos_recientes = sum(recientes_cos_dist) / len(recientes_cos_dist) if recientes_cos_dist else 0
    
    # Ponderacion dando mas peso a ucampus
    peso_db = 0.7
    peso_recientes = 0.3
    dist_pond = peso_db * cosine_dist + peso_recientes * prom_cos_recientes

    if dist_pond <= THRESHOLD - 0.05:
        update_recientes(path_uploaded,rut)

    # cambiar distancia coseno -> base métricas
    if dist_pond <= THRESHOLD:
        status = 'success'
        attempt_id = log_attempt(
            rut, status,
            cosine_distance=cosine_dist,
            euclidean_distance=euclidean_dist,
            uploaded_image_path=f"uploads/{filename_uploaded}",
            db_image_path=nombre_foto,
            notes=f"Ponderada: {dist_pond:.4f}"
        )

        # Actualización del embedding para las imagenes recientes
        # Verificacion del día (no actualizar si ya se actualizó hoy)
        if should_update_embeddings(embeddings_json):
            updated_embeddings_json = update_recent_embeddings_json(embeddings_json, embedding_uploaded)
            # Guardar el JSON actualizado en la base de datos
            insert_user_embeddings(rut, json.dumps(tensor_to_list_dict(updated_embeddings_json)))
    else:
        status = 'error'
        attempt_id = log_attempt(
        rut, status,
        cosine_distance=cosine_dist,
        euclidean_distance=euclidean_dist,
        uploaded_image_path=f"uploads/{filename_uploaded}",
        db_image_path=nombre_foto,
        notes="Verificación fallida"
    )
        
    # en todos los casos borramos
    #delete_uploaded_imagen(path_uploaded) 

    return jsonify({
        "status": "success" if dist_pond <= THRESHOLD else "error",
        "attempt_id": attempt_id,
        "message": "Acceso permitido" if dist_pond <= THRESHOLD else "Acceso denegado",
        "data": {
            "rut": rut,
            "nombre": name,
            "distancia_coseno_ponderada": dist_pond,
            "distancia_coseno_db": cosine_dist,
            "distancia_coseno_reciente": recientes_cos_dist,
            "distancia_euclidiana": euclidean_dist,
        },
        "images": {
            "uploaded_url": f"/facegate/app-front/static/uploads/{filename_uploaded}",
            "db_url": f"/facegate/app-front/static/img/{nombre_foto}"
        }
    })