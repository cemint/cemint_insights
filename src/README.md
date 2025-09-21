# Cemint Insights Source Code

This folder contains the core source code for the Cemint Insights project. The code is organized into modular components to ensure scalability, maintainability, and ease of integration.

## Structure

- **`cloud_functions/`**: Contains serverless functions for handling specific tasks in the cloud.
  - **`stage1-power-alert-handler/`**: Handles power alert notifications.
    - `main.py`: Entry point for the function.
    - `requirements.txt`: Dependencies for the function.
  - **`vertex-ai-stage1-power-prediction-invoker/`**: Invokes Vertex AI for power prediction.
    - `main.py`: Entry point for the function.
    - `requirements.txt`: Dependencies for the function.
  - **`vertex-at-stage1-power-prediction-invoker-XAI/`**: Invokes Vertex AI with explainability features.
    - `main.py`: Entry point for the function.
    - `requirements.txt`: Dependencies for the function.

- **`dashboard/`**: Code for the web-based dashboard to visualize insights.
  - `app.py`: Main dashboard application.
  - `components.py`: Reusable UI components.

- **`data_pipeline/`**: Handles data ingestion, transformation, and schema validation.
  - `loaders.py`: Load raw data into the pipeline.
  - `pipelines.py`: Define data processing pipelines.
  - `schemas.py`: Schema validation for raw data.
  - `transformers.py`: Data transformation logic.

- **`firebase/`**: Contains Firebase backend configuration and functions.
  - **`backend/`**: Firebase backend configuration.
    - `firebase.json`: Firebase project configuration.
  - **`functions/`**: Firebase functions for backend logic.
    - `index.js`: Entry point for Firebase functions.
    - `package.json`: Dependencies for Firebase functions.

- **`models/`**: Machine learning models for training, evaluation, and inference.
  - `training.py`: Train predictive models.
  - `evaluation.py`: Evaluate model performance.
  - `inference.py`: Perform predictions using trained models.
  - `registry.py`: Manage model versions and metadata.

- **`services/`**: Backend services and APIs.
  - `api.py`: RESTful API for interacting with the system.
  - `controllers.py`: Business logic for API endpoints.
  - `recommender.py`: Recommendation engine for optimization.

## How to Use

### Running the Dashboard
To start the dashboard, run the following command:
```bash
python dashboard/app.py
```

### Running the Data Pipeline
To process raw data, use the pipeline scripts in the `data_pipeline/` folder. For example:
```bash
python data_pipeline/pipelines.py
```

### Training Models
To train machine learning models, run:
```bash
python models/training.py
```

### Running Services
To start the backend services, run:
```bash
python services/api.py
```

## Dependencies

Ensure the following dependencies are installed:
- `pandas`
- `numpy`
- `flask`
- `dash`
- `scikit-learn`
- `tensorflow`
- `firebase-admin`

Install them using:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.