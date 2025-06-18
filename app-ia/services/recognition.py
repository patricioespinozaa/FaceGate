import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.database import get_user_by_rut, log_attempt
from models.embeddings import get_embedding
from models.distances import cosine_distance, euclidean_distance
from utils.file_ops import save_uploaded_image, copy_db_image_to_frontend, update_recientes, delete_uploaded_imagen, save_uploaded_image_to_frontend
from flask import jsonify, current_app
import glob


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
    if not user:
        attempt_id = log_attempt(rut, 'error', notes="RUT no encontrado")
        return jsonify({
            "status": "error",
            "attempt_id": attempt_id,
            "message": "RUT no encontrado"
        })

    name, image_path, folder_path = user['nombre'], user['path_foto'], user['path_carpeta_recientes']

    path_uploaded, filename_uploaded = save_uploaded_image_to_frontend(uploaded_image, rut)
    
    nombre_foto = copy_db_image_to_frontend(image_path)

    with open(path_uploaded, 'rb') as f:
        uploaded_bytes = f.read()
    embedding_uploaded = get_embedding(uploaded_bytes)

    if embedding_uploaded is None:
        attempt_id = log_attempt(
            rut, 'error',
            uploaded_image_path=f"uploads/{filename_uploaded}",
            db_image_path=nombre_foto,
            notes="Rostro no detectado"
        )
        delete_uploaded_imagen(path_uploaded)
        return jsonify({
            "status": "error",
            "attempt_id": attempt_id,
            "message": "Rostro no detectado, acérquese a la cámara"
        })

    with open(image_path, 'rb') as f:
        db_bytes = f.read()
    embedding_db = get_embedding(db_bytes)

    euclidean_dist = euclidean_distance(embedding_uploaded, embedding_db)
    cosine_dist = cosine_distance(embedding_uploaded, embedding_db)

    # procesamos la carpeta de recientes 
    embeddings_recientes=[]
    archivos = sorted(glob.glob(os.path.join(folder_path, '*')))[:5]
    for archivo in archivos: 
        with open(archivo, 'rb') as f:
            imagen_bytes = f.read()
        emb = get_embedding(imagen_bytes)
        if emb is not None: 
            embeddings_recientes.append(emb)    

    #calculamos las distancias para la carpeta recientes 
    recientes_cos_dist =  [
        cosine_distance(embedding_uploaded, emb)
        for emb in embeddings_recientes
    ]
    #promedio de las recientes
    prom_cos_recientes = sum(recientes_cos_dist) / len(recientes_cos_dist) if recientes_cos_dist else 1.0
    #ponderacion dando mas peso a ucampus
    peso_db = 0.7
    peso_recientes = 0.3
    dist_pond = peso_db * cosine_dist + peso_recientes * prom_cos_recientes

    # cambiar distancia coseno -> base métricas
    if cosine_dist <= 0.5:
        status = 'success'
        update_recientes(path_uploaded,rut)
    else:
        status = 'error'

    attempt_id = log_attempt(
        rut, status,
        cosine_distance=cosine_dist,
        euclidean_distance=euclidean_dist,
        uploaded_image_path=f"uploads/{filename_uploaded}",
        db_image_path=nombre_foto,
        notes=f"Ponderada: {dist_pond:.4f}"
    )

    # en todos los casos borramos
    #delete_uploaded_imagen(path_uploaded) 

    return jsonify({
        "status": "success" if dist_pond <= 0.5 else "error",
        "attempt_id": attempt_id,
        "message": "Acceso permitido" if dist_pond <= 0.5 else "Acceso denegado",
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
