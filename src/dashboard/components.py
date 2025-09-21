"""
src/dashboard/app.py
-------------------

Streamlit-based dashboard for CementAI PoC.
Visualizes KPIs, process parameters, and recommendations.
"""

import streamlit as st
import pandas as pd
from src.dashboard.components import display_kpis, display_parameters_table, display_recommendations
import requests

# -------------------------------
# Configuration
# -------------------------------
API_URL = "http://127.0.0.1:8000"  # FastAPI services endpoint

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("CementAI Dashboard - PoC")

# -------------------------------
# Sidebar for User Inputs
# -------------------------------
st.sidebar.header("Simulation Controls")
stage = st.sidebar.selectbox("Select Plant Stage", ["raw_mill", "kiln", "utilities"])
run_simulation = st.sidebar.button("Run Simulation")

# -------------------------------
# Display Logic
# -------------------------------
if run_simulation:
    # Example: Load latest processed data
    try:
        df_params = pd.read_csv("data/synthetic/processed/raw_mill_processed.csv")  # Replace dynamically per stage
    except FileNotFoundError:
        st.error("Processed data not found. Run synthetic data generator first.")
        df_params = pd.DataFrame()

    if not df_params.empty:
        display_parameters_table(df_params.head(5))  # Show top 5 rows

        # Get recommendations from services API
        latest_row = df_params.iloc[-1].to_dict()  # Latest parameter row
        response = requests.post(f"{API_URL}/recommend", json={"stage": stage, "parameters": latest_row})
        if response.status_code == 200:
            recommendations = {stage: response.json().get("recommendation")}
            display_recommendations(recommendations)
        else:
            st.error("Failed to fetch recommendations from API.")

        # Example KPIs (for PoC, compute from synthetic data)
        kpi_dict = {
            "SPC": round(df_params.get("spc", pd.Series([85])).mean(), 2),
            "TSR": round(df_params.get("tsr", pd.Series([12])).mean(), 2),
            "Downtime": round(df_params.get("downtime", pd.Series([3])).mean(), 2)
        }
        display_kpis(kpi_dict)
