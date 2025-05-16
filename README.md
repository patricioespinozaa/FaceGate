# FaceGate



# Ejecución del Backend

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
Desde la carpeta app-backend, ejecuta el archivo de pruebas:
```bash
python test/test.py
```