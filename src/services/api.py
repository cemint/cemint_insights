"""
src/services/api.py
-------------------

Provides a simple REST API for serving predictions and recommendations.
Uses FastAPI.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from src.services.controllers import get_model_prediction, get_recommendation

app = FastAPI(title="CementAI Services API", version="1.0")

# -------------------------------
# Input Schema
# -------------------------------
class PredictRequest(BaseModel):
    model_name: str
    features: dict  # {"temperature": 1200, "mill_load": 85, ...}

class RecommendRequest(BaseModel):
    stage: str       # e.g., "raw_mill", "kiln", "utilities"
    parameters: dict # Current process parameters

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def home():
    return {"message": "CementAI Services API Running"}

@app.post("/predict")
def predict(request: PredictRequest):
    """
    Returns model prediction for given features.
    """
    return get_model_prediction(request.model_name, request.features)

@app.post("/recommend")
def recommend(request: RecommendRequest):
    """
    Returns process optimization recommendations for a stage.
    """
    return get_recommendation(request.stage, request.parameters)
