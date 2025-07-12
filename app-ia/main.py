import os
from flask import request, jsonify, send_file
from app import app
from config.settings import PORT
from services.recognition import process_request
from services.database import get_result_by_rut
import time


# Variable global para almacenar el último RUT
pending_rut = None

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict():
    rut = request.form.get('rut')
    uploaded_image = request.files.get('imagen')
    if uploaded_image is None:
        return jsonify({"status": "error", "message": "No image received"})

    response = process_request(uploaded_image, rut)

    global pending_rut
    pending_rut = None

    return response

@app.route('/facegate/app-ia/store_rut', methods=['POST'])
def store_rut():
    global pending_rut
    rut = request.form.get('rut')
    if rut:
        pending_rut = rut  # Sobrescribe el único slot
        return jsonify({"status": "success", "rut": rut})
    else:
        return jsonify({"status": "error", "message": "No RUT provided"})

@app.route('/facegate/app-ia/get_last_rut', methods=['GET'])
def get_last_rut():
    global pending_rut
    return jsonify({"rut": pending_rut})

@app.route('/facegate/app-ia/get_result', methods=['GET'])
def get_result():
    rut = request.args.get('rut')
    if not rut:
        return jsonify({"status": "error", "message": "No RUT provided"}), 400

    timeout = 20  # segundos
    interval = 0.5  # chequear cada 0.5 segundos
    elapsed = 0

    while elapsed < timeout:
        result = get_result_by_rut(rut)
        if result.get("status") != "pending":
            return jsonify(result)
        time.sleep(interval)
        elapsed += interval

    return jsonify(get_result_by_rut(rut))

if __name__ == '__main__':
    app.run(port=PORT, debug=True)