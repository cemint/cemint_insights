"""
src/models/evaluation.py
------------------------

Module to evaluate machine learning models for the cement plant PoC.
Supports regression and classification metrics.
"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import numpy as np

# -------------------------------
# Regression Evaluation
# -------------------------------
def evaluate_regression(y_true, y_pred):
    """
    Evaluate regression model predictions.

    Args:
        y_true (array-like): True target values
        y_pred (array-like): Predicted target values

    Returns:
        dict: Metrics including MAE, RMSE, R2
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }
    return metrics

# -------------------------------
# Classification Evaluation
# -------------------------------
def evaluate_classification(y_true, y_pred, verbose=True):
    """
    Evaluate classification model predictions.

    Args:
        y_true (array-like): True labels
        y_pred (array-like): Predicted labels
        verbose (bool): Print confusion matrix and metrics if True

    Returns:
        dict: Metrics including Accuracy, F1-score, Precision, Recall
    """
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")
    precision = precision_score(y_true, y_pred, average="weighted")
    recall = recall_score(y_true, y_pred, average="weighted")
    cm = confusion_matrix(y_true, y_pred)

    metrics = {
        "Accuracy": acc,
        "F1-Score": f1,
        "Precision": precision,
        "Recall": recall,
        "Confusion_Matrix": cm
    }

    if verbose:
        print("Classification Metrics:")
        print(f"Accuracy: {acc:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print("Confusion Matrix:")
        print(cm)

    return metrics

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # Regression Example
    y_true_reg = [100, 150, 200, 250, 300]
    y_pred_reg = [110, 145, 205, 240, 310]
    print("Regression Metrics:", evaluate_regression(y_true_reg, y_pred_reg))

    # Classification Example
    y_true_clf = [0, 1, 0, 1, 1, 0, 0]
    y_pred_clf = [0, 1, 0, 0, 1, 0, 1]
    evaluate_classification(y_true_clf, y_pred_clf)
