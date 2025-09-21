"""
src/data_pipeline/pipelines.py
------------------------------

Module for creating end-to-end data pipelines for synthetic cement plant datasets.
Combines loaders, schema validation, and transformers to output preprocessed
DataFrames ready for ML or dashboard consumption.
"""

import logging
import sys
import os
from pathlib import Path

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.data_pipeline.loaders import load_all_stages, load_scenario
from src.data_pipeline.transformers import (
    add_time_features,
    fill_missing_values,
    clip_outliers,
    normalize_features,
    create_kpis,
)
from src.data_pipeline.schemas import SCHEMAS  # schema dict per stage
import pandas as pd
import json
import joblib
from glob import glob

# -------------------------------
# Logger Setup
# -------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Enhanced logging for debugging
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG


# -------------------------------
# Schema Validation
# -------------------------------
# Enhanced schema validation to check for empty columns and timestamp formats
def validate_schema(df: pd.DataFrame, stage: str):
    """
    Validate DataFrame schema against predefined schema.

    Args:
        df (pd.DataFrame): Input DataFrame
        stage (str): Stage name to validate against

    Returns:
        bool: True if schema is valid, raises ValueError otherwise
    """
    if stage not in SCHEMAS:
        raise ValueError(f"Schema for stage '{stage}' not found.")

    schema = SCHEMAS[stage]
    expected_columns = schema.get("columns", [])

    # Ensure input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Input data for stage '{stage}' must be a DataFrame, got {type(df)}")

    # Ensure all columns are DataFrame-compatible
    for col in df.columns:
        if isinstance(df[col], pd.Series):
            # Ensure column is part of the DataFrame without converting to a single-column DataFrame
            df[col] = pd.DataFrame(df[col]) if len(df[col].shape) == 1 else df[col]

    # Check for missing columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in DataFrame for stage '{stage}': {missing_columns}")

    # Check for extra columns
    extra_columns = [col for col in df.columns if col not in expected_columns]
    if extra_columns:
        logger.warning(f"Extra columns in DataFrame for stage '{stage}': {extra_columns}")

    # Check for empty columns
    empty_columns = [col for col in df.columns if df[col].dropna().empty]
    if empty_columns:
        raise ValueError(f"Empty columns in DataFrame for stage '{stage}': {empty_columns}")

    # Validate timestamp format
    if "timestamp" in df.columns:
        try:
            pd.to_datetime(df["timestamp"])
        except Exception as e:
            raise ValueError(f"Timestamp parse error in stage '{stage}': {e}")

    logger.info(f"[{stage}] Schema validation passed ✅")
    logger.debug(f"[{stage}] DataFrame structure after validation: {df.dtypes}")
    logger.debug(f"Schema validation input data type: {type(df)}")
    logger.debug(f"Schema validation input data columns: {df.columns if isinstance(df, pd.DataFrame) else 'N/A'}")
    return True


