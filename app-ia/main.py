import os
from flask import request, jsonify, send_file
from app import app
from config.settings import PORT
from services.recognition import process_request
from services.database import get_result_by_rut

reset_guard_flag = False 

@app.route('/facegate/app-ia/reset_guard_view', methods=['POST'])
def reset_guard_view():
    global reset_guard_flag
    reset_guard_flag = True
    return jsonify({"status": "ok"})

@app.route('/facegate/app-ia/should_reset_guard', methods=['GET'])
def should_reset_guard():
    global reset_guard_flag
    if reset_guard_flag:
        reset_guard_flag = False
        return jsonify({"reset": True})
    return jsonify({"reset": False})

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

    return jsonify(get_result_by_rut(rut))

    

if __name__ == '__main__':
    app.run(port=PORT, debug=True)