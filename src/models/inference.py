"""
src/models/inference.py
-----------------------

Module for performing predictions with trained ML models.
"""

import pandas as pd
from .registry import load_model

# -------------------------------
# Predict single dataset
# -------------------------------
def predict(model_name, X):
    """
    Load trained model and predict on input features.

    Args:
        model_name (str): Name of the saved model
        X (DataFrame): Input features

    Returns:
        array: Predicted values
    """
    model = load_model(model_name)
    return model.predict(X)

# -------------------------------
# Batch prediction for multiple datasets
# -------------------------------
def predict_batch(models_dict, datasets_dict):
    """
    Perform predictions for multiple models on multiple datasets.

    Args:
        models_dict (dict): {'SPC_Model': 'regressor', ...}
        datasets_dict (dict): {'raw_mill': DataFrame, ...}

    Returns:
        dict: Predictions per dataset
    """
    predictions = {}
    for model_name, model_type in models_dict.items():
        # Simple mapping for PoC
        if "SPC" in model_name:
            X = datasets_dict["raw_mill"].drop(columns=["SPC"], errors="ignore")
        elif "Kiln" in model_name:
            X = datasets_dict["kiln"].drop(columns=["is_anomaly"], errors="ignore")
        else:
            continue
        predictions[model_name] = predict(model_name, X)
    return predictions

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    from src.data_pipeline.pipelines import get_preprocessed_data

    data = get_preprocessed_data()
    preds = predict("regressor", data["raw_mill"].drop(columns=["SPC"], errors="ignore"))
    print(preds[:10])
