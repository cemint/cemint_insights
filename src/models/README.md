# Models Module – CementAI

## Overview

The `models` module is responsible for training, evaluating, and performing inference on machine learning models for the CementAI project. It uses preprocessed synthetic or real plant data from the `data_pipeline` to generate predictions that optimize plant operations, monitor anomalies, and improve product quality.

## Directory Structure

```text
src/models/
├── __init__.py         # Initializes the models package
├── training.py         # Train regression/classification models
├── inference.py        # Generate predictions using trained models
├── evaluation.py       # Evaluate model performance
└── registry.py         # Save, load, and version models
```

## Key Features

### Training

- **Regression Models**: Predict energy consumption, SPC, feed efficiency.
- **Classification Models**: Detect anomalies (e.g., kiln temperature, critical scenarios).
- Supports single model or multiple model training.
- Automatic model saving with timestamped versioning.

### Inference

- Predict outcomes on new datasets.
- Batch predictions for multiple datasets/models.

### Evaluation

- **Regression Metrics**: MAE, RMSE, R².
- **Classification Metrics**: Accuracy, F1-score, Precision, Recall, Confusion Matrix.

### Model Registry

- Versioned storage of trained models.
- Easy loading of the latest model.
- List all saved models.

### Integration

- Works seamlessly with `data_pipeline` for end-to-end ML workflow.
- Modular design for scaling from PoC to full plant integration.

## Usage Examples

### 1. Training Models

**Train all models:**

```bash
python -m src.models.training
```

This will:

- Load preprocessed datasets from `data_pipeline`.
- Train regression and classification models.
- Save trained models in `models/latest/`.

**Train a single model:**

```python
from src.models.training import train_model
from src.data_pipeline.pipelines import get_preprocessed_data

data = get_preprocessed_data()
X = data["raw_mill"].drop(columns=["SPC"])
y = data["raw_mill"]["SPC"]
result = train_model(X, y, model_name="regressor")
print(result["metrics"])
```

### 2. Evaluate Models

```python
from src.models.evaluation import evaluate_regression, evaluate_classification

# Regression example
metrics = evaluate_regression([100, 150, 200], [110, 145, 205])
print(metrics)

# Classification example
metrics_clf = evaluate_classification([0, 1, 0, 1], [0, 1, 0, 0])
print(metrics_clf)
```

### 3. Inference

**Single Dataset Inference:**

```python
from src.models.inference import predict
from src.data_pipeline.pipelines import get_preprocessed_data

data = get_preprocessed_data()
X = data["raw_mill"].drop(columns=["SPC"])
predictions = predict("regressor", X)
print(predictions[:10])
```

**Batch Inference:**

```python
from src.models.inference import predict_batch

datasets_dict = get_preprocessed_data()
models_dict = {"SPC_Model": "regressor", "Kiln_Anomaly_Model": "classifier"}
preds = predict_batch(models_dict, datasets_dict)
print(preds)
```

### 4. Model Registry

```python
from src.models.registry import save_model, load_model, list_models

# Save a model
save_model(model, name="SPC_Model")

# Load the latest version
model = load_model("SPC_Model")

# List all models
print(list_models())
```

## Configuration

- **MODEL_DIR**: `models/latest/` – stores all trained models with timestamped filenames.
- Models are versioned automatically.
- Can be easily integrated with Vertex AI or other cloud ML platforms.

## PoC Notes

- Uses RandomForest for regression and classification for simplicity and speed.
- Fully compatible with synthetic datasets from `synthetic_data_gen`.
- Supports incremental scaling:
  - Add new features or datasets.
  - Train additional models for other plant subsystems (utilities, quality, fuel mix).

## Execution Options

- **Manual Trigger**: Run scripts individually for training, inference, or evaluation.
- **Automated Trigger**: Can be integrated into a pipeline that:
  - Runs after synthetic data generation.
  - Triggers `training.py` → `evaluation.py` → `inference.py`.

## Integration with Dashboard

- Predictions can be sent to the dashboard module for visualization.
- Helps in showing KPIs like SPC reduction, TSR increase, anomaly detection.

## Summary

This module forms the core ML engine of CementAI. It ensures:

- Predictive optimization of plant operations.
- Anomaly detection for safety and efficiency.
- Scalability from PoC to full-scale plant deployment.
- Easy integration with dashboards and decision-support tools.