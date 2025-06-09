# evaluation.py
import os
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

    # print(f"Resultado = {result}") #NOTE: Al descomentarlo se guardará en el txt resultante (permite observar en que imagen falla)
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

            # Evaluate the image with a random different RUT (spoofing case)
            # Cases: TN, FP 
            suplantadores = [r for r in all_ruts if r != real_rut]
            with tqdm(suplantadores, desc=f"🕵️ Probando {image_name}", leave=False) as pbar:
                for fake_rut in pbar:
                    pbar.set_postfix({'Suplantador': fake_rut})
                    # print(f"Evaluated {image_name} with claimed RUT '{fake_rut}' against real RUT '{real_rut}'.") #NOTE: Al descomentarlo se guardará en el txt resultante (permite observar en que imagen falla)
                    evaluate_image(image_path, claimed_rut=fake_rut, real_rut=real_rut)

    report_metrics()

if __name__ == "__main__":
    # Parse command line arguments for output file
    parser = argparse.ArgumentParser(description="Facegate evaluation script.")
    parser.add_argument("output_file", type=str, help="Path to save the evaluation report (e.g., results.txt)")
    args = parser.parse_args()

    with open(args.output_file, "w") as f:
        with redirect_stdout(f):
            main()
