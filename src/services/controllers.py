"""
src/services/controllers.py
---------------------------

Controllers handle the business logic for APIs.
"""

import pandas as pd
from src.models.inference import predict
from src.services.recommender import generate_recommendation

# -------------------------------
# Controller: Model Prediction
# -------------------------------
def get_model_prediction(model_name: str, features: dict):
    """
    Convert features dict to DataFrame and predict using ML model.
    """
    try:
        df = pd.DataFrame([features])
        preds = predict(model_name, df)
        return {"model": model_name, "prediction": preds.tolist()}
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Controller: Process Recommendation
# -------------------------------
def get_recommendation(stage: str, parameters: dict):
    """
    Returns AI-driven recommendation for process optimization.
    """
    try:
        recommendation = generate_recommendation(stage, parameters)
        return {"stage": stage, "recommendation": recommendation}
    except Exception as e:
        return {"error": str(e)}
