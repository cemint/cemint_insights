"""
src/models/training.py
----------------------

Module for training machine learning models on synthetic cement plant data.
Supports regression (e.g., SPC, energy consumption) and classification (anomaly detection).
"""

import os
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.data_pipeline.pipelines import get_preprocessed_data
from .evaluation import evaluate_regression, evaluate_classification
from .registry import save_model

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../models/latest")

# -------------------------------
# Train a single regression model
# -------------------------------
def train_model(X, y, model_name="regressor", test_size=0.2, random_state=42):
    """
    Train a regression or classification model.

    Args:
        X (DataFrame): Feature matrix
        y (Series): Target variable
        model_name (str): 'regressor' or 'classifier'
        test_size (float): Train/test split fraction
        random_state (int): Random seed

    Returns:
        dict: trained model and evaluation metrics
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    if model_name == "regressor":
        model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_regression(y_test, y_pred)
    elif model_name == "classifier":
        model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_classification(y_test, y_pred, verbose=False)
    else:
        raise ValueError("model_name must be 'regressor' or 'classifier'")

    # Save model
    save_model(model, name=model_name)
    return {"model": model, "metrics": metrics}

# -------------------------------
# Train all models for PoC
# -------------------------------
def train_all_models():
    """
    Train models using all available preprocessed datasets.
    Returns dictionary of models and metrics.
    """
    data = get_preprocessed_data()
    results = {}

    # Example: Predicting SPC from raw_mill + fuel_usage features
    X = data["raw_mill"].drop(columns=["SPC"], errors="ignore")
    y = data["raw_mill"]["SPC"] if "SPC" in data["raw_mill"].columns else None
    if y is not None:
        results["SPC_Model"] = train_model(X, y, model_name="regressor")

    # Example: Anomaly detection for kiln temperature
    X_kiln = data["kiln"].drop(columns=["is_anomaly"], errors="ignore")
    y_kiln = data["kiln"]["is_anomaly"] if "is_anomaly" in data["kiln"].columns else None
    if y_kiln is not None:
        results["Kiln_Anomaly_Model"] = train_model(X_kiln, y_kiln, model_name="classifier")

    return results

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    results = train_all_models()
    for model_name, val in results.items():
        print(f"{model_name} metrics: {val['metrics']}")
