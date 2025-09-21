import os
import pytest
from src.data_pipeline.loaders import load_stage_data as load_stage_files, validate
from src.data_pipeline.pipelines import get_preprocessed_data

def test_load_stage_files_exists():
    base_dir = "data/synthetic/raw"
    timestamp_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for timestamp_dir in timestamp_dirs:
        stage_dir = os.path.join(base_dir, timestamp_dir)
        datasets = load_stage_files(stage_dir)
        assert len(datasets) > 0, f"No datasets loaded from stage directory: {stage_dir}"

def test_validate_schema_stage1():
    import json
    import pandas as pd
    base_dir = "data/synthetic/raw"
    schema_path = "data/synthetic/schema/stage1_raw_materials_schema.json"

    timestamp_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for timestamp_dir in timestamp_dirs:
        csv_path = os.path.join(base_dir, timestamp_dir, "stage1_raw_materials.csv")
        if not os.path.exists(csv_path):
            continue

        schema = json.load(open(schema_path))
        df = pd.read_csv(csv_path)

        is_valid, message = validate(df, schema)
        assert is_valid, f"Validation failed for {csv_path}: {message}"

def test_transform_pipeline_outputs_columns():
    base_dir = "data/synthetic/raw"
    timestamp_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for timestamp_dir in timestamp_dirs:
        data_dir = os.path.join(base_dir, timestamp_dir)
        preprocessed_data = get_preprocessed_data(data_dir)

        for stage, df in preprocessed_data.items():
            assert "timestamp" in df.columns, f"Timestamp column missing in {stage}"
            assert "specific_power_consumption" in df.columns, f"KPI column missing in {stage}"

def test_verify_all_stages():
    base_dir = "data/synthetic/raw"
    if not os.path.exists(base_dir):
        pytest.fail(f"Base directory does not exist: {base_dir}")

    timestamp_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not timestamp_dirs:
        pytest.fail(f"No timestamped directories found in {base_dir}")

    for data_dir in timestamp_dirs:
        try:
            preprocessed_data = get_preprocessed_data(data_dir)
        except Exception as e:
            pytest.fail(f"Error processing data in {data_dir}: {e}")

        for stage, df in preprocessed_data.items():
            # Verify that the DataFrame is not empty
            assert not df.empty, f"DataFrame for {stage} in {data_dir} is empty."

            # Verify that all expected columns are present
            expected_columns = {"timestamp", "hour", "day", "weekday", "month", "specific_power_consumption"}
            missing_columns = expected_columns - set(df.columns)
            assert not missing_columns, f"Missing columns {missing_columns} in {stage} for {data_dir}."

            # Verify that there are no missing values in critical columns
            critical_columns = {"timestamp", "specific_power_consumption"} & set(df.columns)
            for col in critical_columns:
                assert df[col].notnull().all(), f"Missing values found in column {col} for {stage} in {data_dir}."

            # Verify that timestamps are monotonic
            if "timestamp" in df.columns:
                assert df["timestamp"].is_monotonic_increasing, f"Timestamps are not monotonic in {stage} for {data_dir}."

            # Verify that numeric columns are within expected ranges (if applicable)
            numeric_columns = df.select_dtypes(include=["number"]).columns
            for col in numeric_columns:
                assert (df[col] >= 0).all(), f"Negative values found in column {col} for {stage} in {data_dir}."

def test_verify_transformers_and_scripts():
    base_dir = "data/synthetic/raw"
    if not os.path.exists(base_dir):
        pytest.fail(f"Base directory does not exist: {base_dir}")

    timestamp_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not timestamp_dirs:
        pytest.fail(f"No timestamped directories found in {base_dir}")

    for data_dir in timestamp_dirs:
        try:
            preprocessed_data = get_preprocessed_data(data_dir)
        except Exception as e:
            pytest.fail(f"Error processing data in {data_dir}: {e}")

        for stage, df in preprocessed_data.items():
            # Verify that the DataFrame is not empty
            assert not df.empty, f"DataFrame for {stage} in {data_dir} is empty."

            # Verify that all expected columns are present
            expected_columns = {"timestamp", "hour", "day", "weekday", "month", "specific_power_consumption"}
            missing_columns = expected_columns - set(df.columns)
            assert not missing_columns, f"Missing columns {missing_columns} in {stage} for {data_dir}."

            # Verify that transformers are applied correctly
            assert "hour" in df.columns and df["hour"].between(0, 23).all(), f"Invalid hour values in {stage} for {data_dir}."
            assert "specific_power_consumption" in df.columns and (df["specific_power_consumption"] >= 0).all(), f"Invalid KPI values in {stage} for {data_dir}."

            # Verify that numeric columns are scaled (if applicable)
            numeric_columns = df.select_dtypes(include=["number"]).columns
            for col in numeric_columns:
                assert (df[col] >= 0).all(), f"Negative values found in column {col} for {stage} in {data_dir}."

            # Verify that timestamps are monotonic
            if "timestamp" in df.columns:
                assert df["timestamp"].is_monotonic_increasing, f"Timestamps are not monotonic in {stage} for {data_dir}."