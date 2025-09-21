"""
src/models/registry.py
----------------------

Module for saving, loading, and versioning ML models.
"""

import os
import joblib
from datetime import datetime

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../models/latest")
os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------------
# Save model
# -------------------------------
def save_model(model, name):
    """
    Save trained model with timestamped version.

    Args:
        model: trained model object
        name (str): model name

    Returns:
        str: saved filepath
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.joblib"
    filepath = os.path.join(MODEL_DIR, filename)
    joblib.dump(model, filepath)
    print(f"Model saved at {filepath}")
    return filepath

# -------------------------------
# Load model
# -------------------------------
def load_model(name):
    """
    Load the latest version of the model by name.

    Args:
        name (str): model name

    Returns:
        trained model object
    """
    files = [f for f in os.listdir(MODEL_DIR) if f.startswith(name)]
    if not files:
        raise FileNotFoundError(f"No model found with name {name}")
    latest_file = sorted(files)[-1]
    model = joblib.load(os.path.join(MODEL_DIR, latest_file))
    return model

# -------------------------------
# List saved models
# -------------------------------
def list_models():
    """
    List all saved models in the registry.
    """
    return os.listdir(MODEL_DIR)

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    print("Saved models:", list_models())
