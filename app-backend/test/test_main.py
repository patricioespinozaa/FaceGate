import requests
import sys
import os
from main import port

# Añadir el directorio raíz del proyecto al path para importar módulos
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Construir ruta absoluta al archivo de imagen
image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', 'Foto_Patricio.jpg'))

# URL base del endpoint
url = f"http://localhost:{port}/facegate/app-ia/predict"

# Datos para enviar junto con la imagen
data = {'rut': '20918356-0'}

def post_image_and_get_response(image_path, data):
    with open(image_path, 'rb') as img_file:
        files = {'imagen': img_file}
        response = requests.post(url, files=files, data=data)
    return response.json()

def assert_response(expected, actual):
    assert expected['status'] == actual['status'], f"Expected status '{expected['status']}', got '{actual['status']}'"
    assert expected['message'] == actual['message'], f"Expected message '{expected['message']}', got '{actual['message']}'"
    # Comparar campos de data solo si existen para evitar errores si data es None o vacío
    expected_data = expected.get('data', {})
    actual_data = actual.get('data', {})
    for key in expected_data:
        assert expected_data[key] == actual_data.get(key), f"Expected data[{key}]='{expected_data[key]}', got '{actual_data.get(key)}'"

# Ejecutar petición
response_json = post_image_and_get_response(image_path, data)
print(response_json)

# Definición de casos de prueba
test_cases = {
    "positivo": {
        'expected': {
            'status': 'success',
            'message': 'Acceso permitido',
            'data': {
                'rut': '20918356-0',
                'nombre': 'Patricio Bastián Espinoza Acuña',
                'distancia_coseno': 0.31863516569137573,
                'distancia_euclidiana': 0.7982922792434692,
            }
        }
    },
    "rut_no_encontrado": {
        'expected': {
            'status': 'error',
            'message': 'Rut no encontrado',
            'data': {
                'rut': None,
                'nombre': None,
                'distancia_coseno': None,
                'distancia_euclidiana': None,
            }
        }
    },
    "distancia_mayor_1": {
        'expected': {
            'status': 'error',
            'message': 'Acceso denegado',
            'data': {
                'rut': '20918356-0',
                'nombre': 'Patricio Bastián Espinoza Acuña',
                'distancia_coseno': 0.31863516569137573,
                'distancia_euclidiana': 1.5,
            }
        }
    },
    "rostro_no_detectado": {
        'expected': {
            'status': 'error',
            'message': 'Rostro no detectado, acerquese a la cámara',
            'data': {
                'rut': None,
                'nombre': None,
                'distancia_coseno': None,
                'distancia_euclidiana': None,
            }
        }
    }
}

# Ejemplo de cómo usar los casos de prueba para validar respuestas (modificar según contexto real)
# Aquí solo validamos el test positivo contra la respuesta recibida
assert_response(test_cases["positivo"]['expected'], response_json)
