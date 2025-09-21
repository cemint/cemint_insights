"""
src/data_pipeline/transformers.py
---------------------------------

Module for transforming synthetic cement plant datasets.
Includes feature engineering, normalization, missing-value handling, 
and anomaly detection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import logging

# -------------------------------
# Logger Setup
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# -------------------------------
# Add Time-based Features
# -------------------------------
def add_time_features(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """
    Add useful time-based features for ML modeling.

    Args:
        df (pd.DataFrame): Input DataFrame
        timestamp_col (str): Name of the timestamp column

    Returns:
        pd.DataFrame: DataFrame with added time features
    """
    if timestamp_col not in df.columns:
        raise KeyError(f"⛔ {timestamp_col} column not found in DataFrame")

    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors="coerce")

    if df[timestamp_col].isnull().any():
        logger.warning(f"⚠️ Some rows have invalid timestamps in column '{timestamp_col}'")

    df["hour"] = df[timestamp_col].dt.hour
    df["day"] = df[timestamp_col].dt.day
    df["weekday"] = df[timestamp_col].dt.weekday
    df["month"] = df[timestamp_col].dt.month

    logger.info("⏰ Time features added: [hour, day, weekday, month]")
    return df


# -------------------------------
# Validate and Add Time-based Features
# -------------------------------
def validate_and_add_time_features(df: pd.DataFrame, stage: str, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """
    Validate schema and add time-based features to the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        stage (str): Stage name for schema validation
        timestamp_col (str): Name of the timestamp column

    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    from src.data_pipeline.pipelines import validate_schema

    # Validate schema
    validate_schema(df, stage)

    # Add time features
    return add_time_features(df, timestamp_col)


# -------------------------------
# Normalize Numeric Features
# -------------------------------
def normalize_features(df: pd.DataFrame, method: str = "minmax"):
    """
    Normalize numeric features for ML models.

    Args:
        df (pd.DataFrame): Input DataFrame
        method (str): "minmax" or "standard"

    Returns:
        tuple: (DataFrame with normalized numeric columns, fitted scaler)
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        raise ValueError("⛔ No numeric columns found for normalization")

    if method == "minmax":
        scaler = MinMaxScaler()
    elif method == "standard":
        scaler = StandardScaler()
    else:
        raise ValueError("Unsupported normalization method: choose 'minmax' or 'standard'")

    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    logger.info(f"📊 Normalization applied using method='{method}' on {len(numeric_cols)} numeric columns")

    return df, scaler


# -------------------------------
# Handle Missing Values
# -------------------------------
def fill_missing_values(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
    """
    Fill missing values in numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame
        method (str): "mean", "median", or "zero"

    Returns:
        pd.DataFrame: DataFrame with missing values filled
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        logger.warning("⚠️ No numeric columns found for missing-value handling")
        return df

    if method == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif method == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif method == "zero":
        df[numeric_cols] = df[numeric_cols].fillna(0)
    else:
        raise ValueError("Unsupported fill method: choose 'mean', 'median', or 'zero'")

    logger.info(f"🧹 Missing values handled using method='{method}'")
    return df


