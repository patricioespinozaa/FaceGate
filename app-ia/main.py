from flask import request
from app import app
from config.settings import PORT
from services.recognition import process_request

@app.route('/facegate/app-ia/predict', methods=['POST'])
def predict():
    rut = request.form.get('rut')
    uploaded_image = request.files.get('imagen')
    if uploaded_image is None:
        return {"status": "error", "message": "No image received"}

    return process_request(uploaded_image, rut)

if __name__ == '__main__':
    app.run(port=PORT, debug=True)