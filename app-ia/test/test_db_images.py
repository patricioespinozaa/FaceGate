from PIL import Image
import os

def test_lectura_imagen(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Archivo no encontrado en: {image_path}")
        return False

    try:
        with Image.open(image_path) as img:
            img.verify()  # Verifica que sea una imagen válida
        print("✅ Imagen leída correctamente:", image_path)
        return True
    except Exception as e:
        print(f"❌ Error al abrir la imagen: {e}")
        return False
