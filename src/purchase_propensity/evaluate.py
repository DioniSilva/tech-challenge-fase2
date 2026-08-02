from __future__ import annotations

from typing import Any

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def evaluate_model(y_true: Any, y_pred: Any, y_score: Any | None = None) -> dict[str, float]:
    """Calculate classification metrics for predictions.

    Args:
        y_true: Ground-truth binary labels.
        y_pred: Predicted binary labels.
        y_score: Optional positive-class scores for ROC AUC.

    Returns:
        Accuracy, precision, recall, F1, and optional ROC AUC metrics.
    """
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
    if y_score is not None:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_score))
    return metrics
