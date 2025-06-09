# metrics.py
from tabulate import tabulate

# Global metric state
# TP: El modelo predice correctamente el RUT de la persona.
# FN: El modelo no reconoce correctamente a una persona cuando debería haberlo hecho.
# TN: El modelo rechaza correctamente a alguien que intenta suplantar a otro.
# FP: El modelo afirma que una persona es alguien que no es.

TP = FP = TN = FN = 0
y_true = []
y_pred = []

def init_metrics() -> None:
    """Init global metrics."""
    global TP, FP, TN, FN
    TP = FP = TN = FN = 0


def update_metrics(claimed_rut: str, real_rut: str, prediction_success: bool) -> None:
    """Update global metrics based on the evaluation result. 
    Args:
        claimed_rut (str): RUT that was used when sending the image.
        real_rut (str): The actual RUT associated with the image (ground truth).
        prediction_success (bool): True if the model successfully matched the RUT, False otherwise.

    Returns:
        None     
    """
    global TP, FP, TN, FN

    # Se esta probando con las imagenes de la carpeta del RUT real.
    # El claimed_rut corresponde a otro RUT con el que se prueba si la imagen permite el acceso.

    # Cuando se prueba una imagen de una carpeta, con el RUT de dicha carpeta
    if real_rut == claimed_rut:
        if prediction_success:
            TP += 1 
        else:
            FN += 1 
            
    # Cuando se prueba una imagen de una carpeta, con un RUT diferente al de la carpeta
    else:
        if prediction_success:
            FP += 1
        else:
            TN += 1

def report_metrics() -> None:
    """Report the evaluation metrics."""
    # Legit: Una persona que intenta ingresar con su propio RUT.
    # Spoof: Una persona que intenta suplantar a otra persona (imagen con un rut que no es el suyo).

    total_legit = TP + FN
    total_spoof = TN + FP
    total_cases = total_legit + total_spoof
    correct = TP + TN

    # Cálculos de métricas 
    accuracy_legit = TP / total_legit if total_legit else None
    recall_legit = TP / (TP + FN) if (TP + FN) else None
    precision_legit = TP / (TP + FP) if (TP + FP) else None
    f1_legit = (
        (2 * precision_legit * recall_legit) / (precision_legit + recall_legit)
        if (precision_legit and recall_legit and (precision_legit + recall_legit) != 0)
        else None
    )

    accuracy_spoof = TN / total_spoof if total_spoof else None
    recall_spoof = TN / (TN + FP) if (TN + FP) else None
    precision_spoof = TN / (TN + FN) if (TN + FN) else None
    f1_spoof = (
        (2 * precision_spoof * recall_spoof) / (precision_spoof + recall_spoof)
        if (precision_spoof and recall_spoof and (precision_spoof + recall_spoof) != 0)
        else None
    )

    # Métricas generales (macro)
    macro_accuracy = correct / total_cases if total_cases else None

    macro_precision = (
        ((precision_legit or 0) + (precision_spoof or 0)) / 2
    )
    macro_recall = (
        ((recall_legit or 0) + (recall_spoof or 0)) / 2
    )
    macro_f1 = (
        ((f1_legit or 0) + (f1_spoof or 0)) / 2
    )

    print("\n=== EVALUATION RESULTS ===")

    print(f"[Persona que intenta ingresar con su propio RUT]")
    print(f"  Total:           {total_legit}")
    print(f"  True Positives:  {TP}")
    print(f"  False Negatives: {FN}")
    print(f"  Accuracy:        {accuracy_legit:.2%}" if accuracy_legit is not None else "  Accuracy:        N/A")
    print(f"  Recall:          {recall_legit:.2%}" if recall_legit is not None else "  Recall:          N/A")
    print(f"  F1-score:        {f1_legit:.2%}" if f1_legit is not None else "  F1-score:        N/A")

    print(f"\n[Persona que intenta suplantar a otra persona]")
    print(f"  Total:           {total_spoof}")
    print(f"  True Negatives:  {TN}")
    print(f"  False Positives: {FP}")
    print(f"  Accuracy:        {accuracy_spoof:.2%}" if accuracy_spoof is not None else "  Accuracy:        N/A")
    print(f"  Recall:          {recall_spoof:.2%}" if recall_spoof is not None else "  Recall:          N/A")
    print(f"  F1-score:        {f1_spoof:.2%}" if f1_spoof is not None else "  F1-score:        N/A")

    print(f"\n[Métricas generales]")
    print(f"  Evaluaciones totales: {total_cases}")
    print(f"  Predicciones correctas: {correct}")
    print(f"  Exactitud (Accuracy):   {macro_accuracy:.2%}" if macro_accuracy is not None else "  Exactitud:        N/A")
    print(f"  Recall (macro):         {macro_recall:.2%}")
    print(f"  Precision (macro):      {macro_precision:.2%}")
    print(f"  F1-score (macro):       {macro_f1:.2%}")

    headers = ["Clase", "Total", "TP/TN", "FP/FN", "Accuracy", "Recall", "Precision", "F1-score"]

    table = [
        [
            "Legítimo",
            total_legit,
            TP,
            FN,
            f"{accuracy_legit:.2%}" if accuracy_legit is not None else "N/A",
            f"{recall_legit:.2%}" if recall_legit is not None else "N/A",
            f"{precision_legit:.2%}" if precision_legit is not None else "N/A",
            f"{f1_legit:.2%}" if f1_legit is not None else "N/A",
        ],
        [
            "Suplantador",
            total_spoof,
            TN,
            FP,
            f"{accuracy_spoof:.2%}" if accuracy_spoof is not None else "N/A",
            f"{recall_spoof:.2%}" if recall_spoof is not None else "N/A",
            f"{precision_spoof:.2%}" if precision_spoof is not None else "N/A",
            f"{f1_spoof:.2%}" if f1_spoof is not None else "N/A",
        ],
        [
            "Macro Promedio",
            total_cases,
            correct,
            "-",
            f"{macro_accuracy:.2%}" if macro_accuracy is not None else "N/A",
            f"{macro_recall:.2%}",
            f"{macro_precision:.2%}",
            f"{macro_f1:.2%}",
        ]
    ]

    print("\n=== 📊 MÉTRICAS DE EVALUACIÓN ===\n")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


