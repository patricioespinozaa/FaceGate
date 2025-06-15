import os
from flask import request, jsonify, send_file
from app import app
from config.settings import PORT
from services.recognition import process_request

# Variable global para almacenar el último RUT
ultimo_rut = None

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict():
    rut = request.form.get('rut')
    uploaded_image = request.files.get('imagen')
    if uploaded_image is None:
        return {"status": "error", "message": "No image received"}

    global ultimo_rut
    ultimo_rut = None

    return process_request(uploaded_image, rut)

@app.route('/facegate/app-ia/store_rut', methods=['POST'])
def store_rut():
    global ultimo_rut
    rut = request.form.get('rut')
    if rut:
        ultimo_rut = rut
        return jsonify({"status": "success", "rut": rut})
    else:
        return jsonify({"status": "error", "message": "No RUT provided"})

@app.route('/facegate/app-ia/get_rut', methods=['GET'])
def get_rut():
    return jsonify({"rut": ultimo_rut})

@app.route('/facegate/app-ia/get_last_image', methods=['GET'])
def get_last_image():
    return jsonify({"image_url": "/facegate/app-ia/last_capture"})


@app.route('/facegate/app-ia/last_capture', methods=['GET'])
def serve_last_capture():
    capture_path = os.path.join(app.root_path, 'data', 'captured', 'last_capture.jpg')
    if not os.path.exists(capture_path):
        return jsonify({"status": "error", "message": "No capture available"}), 404
    return send_file(capture_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(port=PORT, debug=True)