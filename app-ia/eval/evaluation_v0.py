import os
import random
import requests
import argparse
from contextlib import redirect_stdout
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix
import os

# Configuration
from dotenv import load_dotenv
from config import API_URL
load_dotenv()
EVAL_DIR = os.getenv("EVAL_DIR")

# Global counters for confusion matrix components
TP = FP = TN = FN = 0

# TP: El modelo predice correctamente el RUT de la persona.
# TN: El modelo rechaza correctamente a alguien que intenta suplantar a otro.
# FP: El modelo afirma que una persona es alguien que no es.
# FN: El modelo no reconoce correctamente a una persona cuando debería haberlo hecho.

# Lists for true and predicted labels for metric calculations
y_true = []
y_pred = []

def evaluate_image(image_path: str, claimed_rut: str, real_rut: str) -> None:
    """
    Sends an image to the prediction API with a claimed RUT and compares the response
    with the actual RUT, updating global counters and label lists for evaluation.

    Args:
        image_path (str): Path to the image file to evaluate.
        claimed_rut (str): The RUT claimed in the request (identity to verify).
        real_rut (str): The true RUT of the person in the image.

    Returns:
        None: This function updates global counters and lists directly.
    """
    global TP, FP, TN, FN

    with open(image_path, "rb") as img_file:
        files = {"imagen": img_file}
        data = {"rut": claimed_rut}

        try:
            response = requests.post(API_URL, files=files, data=data, timeout=10)
            response.raise_for_status()
            result = response.json()

            prediction_success = result.get("status") == "success" # Check if the prediction was successful

            if real_rut == claimed_rut:
                # Legitimate case: image belongs to claimed RUT
                if prediction_success: 
                    TP += 1
                    y_true.append(real_rut)
                    y_pred.append(claimed_rut)
                else:
                    FN += 1
                    y_true.append(real_rut)
                    y_pred.append("unknown") #NOTE: Se podria remover este label 
            else:
                # Spoofing case: image does not belong to claimed RUT
                if prediction_success:
                    FP += 1
                    y_true.append(real_rut)
                    y_pred.append(claimed_rut)
                # If the prediction failed, we assume it's a negative case
                else:
                    TN += 1
                    y_true.append(real_rut)
                    y_pred.append("unknown") #NOTE: Se podria remover este label

        except Exception as e:
            print(f"❌ Error with image '{image_path}': {e}")

def main() -> None:
    """
    Main function to execute the evaluation process over all images and RUTs.

    Steps:
    - Lists all RUT folders in the evaluation directory.
    - For each image in each RUT folder, performs two tests:
      1. Claims the real RUT (legitimate case).
      2. Claims a random different RUT (spoofing case).
    - Collects metrics and prints a summary with classification report.

    Returns:
        None
    """
    global TP, FP, TN, FN, y_true, y_pred

    # Get all RUT folder names
    all_ruts = [rut for rut in os.listdir(EVAL_DIR) if os.path.isdir(os.path.join(EVAL_DIR, rut))]

    for real_rut in tqdm(all_ruts, desc="🔎 Evaluating RUTs"):
            real_path = os.path.join(EVAL_DIR, real_rut)
            image_files = os.listdir(real_path)

            for image_name in tqdm(image_files, desc=f"📸 Images in RUT {real_rut}", leave=False):
                image_path = os.path.join(real_path, image_name)

                # Case 1: Legitimate attempt
                evaluate_image(image_path, claimed_rut=real_rut, real_rut=real_rut)

                # Case 2: Spoofing attempt
                suplantadores = [r for r in all_ruts if r != real_rut]
                fake_rut = random.choice(suplantadores)
                evaluate_image(image_path, claimed_rut=fake_rut, real_rut=real_rut)

    # Print confusion matrix counts
    print("\n=== EVALUATION RESULTS ===")
    total_legit = TP + FN   # Casos en los que claimed_rut == real_rut
    total_spoof = TN + FP   # Casos en los que claimed_rut != real_rut

    print("\n=== EVALUATION RESULTS ===")
    print(f"[Legitimate attempts]")
    print(f"  Total:           {total_legit}")
    print(f"  True Positives:  {TP}")
    print(f"  False Negatives: {FN}")
    print(f"  Accuracy:        {TP / total_legit:.2%}" if total_legit > 0 else "  Accuracy:        N/A")

    print(f"\n[Spoofing attempts]")
    print(f"  Total:           {total_spoof}")
    print(f"  True Negatives:  {TN}")
    print(f"  False Positives: {FP}")
    print(f"  Accuracy:        {TN / total_spoof:.2%}" if total_spoof > 0 else "  Accuracy:        N/A")

    # Optional: global accuracy
    total_cases = total_legit + total_spoof
    correct = TP + TN
    print(f"\n[Overall]")
    print(f"  Total evaluations: {total_cases}")
    print(f"  Correct predictions: {correct}")
    print(f"  Overall Accuracy:   {correct / total_cases:.2%}" if total_cases > 0 else "  Overall Accuracy:   N/A")


    # Print classification metrics report
    print("\n=== METRICS (sklearn) ===")
    print(classification_report(y_true, y_pred, digits=4, zero_division=0))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facegate evaluation script.")
    parser.add_argument("output_file", type=str, help="Path to save the evaluation report (e.g., results.txt)")
    args = parser.parse_args()

    with open(args.output_file, "w") as f:
        with redirect_stdout(f):
            main()
