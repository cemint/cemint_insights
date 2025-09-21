# Synthetic Data Generation for Cemint Insights

This module is responsible for generating synthetic data for various stages of the cement manufacturing process. The synthetic data is used for testing, experimentation, and validation of the data pipeline and machine learning models.

## Structure

- **`run_all.py`**: Script to generate synthetic data for all stages in one go.
- **`generators/`**: Contains individual scripts for generating synthetic data for each stage:
  - `stage1_raw_materials.py`: Generates data for raw materials.
  - `stage2_grinding_preheater.py`: Generates data for grinding and preheater stages.
  - `stage3_clinker.py`: Generates data for the clinker production stage.
  - `stage4_cement_grinding.py`: Generates data for cement grinding.
  - `stage5_packaging_dispatch.py`: Generates data for packaging and dispatch.

## How to Use

### Generate Data for All Stages
Run the following command to generate synthetic data for all stages:
```bash
python run_all.py
```

### Generate Data for a Specific Stage
Run the corresponding generator script. For example:
```bash
python generators/stage1_raw_materials.py
```

## Dependencies

Ensure the following dependencies are installed:
- `pandas`
- `numpy`
- `faker`

Install them using:
```bash
pip install pandas numpy faker
```

## Example Output

The generated data will be saved in the `data/synthetic/processed/` directory, organized by timestamp.

---

## Adding New Generators

1. Create a new script in the `generators/` folder.
2. Follow the structure of existing generator scripts.
3. Update `run_all.py` to include the new generator.

