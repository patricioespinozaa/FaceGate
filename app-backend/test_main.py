import requests

url = 'http://localhost:8902/facegate/app-ia/predict'

files = {'imagen': open('/ruta/a/tu/imagen.jpg', 'rb')}
data = {'rut': '12345678-9'}

response = requests.post(url, files=files, data=data)

print(response.json())