# -------------------------------
# Preprocessing for a single dataset
# -------------------------------
# Enhanced error handling in preprocess_single
# Add debug logs to trace DataFrame structure in preprocess_single
def preprocess_single(df: pd.DataFrame, stage: str, normalize_method: str = "minmax") -> pd.DataFrame:
    """
    Apply preprocessing (schema validation + time features + normalization) 
    to a single DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        stage (str): Stage name (e.g., "stage1_raw_material").
        normalize_method (str): Scaling method, "minmax" or "standard".

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Validate schema
    validate_schema(df, stage)
    assert isinstance(df, pd.DataFrame), f"[{stage}] Schema validation did not return a DataFrame"

    logger.debug(f"[{stage}] Initial DataFrame: Rows={len(df)}, Columns={len(df.columns)}")
    logger.debug(f"Preprocessing stage: {stage}, initial DataFrame structure: {df.dtypes}")

    # Add engineered features
    try:
        df = add_time_features(df)
        assert isinstance(df, pd.DataFrame), f"[{stage}] Adding time features did not return a DataFrame"
        logger.debug(f"[{stage}] After adding time features: Rows={len(df)}, Columns={len(df.columns)}")
    except Exception as e:
        logger.error(f"Error adding time features for stage {stage}: {e}")
        raise

    # Normalize numeric features
    try:
        df, _ = normalize_features(df, method=normalize_method)
        assert isinstance(df, pd.DataFrame), f"[{stage}] Normalization did not return a DataFrame"
        logger.debug(f"[{stage}] After normalization: Rows={len(df)}, Columns={len(df.columns)}")
    except Exception as e:
        logger.error(f"Error normalizing features for stage {stage}: {e}")
        raise

    logger.info(f"[{stage}] Preprocessing complete ✅")
    logger.debug(f"Post-processing stage: {stage}, final DataFrame structure: {df.dtypes}")
    logger.debug(f"Preprocessing input data type: {type(df)}")
    logger.debug(f"Preprocessing input data columns: {df.columns if isinstance(df, pd.DataFrame) else 'N/A'}")
    return df


# -------------------------------
# Save Preprocessed Data
# -------------------------------
def save_preprocessed_data(preprocessed_data, scalers):
    """
    Save preprocessed datasets, statistics, and scalers to the processed directory.

    Args:
        preprocessed_data (dict): Dictionary of preprocessed DataFrames.
        scalers (dict): Dictionary of scalers used for normalization.
    """
    try:
        # Directory for processed data
        PROCESSED_DIR = os.path.abspath(os.path.join(os.getcwd(), "processed"))
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        SCALERS_DIR = os.path.abspath(os.path.join(os.getcwd(), "artifacts/scalers"))
        os.makedirs(SCALERS_DIR, exist_ok=True)

        logger.debug(f"Processed directory: {PROCESSED_DIR}")
        logger.debug(f"Preprocessed data to save: {list(preprocessed_data.keys())}")

        for stage, df in preprocessed_data.items():
            # Log DataFrame structure before saving
            logger.debug(f"Saving DataFrame for {stage}: Shape: {df.shape}, Columns: {list(df.columns)}")

            # Validate DataFrame structure
            if df.empty:
                logger.warning(f"⚠️ DataFrame for {stage} is empty. Skipping save.")
                continue

            # Ensure DataFrame matches schema
            expected_columns = SCHEMAS.get(stage, {}).get("columns", [])
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"❌ Missing columns in DataFrame for {stage}: {missing_columns}. Skipping save.")
                continue

            # Save processed CSV
            csv_path = os.path.join(PROCESSED_DIR, f"{stage}_processed.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"✅ Saved preprocessed CSV for {stage} at {csv_path}")

            # Save processed Parquet
            parquet_path = os.path.join(PROCESSED_DIR, f"{stage}_processed.parquet")
            df.to_parquet(parquet_path, index=False)
            logger.info(f"✅ Saved preprocessed Parquet for {stage} at {parquet_path}")

            # Save statistics
            stats = df.describe().to_dict()
            stats_path = os.path.join(PROCESSED_DIR, f"{stage}_stats.json")
            with open(stats_path, "w") as stats_file:
                json.dump(stats, stats_file)
            logger.info(f"✅ Saved statistics for {stage} at {stats_path}")

            # Save scaler
            if stage in scalers:
                scaler_path = os.path.join(SCALERS_DIR, f"{stage}_scaler.joblib")
                joblib.dump(scalers[stage], scaler_path)
                logger.info(f"✅ Saved scaler for {stage} at {scaler_path}")
    except Exception as e:
        logger.error(f"Error saving preprocessed data: {e}")
        raise


# -------------------------------
# Full Preprocessing Pipeline
# -------------------------------
def get_preprocessed_data(data_dir: str = "../data/synthetic/raw", normalize_method: str = "minmax"):
    """
    Load all synthetic datasets, apply schema validation, 
    feature engineering, and normalization.

    Args:
        data_dir (str): Directory where synthetic CSVs are stored.
        normalize_method (str): Scaling method, "minmax" or "standard".

    Returns:
        dict: Dictionary of preprocessed DataFrames with keys as dataset names.
    """
    print("get_preprocessed_data function called")
    print("get_preprocessed_data function execution started")
    try:
        # Ensure raw data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.warning(f"⚠️ Raw data directory created: {data_dir}")

        logger.debug(f"Checking raw data directory: {data_dir}")
        print("Invoking load_all_stages function")
        print(f"Arguments for load_all_stages: data_dir={data_dir}")
        datasets = load_all_stages(data_dir)  # Updated function call
        print(f"Loaded datasets: {list(datasets.keys())}")
        print(f"Data returned by load_all_stages: {datasets}")

        preprocessed = {}
        scalers = {}
        for name, df in datasets.items():
            logger.debug(f"Processing dataset: {name}, Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"Processing dataset: {name}, Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"Iterating over dataset: {name}")
            preprocessed[name], scalers[name] = preprocess_single(df, stage=name, normalize_method=normalize_method)

        logger.info("✅ All datasets preprocessed successfully")

        # Debug logging of preprocessed data
        logger.debug(f"Preprocessed data keys: {list(preprocessed.keys())}")
        print(f"Preprocessed data keys: {list(preprocessed.keys())}")
        for name, df in preprocessed.items():
            logger.debug(f"Dataset: {name}, Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"Dataset: {name}, Rows: {len(df)}, Columns: {len(df.columns)}")

        # Save preprocessed data
        print("Calling save_preprocessed_data function")
        save_preprocessed_data(preprocessed, scalers)

        # Log the output directory and file paths
        logger.info(f"Saving processed files to directory: {output_dir}")
        for file_name in os.listdir(output_dir):
            logger.info(f"File saved: {file_name}")

        print("get_preprocessed_data function completed")
        print("get_preprocessed_data is returning early")
        return preprocessed
    except Exception as e:
        logger.error(f"Error in preprocessing data: {e}")
        raise


# -------------------------------
# Scenario-specific pipeline
# -------------------------------
def get_preprocessed_scenario(
    data_dir: str = "../data/synthetic/raw",
    scenario: str = "normal",
    normalize_method: str = "minmax"
):
    """
    Load scenario-specific datasets and apply preprocessing.

    Args:
        data_dir (str): Directory containing scenario CSVs.
        scenario (str): Scenario to load ("normal", "critical_low", "critical_high").
        normalize_method (str): Scaling method.

    Returns:
        dict: Preprocessed scenario-specific datasets.
    """
    try:
        logger.info(f"Loading scenario: {scenario} ...")
        datasets = load_scenario(data_dir=data_dir, scenario=scenario)

        preprocessed = {}
        for name, df in datasets.items():
            preprocessed[name] = preprocess_single(df, stage=name, normalize_method=normalize_method)

        logger.info(f"✅ Scenario '{scenario}' preprocessed successfully")
        return preprocessed
    except Exception as e:
        logger.error(f"Error in preprocessing scenario '{scenario}': {e}")
        raise


def get_preprocessed_data(data_dir, normalize_method="minmax"):
    """
    Preprocess data from a given directory.

    Args:
        data_dir (str): Path to the directory containing raw data.
        normalize_method (str): Method for scaling numeric features ('minmax' or 'standard').

    Returns:
        dict: Dictionary of preprocessed DataFrames for each stage.
    """
    processed_data = {}
    stage_dirs = glob(os.path.join(data_dir, "stage*"))

    for stage_dir in stage_dirs:
        stage_name = os.path.basename(stage_dir)
        csv_files = glob(os.path.join(stage_dir, "*.csv"))

        for file_path in csv_files:
            df = pd.read_csv(file_path)

            # Apply transformations
            df = add_time_features(df)
            df, scaler = normalize_features(df, method=normalize_method)
            df = fill_missing_values(df, strategy="mean")
            df = clip_outliers(df, columns=df.select_dtypes(include=["number"]).columns)
            df = create_kpis(df)

            # Save processed data
            output_path = os.path.join("data/synthetic/processed/", os.path.basename(data_dir), f"{stage_name}_processed.csv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            logger.info(f"✅ Processed data saved to {output_path}")

            # Save stats
            stats = df.describe().to_dict()
            stats_path = output_path.replace("_processed.csv", "_stats.json")
            with open(stats_path, "w") as stats_file:
                json.dump(stats, stats_file)

            # Save scaler (if applicable)
            scaler_path = os.path.join("artifacts/scalers", f"{stage_name}_scaler.joblib")
            os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
            joblib.dump(df.select_dtypes(include=["number"]).columns, scaler_path)

            processed_data[stage_name] = df

    return processed_data


# -------------------------------
# Main Entry Point
# -------------------------------
# Modify the main entry point to support stage-specific execution
if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Run data pipeline for raw files.")
    parser.add_argument("--data_dir", type=str, default="data/synthetic/raw/", help="Path to the raw data directory")
    parser.add_argument("--output_dir", type=str, default="data/synthetic/processed/", help="Path to save the processed data")
    parser.add_argument("--stage", type=str, default=None, help="Specific stage to process (e.g., stage1_raw_materials)")

    args = parser.parse_args()

    # Get current timestamp for output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(args.output_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Load datasets
    from src.data_pipeline.loaders import load_all_stages, load_stage_data

    if args.stage:
        # Find the latest timestamped folder
        timestamp_folders = sorted(glob(os.path.join(args.data_dir, "*")))
        if not timestamp_folders:
            raise FileNotFoundError(f"No timestamped folders found in {args.data_dir}")

        latest_folder = timestamp_folders[-1]
        stage_dir = os.path.join(latest_folder, args.stage)
        if not os.path.exists(stage_dir):
            raise FileNotFoundError(f"Stage directory not found: {stage_dir}")

        datasets = {args.stage: load_stage_data(stage_dir)}
    else:
        # Process all stages
        datasets = load_all_stages(args.data_dir)

    # Process and save each dataset
    from src.data_pipeline.transformers import transform_pipeline

    for stage, data_dict in datasets.items():
        for file_name, df in data_dict.items():
            if not isinstance(df, pd.DataFrame):
                logger.error(f"Expected DataFrame for {file_name} in stage {stage}, but got {type(df)}")
                continue

            print(f"Processing {file_name} for stage {stage}...")
            try:
                processed_df = transform_pipeline(df)

                # Save processed data
                output_path = os.path.join(output_dir, f"{file_name}_processed.csv")
                processed_df.to_csv(output_path, index=False)
                print(f"Processed data saved to {output_path}")
            except Exception as e:
                logger.error(f"Error processing {file_name} in stage {stage}: {e}")

    logger.info(f"All datasets processed and saved under {output_dir}")
    print(f"All datasets processed and saved under {output_dir}")
