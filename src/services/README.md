# CementAI Services Module

## Overview

The `services` module provides APIs and business logic for CementAI, including model inference, process recommendations, and controllers for handling plant operations. It is designed for modular, scalable, and PoC-ready deployment.

## Directory Structure

```text
src/services/
├── __init__.py
├── api.py          # FastAPI server for predictions and recommendations
├── controllers.py  # Handles business logic between APIs and models
└── recommender.py  # Generates AI-based process optimization suggestions
```

## Key Features

### API Layer (`api.py`)

- Provides REST endpoints for:
  - **Model Predictions**: `/predict`
  - **Process Recommendations**: `/recommend`
- Input validation with Pydantic.
- Modular and extensible for future ML/AI integration.

### Controllers (`controllers.py`)

- Bridges the API and ML models.
- Converts input JSON into DataFrame for inference.
- Handles recommendations by calling the recommender module.

### Recommender (`recommender.py`)

- Generates process optimization suggestions.
- Supports plant stages: `raw_mill`, `kiln`, `utilities`.
- PoC uses rule-based heuristics, extensible to AI/ML or Generative AI.
- Recommendations can be “normal,” “critical,” or “extreme,” mimicking real plant variability.

### Modular and Scalable

- Services are independent, adhering to SOLID principles.
- Can integrate seamlessly with synthetic data, data pipeline, ML models, and dashboard.

## Usage Examples

### 1. Start API Server

Run locally using FastAPI and Uvicorn:

```bash
uvicorn src.services.api:app --reload
```

- Server will be accessible at: `http://127.0.0.1:8000/`
- Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

### 2. Predict Endpoint

**POST** `/predict`

**Request Body:**

```json
{
  "model_name": "SPC_Model",
  "features": {
    "temperature": 1400,
    "mill_load": 85,
    "fuel_rate": 120,
    "residue": 5.2
  }
}
```

**Response Example:**

```json
{
  "model": "SPC_Model",
  "prediction": [87.5]
}
```

### 3. Recommend Endpoint

**POST** `/recommend`

**Request Body:**

```json
{
  "stage": "kiln",
  "parameters": {
    "temperature": 1460,
    "burner_rate": 120,
    "fan_speed": 95
  }
}
```

**Response Example:**

```json
{
  "stage": "kiln",
  "recommendation": {
    "action": "Reduce burner temperature by 20°C"
  }
}
```

## PoC Notes

- **Rule-based Recommender**: Generates recommendations based on thresholds.
- **Extensible to AI**: Easily replace heuristics with Generative AI or ML models for advanced optimization.

### Integration

- Works with `data_pipeline` and `models` modules.
- Predictions feed into the dashboard for KPI visualization (e.g., SPC reduction, TSR improvement, energy optimization).
- Configurable inputs support dynamic simulation scenarios (`normal`, `critical`, `extreme`) for PoC testing.

## Configuration Options

- Adjust plant stage parameters dynamically for testing.
- Compatible with synthetic datasets from `synthetic_data_gen`.
- Can scale to real-time plant data ingestion with minimal changes.

## Next Steps

- Integrate API with the dashboard module to visualize predictions.
- Connect recommender outputs with advanced process control modules for automation.
- Extend rule-based recommendations with ML models trained on real plant or synthetic datasets.
- Enable scheduled or event-driven triggers to run predictions automatically.

## Summary

This module ensures:

- Modular and scalable API services for CementAI.
- Predictive optimization and actionable recommendations.
- Seamless integration with other CementAI components.
- Extensibility for future AI/ML enhancements.