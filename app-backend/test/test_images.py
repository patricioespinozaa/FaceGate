import requests
import sys
import os
from typing import Dict, Any

# Root directory of the project
root_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from main import port

# Base URL of the API endpoint for face recognition prediction
url: str = f"http://localhost:{port}/facegate/app-ia/predict"

def post_image_and_get_response(image_path: str, data: Dict[str, str]) -> Dict[str, Any]:
    """
    Sends a POST request with an image file and form data to the prediction API,
    then returns the JSON response as a dictionary.

    Args:
        image_path (str): Absolute path to the image file to be uploaded.
        data (Dict[str, str]): Form data to be sent alongside the image (e.g., user 'rut').

    Returns:
        Dict[str, Any]: Parsed JSON response from the API as a dictionary.
    """
    with open(image_path, 'rb') as img_file:
        files = {'imagen': img_file}
        response = requests.post(url, files=files, data=data)
    return response.json()

def assert_response(expected: Dict[str, Any], actual: Dict[str, Any]) -> None:
    """
    Compares the expected and actual API responses for key fields,
    asserting that 'status' and 'message' match, as well as all data fields
    except specific distance metrics which are excluded from strict equality.

    Args:
        expected (Dict[str, Any]): The expected response dictionary.
        actual (Dict[str, Any]): The actual response dictionary to validate.

    Raises:
        AssertionError: If any of the compared fields do not match.
    """
    assert expected['status'] == actual['status'], f"Expected status '{expected['status']}', got '{actual['status']}'"
    assert expected['message'] == actual['message'], f"Expected message '{expected['message']}', got '{actual['message']}'"

    excluded_keys = {'distancia_coseno', 'distancia_euclidiana'}
    expected_data = expected.get('data', {})
    actual_data = actual.get('data', {})

    for key in expected_data:
        if key not in excluded_keys:
            assert expected_data[key] == actual_data.get(key), f"Expected data[{key}]='{expected_data[key]}', got '{actual_data.get(key)}'"

def assert_images_exist(response: Dict[str, Any]) -> None:
    """
    Checks if the response contains valid image URLs in the 'images' field,
    asserting that the URLs start with the expected static path prefix.

    Args:
        response (Dict[str, Any]): The API response dictionary to check.

    Raises:
        AssertionError: If image URLs are missing or do not have the expected format.
    """
    images = response.get('images', {})
    uploaded_url = images.get('uploaded_url')
    db_url = images.get('db_url')

    assert uploaded_url is not None and uploaded_url.startswith("/static/"), f"Invalid uploaded_url: {uploaded_url}"
    assert db_url is not None and db_url.startswith("/static/"), f"Invalid db_url: {db_url}"

# Example test execution - adjust paths as needed for your environment
image_path = os.path.abspath(os.path.join(root_dir, 'test', 'src', 'Foto_Patricio.jpg'))
data = {'rut': '20918356-0'}

expected_response = {
    'status': 'success',
    'message': 'Acceso permitido',
    'data': {
        'rut': '20918356-0',
        'nombre': 'Patricio Bastián Espinoza Acuña',
        'distancia_coseno': None,
        'distancia_euclidiana': None,
    }
}

response_json = post_image_and_get_response(image_path, data)
assert_response(expected_response, response_json)
assert_images_exist(response_json)

print("✅ Test 'acceso permitido' passed successfully.")
