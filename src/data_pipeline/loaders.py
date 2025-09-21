"""
src/data_pipeline/loaders.py
----------------------------

Module for loading synthetic and real-time cement plant datasets.
Provides robust CSV loading with error handling and stage-wise organization.
"""

import os
import glob
import pandas as pd
import json
from dateutil.parser import parse as dtparse
import logging


# Configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


SCHEMA_DIR = "data/synthetic/schema"


# Define and export the project root directory
PROJECT_ROOT = os.getenv("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
DEFAULT_BASE_DIR = os.path.join(PROJECT_ROOT, "data/synthetic/raw")


# -------------------------------
# Schema Loader
# -------------------------------
def load_schema(stage_name: str):
    """Load schema JSON for a given stage."""
    # Map stage names to schema file names if necessary
    schema_mapping = {
        "stage1_raw_materials": "stage1_raw_materials",
        "stage2_grinding_preheater": "stage2_grinding_preheater",
        "stage3_clinker": "stage3_clinker",
        "stage4_cement_grinding": "stage4_cement_grinding",
        "stage5_packing_dispatch": "stage5_packing_dispatch"
    }
    schema_name = schema_mapping.get(stage_name, stage_name)
    path = os.path.join(SCHEMA_DIR, f"{schema_name}_schema.json")
    print(f"Loading schema for stage: {stage_name}, Path: {path}")  # Debugging log
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema not found for {stage_name}: {path}")
    with open(path, "r") as f:
        return json.load(f)


# -------------------------------
# Single CSV Loader
# -------------------------------
def load_csv(file_path):
    """
    Load a CSV file into a DataFrame with error handling and validation.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded CSV: {file_path}")

        # Ensure the loaded object is a DataFrame
        if isinstance(df, pd.Series):
            raise TypeError(f"Loaded object is a Series, expected a DataFrame: {file_path}")

        # Log DataFrame structure
        logger.debug(f"Loaded DataFrame shape: {df.shape}")
        logger.debug(f"Loaded DataFrame columns: {list(df.columns)}")

        # Debug log to trace data structure
        logger.debug(f"Loaded data structure: {df.dtypes}")

        # Validate DataFrame structure
        if df.empty:
            logger.warning(f"⚠️ Loaded DataFrame is empty: {file_path}")
        elif "timestamp" not in df.columns:
            logger.warning(f"⚠️ 'timestamp' column missing in DataFrame: {file_path}")

        return df
    except Exception as e:
        logger.error(f"Error loading CSV file {file_path}: {e}")
        raise


# -------------------------------
# Schema Validator
# -------------------------------
def validate_schema(df: pd.DataFrame, schema: dict):
    """Validate DataFrame against schema fields."""
    required_cols = [f["name"] for f in schema["fields"]]
    missing = set(required_cols) - set(df.columns)
    if missing:
        print(f"DEBUG: Required columns: {required_cols}")
        print(f"DEBUG: DataFrame columns: {list(df.columns)}")
        return False, f"Missing columns: {missing}"

    # Validate timestamp
    if "timestamp" in df.columns:
        try:
            pd.to_datetime(df["timestamp"])
        except Exception:
            return False, "Timestamp parse error"

    return True, "OK"


# -------------------------------
# Load Stage-wise Synthetic Data
# -------------------------------
def load_stage_data(stage_dir):
    """
    Load all CSV files from a specific stage directory.

    Args:
        stage_dir (str): Path to the stage folder.

    Returns:
        dict: Dictionary with keys as file base names and values as DataFrames.
    """
    datasets = {}
    csv_files = glob.glob(os.path.join(stage_dir, "*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {stage_dir}")

    for file_path in csv_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        datasets[base_name] = load_csv(file_path)

    return datasets


# -------------------------------
# Load All Stages (Latest Run)
# -------------------------------
def load_all_stages(base_dir=DEFAULT_BASE_DIR):
    """
    Load datasets from all stage folders inside the latest timestamp directory.

    Args:
        base_dir (str): Base directory containing timestamped folders.

    Returns:
        dict: Nested dictionary with stage names as keys and DataFrame dicts as values.
              Example: data["stage1_raw_materials"]["stage1_raw_materials"]
    """
    print(f"load_all_stages received base_dir: {base_dir}")
    print("load_all_stages function execution started")
    # Find latest timestamped folder
    timestamp_folders = sorted(glob.glob(os.path.join(base_dir, "*")))
    if not timestamp_folders:
        raise FileNotFoundError(f"No timestamped folders found in {base_dir}")

    latest_folder = timestamp_folders[-1]
    print(f"[INFO] Loading data from latest run: {latest_folder}")

    stage_dirs = [d for d in glob.glob(os.path.join(latest_folder, "stage*")) if os.path.isdir(d)]
    if not stage_dirs:
        logger.warning(f"⚠️ No stage directories found in {latest_folder}. Loading CSV files directly.")
        csv_files = glob.glob(os.path.join(latest_folder, "*.csv"))
        all_data = {}
        for csv_file in csv_files:
            stage_name = os.path.splitext(os.path.basename(csv_file))[0]
            all_data[stage_name] = pd.read_csv(csv_file)
            logger.debug(f"Loaded CSV file: {csv_file}, Rows: {len(all_data[stage_name])}, Columns: {len(all_data[stage_name].columns)}")
            logger.debug(f"DataFrame structure for {stage_name}: {all_data[stage_name].dtypes}")
        return {k: v for k, v in all_data.items() if isinstance(v, pd.DataFrame)}

    all_data = {}
    for stage_dir in stage_dirs:
        stage_name = os.path.basename(stage_dir)
        print(f"[INFO] Loading {stage_name} ...")
        all_data[stage_name] = load_stage_data(stage_dir)

    # Ensure all_data contains only DataFrames
    all_data = {k: v for k, v in all_data.items() if isinstance(v, pd.DataFrame)}

    print(f"All loaded data: {all_data}")
    print(f"load_all_stages output: {all_data}")
    print(f"Final output of load_all_stages: {all_data}")
    print(f"Returning from load_all_stages with data: {all_data}")
    return all_data


# -------------------------------
# Load Scenario-specific Data
# -------------------------------
def load_scenario(base_dir=DEFAULT_BASE_DIR, scenario="normal"):
    """
    Load scenario-specific datasets for all stages.
    Expects files like: stage1_raw_materials_normal.csv, stage2_grinding_preheater_critical.csv, etc.

    Args:
        base_dir (str): Base directory containing timestamped folders.
        scenario (str): Scenario type ("normal", "critical_low", "critical_high").

    Returns:
        dict: Nested dictionary with stage names as keys and DataFrame dicts as values.
    """
    timestamp_folders = sorted(glob.glob(os.path.join(base_dir, "*")))
    if not timestamp_folders:
        raise FileNotFoundError(f"No timestamped folders found in {base_dir}")

    latest_folder = timestamp_folders[-1]
    print(f"[INFO] Loading scenario '{scenario}' from: {latest_folder}")

    stage_dirs = [d for d in glob.glob(os.path.join(latest_folder, "stage*")) if os.path.isdir(d)]
    all_data = {}

    for stage_dir in stage_dirs:
        stage_name = os.path.basename(stage_dir)
        datasets = {}
        csv_files = glob.glob(os.path.join(stage_dir, f"*_{scenario}.csv"))
        if not csv_files:
            print(f"[WARN] No {scenario} files found in {stage_dir}, skipping...")
            continue

        for file_path in csv_files:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            datasets[base_name] = load_csv(file_path)

        if datasets:
            all_data[stage_name] = datasets

    return all_data


# -------------------------------
# Validate DataFrame
# -------------------------------
def validate(df, schema):
    """
    Validate a DataFrame against a given schema.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        schema (dict): Schema dictionary loaded from a JSON file.

    Returns:
        tuple: (bool, str) Validation status and message.
    """
    # Check all required columns exist
    cols = [f['name'] for f in schema['fields']]
    missing = set(cols) - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"

    # Check for totally empty columns
    empty_cols = [col for col in df.columns if df[col].dropna().empty]
    if empty_cols:
        return False, f"Empty columns: {empty_cols}"

    # Try to parse timestamp
    try:
        pd.to_datetime(df['timestamp'])
    except Exception as e:
        return False, "Timestamp parse error"

    return True, "OK"


# -------------------------------
# Load Stage Files
# -------------------------------
def load_stage_files(run_dir: str):
    """
    Load all stage CSV files in run_dir, validate against schema.
    Returns dict {stage_name: DataFrame}.
    """
    files = glob.glob(os.path.join(run_dir, "stage*.csv"))
    datasets = {}

    if not files:
        raise FileNotFoundError(f"No stage CSV files found in {run_dir}")

    # Dynamically load all schemas
    schema_dir = "data/synthetic/schema"
    schema_files = glob.glob(os.path.join(schema_dir, "*_schema.json"))
    schema_mapping = {
        os.path.splitext(os.path.basename(f))[0].replace("_schema", ""): f
        for f in schema_files
    }

    for f in files:
        stage_name = os.path.splitext(os.path.basename(f))[0]
        stage_name = stage_name.split('_default')[0]

        if stage_name not in schema_mapping:
            logger.warning(f"No schema found for stage: {stage_name}. Skipping validation.")
            continue

        schema_path = schema_mapping[stage_name]
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        df = pd.read_csv(f)
        ok, msg = validate_schema(df, schema)
        if not ok:
            logger.warning(f"Validation failed for {stage_name}: {msg}. Proceeding without validation.")

        datasets[stage_name] = df

    return datasets


# Example usage
if __name__ == "__main__":
    schema_path = "data/synthetic/schema/stage1_raw_materials_schema.json"
    csv_path = "data/synthetic/raw/2025-09-17_23-10-01/stage1_raw_materials.csv"

    schema = json.load(open(schema_path))
    df = pd.read_csv(csv_path)

    validation_status, message = validate(df, schema)
    print(validation_status, message)