# -------------------------------
# Detect Anomalies
# -------------------------------
def detect_anomalies(df: pd.DataFrame, threshold: float = 3) -> pd.DataFrame:
    """
    Detect anomalies using z-score for numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame
        threshold (float): z-score threshold to classify as anomaly

    Returns:
        pd.DataFrame: DataFrame with boolean 'is_anomaly' column
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        logger.warning("⚠️ No numeric columns found for anomaly detection")
        df["is_anomaly"] = False
        return df

    z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
    df["is_anomaly"] = (z_scores > threshold).any(axis=1)

    anomaly_count = df["is_anomaly"].sum()
    logger.info(f"🚨 Anomaly detection complete. Found {anomaly_count} anomalies (threshold={threshold})")

    return df


# -------------------------------
# Clip Outliers
# -------------------------------
def clip_outliers(df: pd.DataFrame, columns: list, lower_percentile: float = 1, upper_percentile: float = 99) -> pd.DataFrame:
    """
    Clip outliers in specified columns.

    Args:
        df (pd.DataFrame): Input DataFrame
        columns (list): List of columns to clip
        lower_percentile (float): Lower percentile for clipping
        upper_percentile (float): Upper percentile for clipping

    Returns:
        pd.DataFrame: DataFrame with outliers clipped
    """
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            logger.warning(f"⚠️ {col} not found in DataFrame columns")
            continue

        lower_bound = np.percentile(df[col].dropna(), lower_percentile)
        upper_bound = np.percentile(df[col].dropna(), upper_percentile)
        df[col] = np.clip(df[col], lower_bound, upper_bound)

    logger.info(f"✂️ Outliers clipped in columns: {columns}")
    return df


# -------------------------------
# Scale Features
# -------------------------------
def scale_features(df: pd.DataFrame, columns: list, method: str = "minmax") -> pd.DataFrame:
    """
    Scale numeric features using MinMaxScaler or StandardScaler.

    Args:
        df (pd.DataFrame): Input DataFrame
        columns (list): List of columns to scale
        method (str): Scaling method ("minmax" or "standard")

    Returns:
        pd.DataFrame: DataFrame with scaled features
    """
    df = df.copy()

    if method == "minmax":
        scaler = MinMaxScaler()
    elif method == "standard":
        scaler = StandardScaler()
    else:
        raise ValueError("Unsupported scaling method: choose 'minmax' or 'standard'")

    df[columns] = scaler.fit_transform(df[columns])
    logger.info(f"📏 Features scaled using method='{method}' on columns: {columns}")

    return df


# -------------------------------
# Create KPIs
# -------------------------------
def create_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived KPIs (Key Performance Indicators).

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: DataFrame with added KPI columns
    """
    df = df.copy()

    if 'mill_power_kwh' in df.columns and 'throughput_tph' in df.columns:
        df['specific_power_consumption'] = df['mill_power_kwh'] / df['throughput_tph']
        logger.info("📊 KPI 'specific_power_consumption' created")
    else:
        logger.warning("⚠️ Required columns for KPI calculation are missing")

    return df


# -------------------------------
# Full Transformation Pipeline
# -------------------------------
def transform_pipeline(
    df: pd.DataFrame,
    normalize_method: str = "minmax",
    fill_method: str = "mean",
    timestamp_col: str = "timestamp",
    anomaly_threshold: float = 3,
    clip_columns: list = None,
    scale_columns: list = None
) -> pd.DataFrame:
    """
    Apply full preprocessing pipeline to a DataFrame.

    Steps:
    1. Fill missing values
    2. Add time features
    3. Normalize numeric columns
    4. Detect anomalies
    5. Clip outliers
    6. Scale features
    7. Create KPIs

    Args:
        df (pd.DataFrame): Input DataFrame
        normalize_method (str): Normalization method ("minmax" or "standard")
        fill_method (str): Missing value fill method ("mean", "median", "zero")
        timestamp_col (str): Name of timestamp column
        anomaly_threshold (float): z-score threshold for anomaly detection

    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input to transform_pipeline must be a DataFrame")

    logger.info("🚀 Starting transformation pipeline...")

    # Fill missing values
    df = fill_missing_values(df, method=fill_method)

    # Add time features
    df = add_time_features(df, timestamp_col=timestamp_col)

    # Normalize numeric features
    df, _ = normalize_features(df, method=normalize_method)

    # Detect anomalies
    df = detect_anomalies(df, threshold=anomaly_threshold)

    # Clip outliers
    if clip_columns:
        df = clip_outliers(df, columns=clip_columns)

    # Scale features
    if scale_columns:
        df = scale_features(df, columns=scale_columns, method=normalize_method)

    # Create KPIs
    df = create_kpis(df)

    logger.info("✅ Transformation pipeline completed successfully")
    return df
