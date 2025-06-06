# metrics.py
from sklearn.metrics import classification_report

# Global metric state
# TP: El modelo predice correctamente el RUT de la persona.
# FN: El modelo no reconoce correctamente a una persona cuando debería haberlo hecho.
# TN: El modelo rechaza correctamente a alguien que intenta suplantar a otro.
# FP: El modelo afirma que una persona es alguien que no es.

TP = FP = TN = FN = 0
y_true = []
y_pred = []

def init_metrics():
    """Reinicia las métricas globales."""
    global TP, FP, TN, FN, y_true, y_pred
    TP = FP = TN = FN = 0
    y_true = []
    y_pred = []

def update_metrics(claimed_rut: str, real_rut: str, prediction_success: bool):
    """Actualiza métricas según el resultado de la predicción."""
    global TP, FP, TN, FN, y_true, y_pred

    # Si el RUT real coincide con el RUT reclamado
    if real_rut == claimed_rut:
        if prediction_success:
            TP += 1
            y_true.append(real_rut)
            y_pred.append(claimed_rut)
        else:
            FN += 1
            # Excluir casos "unknown"
            
    # Si el RUT real no coincide con el RUT reclamado
    else:
        if prediction_success:
            FP += 1
            y_true.append(real_rut)
            y_pred.append(claimed_rut)
        else:
            TN += 1
            # Excluir casos "unknown"

def report_metrics():
    """Imprime resumen de métricas con cálculos manuales y reporte sklearn."""
    # Legit: Una persona que intenta ingresar con su propio RUT.
    # Spoof: Una persona que intenta suplantar a otra persona.

    total_legit = TP + FN
    total_spoof = TN + FP
    total_cases = total_legit + total_spoof
    correct = TP + TN

    # Cálculos de métricas por clase
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

    # Métricas generales (macro promedio)
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

    print("\n=== METRICS (sklearn) ===")
    #print(classification_report(y_true, y_pred, digits=4, zero_division=0))

