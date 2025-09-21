"""
src/models/__init__.py

This file initializes the models package and exposes key functions for
training, inference, evaluation, and model registry.
"""

from .training import train_model, train_all_models
from .inference import predict, predict_batch
from .evaluation import evaluate_regression, evaluate_classification
from .registry import save_model, load_model, list_models

__all__ = [
    "train_model",
    "train_all_models",
    "predict",
    "predict_batch",
    "evaluate_regression",
    "evaluate_classification",
    "save_model",
    "load_model",
    "list_models"
]
