# Tests for Cemint Insights

This folder contains unit tests for the Cemint Insights project. The tests ensure the correctness, reliability, and robustness of the various components of the project, including data pipelines, machine learning models, services, and the dashboard.

## Purpose

The purpose of this folder is to:
1. Validate the functionality of individual components.
2. Ensure that changes to the codebase do not introduce regressions.
3. Provide a framework for testing new features and bug fixes.

## Structure

The folder is organized as follows:

- **`test_data_pipeline.py`**: Tests for the data pipeline components, including loaders, transformers, and schema validation.
- **`test_dashboard.py`**: Tests for the dashboard application, ensuring the UI components and app logic work as expected.
- **`test_models.py`**: Tests for machine learning models, including training, evaluation, and inference.
- **`test_services.py`**: Tests for backend services, including APIs and business logic.

## How to Run Tests

To run all tests, navigate to the root of the project and execute the following command:

```bash
pytest tests/
```

To run a specific test file, use:

```bash
pytest tests/test_data_pipeline.py
```

For verbose output, add the `-v` flag:

```bash
pytest -v tests/
```

## Adding New Tests

1. Create a new test file in this folder with the prefix `test_` (e.g., `test_new_feature.py`).
2. Use the `pytest` framework to write your tests.
3. Follow the structure of existing test files for consistency.
4. Run the tests to ensure they pass before submitting your changes.

## Dependencies

Ensure the following dependencies are installed before running the tests:

- `pytest`
- `pytest-mock` (if mocking is required)

Install them using:

```bash
pip install pytest pytest-mock
```

## Example Test

Here is an example of a simple test:

```python
def test_example():
    assert 1 + 1 == 2
```

## Test Cases in `test_data_pipeline.py`

The `test_data_pipeline.py` file specifically contains unit tests for validating the functionality of the data pipeline in the CementAI project. These tests ensure that the data loading, schema validation, and preprocessing steps work as expected across all timestamped folders in the `data/synthetic/raw/` directory.

### 1. **`test_load_stage_files_exists`**
   - **Purpose**: Verifies that all stage files are successfully loaded from each timestamped folder.
   - **Checks**: Ensures that datasets are not empty for any stage directory.

### 2. **`test_validate_schema_stage1`**
   - **Purpose**: Validates the schema of `stage1_raw_materials.csv` against the defined JSON schema.
   - **Checks**: Ensures all required columns are present, types match, and timestamps are parseable.

### 3. **`test_transform_pipeline_outputs_columns`**
   - **Purpose**: Tests the preprocessing pipeline to ensure it produces the expected outputs.
   - **Checks**: Verifies that time-based features and KPIs (e.g., `specific_power_consumption`) are added to the processed DataFrames.

## How to Run the Data Pipeline Tests

1. Ensure that the required dependencies are installed:

   ```bash
   pip install pytest
   ```

2. Set the `PYTHONPATH` to the project root directory:

   ```bash
   export PYTHONPATH=$(pwd)
   ```

3. Run the tests using `pytest`:

   ```bash
   pytest tests/ --maxfail=5 --disable-warnings
   ```

## Use Case for Data Pipeline Tests

These tests are designed to:

- Validate the integrity of raw data files.
- Ensure schema compliance for each stage.
- Verify that preprocessing steps (e.g., feature engineering, scaling, KPI creation) are applied correctly.

By running these tests, you can confidently ensure that the data pipeline is functioning as intended and producing reliable outputs for downstream machine learning tasks.

## Notes

- The tests iterate over all timestamped folders in `data/synthetic/raw/`.
- If any required files are missing, the tests will skip those folders and log appropriate warnings.
- Ensure that the `data/synthetic/raw/` directory contains valid test data before running the tests.