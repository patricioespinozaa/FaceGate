# FaceGate



## Backend

Pasos para configurar y ejecutar el backend correctamente:

### 1. Acceder a la carpeta del backend

```bash
cd app-backend
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv backend_env
source backend_env/bin/activate   # En Linux/Mac
backend_env\Scripts\activate      # En Windows
```

### 3. Instalar las dependencias
Instala las librerías necesarias desde el archivo backend_requirements.txt:
```bash
pip install -r backend_requirements.txt
```

### 4. Ejecutar los tests
Desde la carpeta app-backend, ejecutar los archivos de pruebas:

- Preprocesamiento en utils.py
```bash
python test/test_utils.py
```

- Funcionamiento de la aplicación 
```bash
# En una terminal se ejecuta la aplicación
python main.py
```

```bash
# En otra terminal se ejecuta el test de la app
python test/test_main.py
```