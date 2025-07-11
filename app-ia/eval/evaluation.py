# evaluation.py
import os
import time
import random
import argparse
from contextlib import redirect_stdout
from tqdm import tqdm
from dotenv import load_dotenv

from api_client import send_image_to_api
from metrics import init_metrics, update_metrics, report_metrics

load_dotenv()
EVAL_DIR = os.getenv("EVAL_DIR")

if not EVAL_DIR:
    raise ValueError("[Error] EVAL_DIR not set. Please define it in your .env file.")

def evaluate_image(image_path: str, claimed_rut: str, real_rut: str) -> None:
    """Evaluate a single image against the API with the claimed RUT.
    Args:
        image_path (str): Path to the image file to be evaluated.
        claimed_rut (str): RUT claimed in the API request (the one that was submitted).
        real_rut (str): Actual RUT corresponding to the image (ground truth).

    Returns:
        None
    
    """
    result = send_image_to_api(image_path, claimed_rut)
    if result is None:
        print(f"[Error] with image '{image_path}': API call failed or invalid JSON.")
        return

    print(f"Resultado = {result}") #NOTE: Al descomentarlo se guardará en el txt resultante (permite observar en que imagen falla)
    prediction_success = result.get("status") == "success" # Indica si la predicción fue exitosa o erronea
    update_metrics(claimed_rut, real_rut, prediction_success)

def main() -> None:
    """Main function to evaluate all images in the evaluation directory."""
    init_metrics()
    all_ruts = [rut for rut in os.listdir(EVAL_DIR) if os.path.isdir(os.path.join(EVAL_DIR, rut))]

    # Para cada rut, se extraen las imagenes de su carpeta.
    # En la segunda iteracion, se comprueba la imagen de la carpeta con el rut correspondiente (el rut del nombre de la carpeta)
    # En la tercera iteracion, se comprueba la imagen de la carpeta con el resto de ruts.
    # El funcionamiento es, para las imagenes de una carpeta, se prueba si se autoriza el acceso o no con cada uno de los ruts.
    start_time = time.time()
    image_count = sum(len(os.listdir(os.path.join(EVAL_DIR, rut))) for rut in all_ruts)
    print(f"Evaluating {len(all_ruts)} RUTs with a total of {image_count} images...")

    spoof_cases = {
        ("21095757-k", "21166885-7"),
        ("20918356-0", "19891604-8"),
        ("20918356-0", "20625224-3"),
        ("19891604-8", "20625224-3"),
        ("20625224-3", "21166885-7")
    }
    for real_rut in tqdm(all_ruts, desc="🔎 Evaluating RUTs"): 
        # Extract the real RUT folder path
        real_path = os.path.join(EVAL_DIR, real_rut)
        image_files = os.listdir(real_path) 
        image_files.sort()

        # Iterate over each image in the RUT folder
        for image_name in tqdm(image_files, desc=f"📸 Images in RUT {real_rut}", leave=False):
            image_path = os.path.join(real_path, image_name)
            # Evaluate the image with the real RUT
            # Cases: TP, FN
            evaluate_image(image_path, claimed_rut=real_rut, real_rut=real_rut)

    # Evaluate the image with a different RUT (spoofing case)
    # Cases: TN, FP 

    spoof_image_count = 0
    print("\nEvaluando casos de suplantación específicos...")
    for attacker_rut, claimed_rut in tqdm(spoof_cases, desc="🕵️ Casos de suplantación"):
        attacker_path = os.path.join(EVAL_DIR, attacker_rut)
        if not os.path.exists(attacker_path):
            print(f"[Advertencia] Carpeta no encontrada para suplantador: {attacker_rut}")
            continue

        image_files = sorted(os.listdir(attacker_path))[:25]  # Limita a 25
        for image_name in tqdm(image_files, desc=f"{attacker_rut} -> {claimed_rut}", leave=False):
            image_path = os.path.join(attacker_path, image_name)
            evaluate_image(image_path, claimed_rut=claimed_rut, real_rut=attacker_rut)
            spoof_image_count += 1

    total_images = image_count + spoof_image_count
    end_time = time.time()
    elapsed_time = end_time - start_time
    avg_time_per_image = elapsed_time / total_images if total_images > 0 else 0

    print("\n=== ⏱️ TIEMPO DE EJECUCIÓN ===")
    print(f"Total de imágenes evaluadas: {total_images}")
    print(f"Tiempo total: {elapsed_time:.2f} segundos")
    print(f"Tiempo promedio por imagen: {avg_time_per_image:.2f} segundos")
    report_metrics()

if __name__ == "__main__":
    # Parse command line arguments for output file
    parser = argparse.ArgumentParser(description="Facegate evaluation script.")
    parser.add_argument("output_file", type=str, help="Path to save the evaluation report (e.g., results.txt)")
    args = parser.parse_args()

    with open(args.output_file, "w") as f:
        with redirect_stdout(f):
            main()
