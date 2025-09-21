# CementAI Dashboard Module

## Overview

The CementAI Dashboard is a Streamlit-based web interface that visualizes KPIs, plant parameters, and AI-generated recommendations. It integrates with the synthetic data pipeline, ML models, and services API to provide an end-to-end proof-of-concept for autonomous cement plant optimization.

## Directory Structure

```text
src/dashboard/
├── __init__.py
├── app.py          # Main Streamlit dashboard application
└── components.py   # Reusable UI components for displaying KPIs, parameters, recommendations
```

## Key Features

### KPI Visualization

- Displays key performance indicators (KPIs) such as:
  - **SPC** (Specific Power Consumption)
  - **TSR** (Thermal Substitution Rate)
  - **Downtime**
- Helps monitor plant efficiency at a glance.

### Process Parameters Table

- Shows the latest process parameters from each stage of the plant.
- Works with synthetic or real processed datasets.

### AI Recommendations

- Displays actionable recommendations for optimizing processes.
- Pulls suggestions from the FastAPI services module.

### Simulation Controls

- Sidebar allows selecting plant stages (`raw_mill`, `kiln`, `utilities`).
- Trigger simulations for PoC scenarios:
  - **Normal**
  - **Critical**
  - **Extreme**

### PoC Ready

- Works with synthetic data immediately.
- Easily extendable to real-time plant data.

## Components

### `components.py`

- **`display_kpis(kpi_dict: dict)`**: Displays KPIs in a neat column layout.
- **`display_parameters_table(df: pd.DataFrame)`**: Displays process parameters in a table.
- **`display_recommendations(recommendations: dict)`**: Shows AI-generated recommendations for a stage.

## How the Dashboard Works

### Load Processed Data

- Reads processed synthetic data from `data/synthetic/processed/`.
- Uses the latest row to simulate current plant conditions.

### Fetch AI Recommendations

- Calls `/recommend` endpoint of `src/services/api.py`.
- Displays recommendations for the selected plant stage.

### Compute KPIs

- Computes KPIs from the latest processed data for PoC demonstration.

### Visualization

- KPIs, parameter tables, and recommendations are displayed dynamically using Streamlit.

## Usage Examples

### 1. Start the Services API

Run the API server locally:

```bash
uvicorn src.services.api:app --reload
```

- Endpoint available at: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

### 2. Start the Dashboard

Run the Streamlit dashboard:

```bash
streamlit run src/dashboard/app.py
```

- Dashboard accessible in your browser (default: `http://localhost:8501`).

### 3. Simulation Controls

Use the sidebar to select the plant stage:

- `raw_mill`
- `kiln`
- `utilities`

Click **Run Simulation** to:

- Display process parameters.
- Display KPIs.
- Fetch AI recommendations.

## Example Workflow

1. Generate synthetic plant data using `synthetic_data_gen`.
2. Run data pipelines to process raw data.
3. Start services API for predictions and recommendations.
4. Launch the dashboard to visualize results.

## Integration Notes

- **Modular Design**: Components are reusable and follow SOLID principles.
- **Real-time Ready**: Can be connected to live plant data instead of synthetic datasets.
- **PoC Flexibility**: Supports multiple scenarios (`normal`, `critical`, `extreme`) to simulate various operational conditions.
- **Extensible**: Can incorporate ML/Generative AI models for advanced recommendations.

## Dependencies

- **Python** >= 3.9
- **Streamlit**: `pip install streamlit`
- **Pandas**: `pip install pandas`
- **Requests**: `pip install requests`

## Next Steps

- Connect the dashboard to real plant data.
- Include time-series visualizations for historical trends.
- Extend the recommendation engine with advanced ML/Generative AI models.
- Automate data refresh using scheduled triggers or event-driven updates