import os
from flask import request, jsonify, send_file
from app import app
from config.settings import PORT
from services.recognition import process_request

# Variable global para almacenar el último RUT
last_result = {
    "rut": None,
    "image_url": None,
    "predict_result": "pending"
}

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict():
    rut = request.form.get('rut')
    uploaded_image = request.files.get('imagen')
    if uploaded_image is None:
        return jsonify({"status": "error", "message": "No image received"})

    global last_result
    last_result["rut"] = rut
    last_result["image_url"] = None
    last_result["predict_result"] = "pending"

    response = process_request(uploaded_image, rut)

    response_json = response.get_json()
    last_result["image_url"] = "/facegate/app-ia/last_capture"
    last_result["predict_result"] = response_json.get("status", "error")

    return jsonify(response)

@app.route('/facegate/app-ia/store_rut', methods=['POST'])
def store_rut():
    global last_result
    rut = request.form.get('rut')
    if rut:
        last_result["rut"] = rut
        return jsonify({"status": "success", "rut": rut})
    else:
        return jsonify({"status": "error", "message": "No RUT provided"})

@app.route('/facegate/app-ia/get_rut', methods=['GET'])
def get_rut():
    global last_result
    return jsonify({"rut": last_result["rut"]})

@app.route('/facegate/app-ia/get_result', methods=['GET'])
def get_result():
    global last_result
    return jsonify(last_result)

@app.route('/facegate/app-ia/last_capture', methods=['GET'])
def serve_last_capture():
    capture_path = os.path.join(app.root_path, 'data', 'captured', 'last_capture.jpg')
    if not os.path.exists(capture_path):
        return jsonify({"status": "error", "message": "No capture available"}), 404
    return send_file(capture_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(port=PORT, debug=True)