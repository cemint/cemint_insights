"""
src/data_pipeline/__init__.py
------------------------------

This package provides modules to load, preprocess, and transform
cement plant synthetic datasets for ML model training and inference.

Modules:
- loaders: Functions to load CSV data (synthetic or real-time)
- transformers: Data preprocessing, feature engineering, and anomaly detection
- pipelines: End-to-end pipelines combining loaders + transformers
"""

# -------------------------------
# Public Exports
# -------------------------------

# Loaders
from .loaders import (
    load_csv,
    load_all_stages,  # Updated from load_all_synthetic
    load_scenario,
)

# Transformers
from .transformers import (
    add_time_features,
    normalize_features,
    fill_missing_values,
    detect_anomalies,
    transform_pipeline,
)

# Pipelines
from .pipelines import (
    get_preprocessed_data,
    get_preprocessed_scenario,
    preprocess_single,
)

# -------------------------------
# Package Metadata
# -------------------------------
__version__ = "1.0.2"

# Explicitly define public API
__all__ = [
    # loaders
    "load_csv",
    "load_all_stages",
    "load_scenario",
    # transformers
    "add_time_features",
    "normalize_features",
    "fill_missing_values",
    "detect_anomalies",
    "transform_pipeline",
    # pipelines
    "get_preprocessed_data",
    "get_preprocessed_scenario",
    "preprocess_single",
    # wrapper
    "load_and_preprocess_all",
]


# -------------------------------
# Convenience Wrapper
# -------------------------------
def load_and_preprocess_all(data_dir="../data/synthetic/raw", normalize_method="minmax"):
    """
    Load all synthetic datasets and apply preprocessing pipeline.

    Args:
        data_dir (str): Directory containing raw synthetic datasets.
        normalize_method (str): Scaling method ("minmax" or "standard").

    Returns:
        dict: Dictionary of preprocessed DataFrames with dataset names as keys.
    """
    return get_preprocessed_data(data_dir=data_dir, normalize_method=normalize_method)
