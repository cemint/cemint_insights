# Data Pipeline Module

## Overview

The `data_pipeline` module is responsible for loading, preprocessing, and transforming synthetic cement plant datasets to make them ready for machine learning (ML) model training, inference, and analysis. It is designed to handle multiple datasets, time-based feature engineering, normalization, anomaly detection, and scenario-specific data.

## Folder Structure

```text
src/data_pipeline/
├── __init__.py          # Expose pipeline functions
├── loaders.py           # Load CSV files (synthetic or real-time)
├── transformers.py      # Preprocessing, feature engineering, normalization
└── pipelines.py         # End-to-end preprocessing pipeline
```

## Key Features

### Loaders

- Load single or multiple CSVs (fuel_usage, kiln, raw_mill, quality, utilities).
- Support scenario-based loading (normal, critical_low, critical_high).
- Robust error handling for missing/empty files.

### Transformers

- Add time-based features (hour, day, weekday, month).
- Normalize numeric features (MinMax or Standard scaling).
- Handle missing values (mean, median, zero).
- Detect anomalies using z-score.

### Pipelines

- Full preprocessing pipeline combining loaders and transformers.
- Scenario-specific pipelines.
- Single dataset or multi-dataset preprocessing.

### Convenience

- Centralized function to load and preprocess all datasets.
- Modular and reusable for PoC, ML experiments, or scaling.

## Usage Examples

# Data Pipeline – Usage Guide

This guide shows quick examples of how to use the `data_pipeline` module to load raw data, preprocess it, and run scenario-based pipelines.

---

## 📦 Importing the Package

```python
from data_pipeline import (
    load_raw_data,
    preprocess_data,
    run_pipeline,
)
```

---

## 1️⃣ Loading Raw Data

```python
# Load raw data from a CSV file
raw_data = load_raw_data("data/raw/fuel_consumption.csv")

print(raw_data.head())
```

---

## 2️⃣ Preprocessing Data

```python
# Preprocess the raw data (e.g., cleaning, feature engineering)
processed_data = preprocess_data(raw_data)

print(processed_data.head())
```

---

## 3️⃣ Running Scenario-Based Pipelines

You can define and run end-to-end pipelines for specific scenarios (e.g., fuel optimization, emissions monitoring, etc.).

```python
# Run a scenario-based pipeline
results = run_pipeline(
    scenario="fuel_optimization",
    input_path="data/raw/fuel_consumption.csv",
    output_path="data/processed/fuel_optimization_results.csv",
)

print("Pipeline results saved at:", results)
```

---

## 4️⃣ Available Scenarios

Currently supported:

- **fuel_optimization** – Analyze and optimize fuel consumption.
- **emissions_monitoring** – Track and reduce CO₂ emissions.
- **production_efficiency** – Optimize cement manufacturing production efficiency.

### Example

```python
results = run_pipeline(
    scenario="emissions_monitoring",
    input_path="data/raw/emissions_data.csv",
    output_path="data/processed/emissions_results.csv",
)
```

---

## 5️⃣ CLI Support (Optional)

You can also run the pipeline via CLI:

```bash
python -m data_pipeline --scenario fuel_optimization \
                        --input data/raw/fuel_consumption.csv \
                        --output data/processed/fuel_optimization_results.csv
```

---

✅ With this workflow, you can easily move from raw data → preprocessing → scenario pipelines.

## Integration with ML Models

The preprocessed data can be directly fed into ML models for:

- Regression (e.g., predicting Specific Power Consumption, Clinker quality).
- Classification / Anomaly Detection (e.g., critical_high / critical_low scenarios).
- Optimization models for energy consumption, fuel efficiency, and process stability.

## Notes

- The module is fully modular; you can preprocess individual datasets or all datasets at once.
- Supports scenario-based simulation for "normal", "critical_low", and "critical_high" situations.
- Designed for easy extension for real-time integration with IoT sensors or BigQuery.
- Can be integrated with Vertex AI pipelines for cloud-based model training and deployment.