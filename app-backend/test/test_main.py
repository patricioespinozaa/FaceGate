import requests
import sys
import os
from typing import Dict, Any

# Add the project's root directory to sys.path to import modules
root_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from main import port

# Base URL of the endpoint
url: str = f"http://localhost:{port}/facegate/app-ia/predict"

def post_image_and_get_response(image_path: str, data: Dict[str, str]) -> Dict[str, Any]:
    """
    Sends an image and form data via POST request to the API and returns the JSON response.

    Args:
        image_path (str): Path to the image file to be sent.
        data (Dict[str, str]): Form data dictionary to send alongside the image.

    Returns:
        Dict[str, Any]: JSON response from the server parsed into a dictionary.
    """
    with open(image_path, 'rb') as img_file:
        files = {'imagen': img_file}
        response = requests.post(url, files=files, data=data)
    return response.json()

def assert_response(expected: Dict[str, Any], actual: Dict[str, Any]) -> None:
    """
    Compares expected and actual API responses, asserting equality for specific fields.

    Args:
        expected (Dict[str, Any]): The expected response dictionary.
        actual (Dict[str, Any]): The actual response dictionary to test.

    Raises:
        AssertionError: If any of the compared fields differ.
    """
    assert expected['status'] == actual['status'], f"Expected status '{expected['status']}', got '{actual['status']}'"
    assert expected['message'] == actual['message'], f"Expected message '{expected['message']}', got '{actual['message']}'"

    # Compare data fields excluding the distance metrics
    excluded_keys = {'distancia_coseno', 'distancia_euclidiana'}
    expected_data = expected.get('data', {})
    actual_data = actual.get('data', {})

    for key in expected_data:
        if key not in excluded_keys:
            assert expected_data[key] == actual_data.get(key), f"Expected data[{key}]='{expected_data[key]}', got '{actual_data.get(key)}'"

# Test cases
test_cases = {
    "acceso_permitido": {
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
    "acceso_denegado": {
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

# Tests
image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', 'Foto_Patricio.jpg'))
data = {'rut': '20918356-0'}
response_json = post_image_and_get_response(image_path, data)
assert_response(test_cases["acceso_permitido"]['expected'], response_json)

image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', 'Foto_Patricio.jpg'))
data = {'rut': '12345678-9'}
response_json = post_image_and_get_response(image_path, data)
assert_response(test_cases["rut_no_encontrado"]['expected'], response_json)

data = {'rut': '20918356-0'}
image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', '20625224-3.jpg'))
response_json = post_image_and_get_response(image_path, data)
assert_response(test_cases["acceso_denegado"]['expected'], response_json)

data = {'rut': '20918356-0'}
image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', 'roku.jpg'))
response_json = post_image_and_get_response(image_path, data)
assert_response(test_cases["rostro_no_detectado"]['expected'], response_json)

print("All tests passed successfully.")