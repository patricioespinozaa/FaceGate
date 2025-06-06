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
    """Evalúa una imagen y actualiza las métricas."""
    result = send_image_to_api(image_path, claimed_rut)
    if result is None:
        print(f"[Error] with image '{image_path}': API call failed or invalid JSON.")
        return

    prediction_success = result.get("status") == "success"

    update_metrics(claimed_rut, real_rut, prediction_success)

def main() -> None:
    """Main function to evaluate all images in the evaluation directory."""
    init_metrics()
    all_ruts = [rut for rut in os.listdir(EVAL_DIR) if os.path.isdir(os.path.join(EVAL_DIR, rut))]

    for real_rut in tqdm(all_ruts, desc="🔎 Evaluating RUTs"):
        # Extract the real RUT folder path
        real_path = os.path.join(EVAL_DIR, real_rut)
        image_files = os.listdir(real_path) 

        # Iterate over each image in the RUT folder
        for image_name in tqdm(image_files, desc=f"📸 Images in RUT {real_rut}", leave=False):
            image_path = os.path.join(real_path, image_name)
            # Evaluate the image with the real RUT
            # Cases: TP, FN
            evaluate_image(image_path, claimed_rut=real_rut, real_rut=real_rut)

            # Evaluate the image with a random different RUT (spoofing case)
            # Cases: TN, FP 
            suplantadores = [r for r in all_ruts if r != real_rut]
            print(f"Usuario real: {real_rut}")
            print(f"Usuarios suplantadores: {suplantadores}")
            for fake_rut in suplantadores:
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
