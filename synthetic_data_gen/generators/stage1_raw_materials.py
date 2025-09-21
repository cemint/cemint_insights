"""
Stage 1 Synthetic Data Generator: Raw Materials
------------------------------------------------
This script generates synthetic sensor/process data for the
Raw Materials stage in cement manufacturing.

It mimics limestone/clay/iron ore extraction, blending,
and pre-processing before grinding.

Author: CEMint AI Hackathon Team
"""

import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_inputs(start_date, duration_days, interval_minutes):
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid start_date format. Use 'YYYY-MM-DD'.")

    if duration_days <= 0:
        raise ValueError("duration_days must be a positive integer.")

    if interval_minutes <= 0:
        raise ValueError("interval_minutes must be a positive integer.")


def generate_stage1_raw_materials(start_date: str,
                                  duration_days: int,
                                  interval_minutes: int,
                                  scenario: str,
                                  output_dir: str):
    """
    Generate synthetic raw materials data for Stage 1.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        duration_days (int): Number of days to simulate.
        interval_minutes (int): Interval between samples in minutes.
        scenario (str): One of ["normal", "critical_low", "critical_high"].
        output_dir (str): Directory to save the generated CSV.
    """
    validate_inputs(start_date, duration_days, interval_minutes)

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = start_datetime + timedelta(days=duration_days)

    timestamps = pd.date_range(start=start_datetime, end=end_datetime, freq=f"{interval_minutes}T")

    if scenario == "normal":
        data = {
            "timestamp": timestamps,
            "limestone_feed_tph": np.random.normal(150, 10, len(timestamps)),
            "clay_feed_tph": np.random.normal(75, 5, len(timestamps)),
            "iron_ore_feed_tph": np.random.normal(15, 2, len(timestamps)),
            "gypsum_feed_tph": np.random.normal(10, 1, len(timestamps)),
            "laterite_feed_tph": np.random.normal(7, 1, len(timestamps)),
            "limestone_moisture_pct": np.random.normal(3, 0.5, len(timestamps)),
            "clay_moisture_pct": np.random.normal(3, 0.5, len(timestamps)),
            "avg_particle_size_mm": np.random.normal(1.2, 0.2, len(timestamps)),
            "CaO_pct": np.random.normal(45, 2, len(timestamps)),
            "SiO2_pct": np.random.normal(15, 1, len(timestamps)),
            "Al2O3_pct": np.random.normal(7, 1, len(timestamps)),
            "Fe2O3_pct": np.random.normal(3, 0.5, len(timestamps)),
            "MgO_pct": np.random.normal(1, 0.2, len(timestamps)),
            "crusher_power_kw": np.random.normal(75, 5, len(timestamps)),
            "conveyor_speed_mps": np.random.normal(2, 0.2, len(timestamps)),
            "CO2_emission_kgph": np.random.normal(150, 10, len(timestamps)),
            "dust_concentration_mgpm3": np.random.normal(30, 5, len(timestamps)),
            "crusher_status": np.random.choice([0, 1], len(timestamps), p=[0.1, 0.9]),
            "energy_consumption_kwh": np.random.normal(750, 50, len(timestamps)),
            "moisture_content_pct": np.random.normal(3, 0.5, len(timestamps))
        }
    elif scenario == "critical_low":
        data = {
            "timestamp": timestamps,
            "limestone_feed_tph": np.random.normal(100, 5, len(timestamps)),
            "clay_feed_tph": np.random.normal(50, 3, len(timestamps)),
            "iron_ore_feed_tph": np.random.normal(10, 1, len(timestamps)),
            "gypsum_feed_tph": np.random.normal(5, 0.5, len(timestamps)),
            "laterite_feed_tph": np.random.normal(3, 0.5, len(timestamps)),
            "limestone_moisture_pct": np.random.normal(1, 0.2, len(timestamps)),
            "clay_moisture_pct": np.random.normal(1, 0.2, len(timestamps)),
            "avg_particle_size_mm": np.random.normal(0.8, 0.1, len(timestamps)),
            "CaO_pct": np.random.normal(40, 1, len(timestamps)),
            "SiO2_pct": np.random.normal(12, 0.5, len(timestamps)),
            "Al2O3_pct": np.random.normal(5, 0.5, len(timestamps)),
            "Fe2O3_pct": np.random.normal(2, 0.2, len(timestamps)),
            "MgO_pct": np.random.normal(0.8, 0.1, len(timestamps)),
            "crusher_power_kw": np.random.normal(50, 3, len(timestamps)),
            "conveyor_speed_mps": np.random.normal(1.5, 0.1, len(timestamps)),
            "CO2_emission_kgph": np.random.normal(100, 5, len(timestamps)),
            "dust_concentration_mgpm3": np.random.normal(20, 3, len(timestamps)),
            "crusher_status": np.random.choice([0, 1], len(timestamps), p=[0.3, 0.7]),
            "energy_consumption_kwh": np.random.normal(500, 30, len(timestamps)),
            "moisture_content_pct": np.random.normal(1, 0.2, len(timestamps))
        }
    elif scenario == "critical_high":
        data = {
            "timestamp": timestamps,
            "limestone_feed_tph": np.random.normal(200, 15, len(timestamps)),
            "clay_feed_tph": np.random.normal(100, 10, len(timestamps)),
            "iron_ore_feed_tph": np.random.normal(20, 2, len(timestamps)),
            "gypsum_feed_tph": np.random.normal(15, 2, len(timestamps)),
            "laterite_feed_tph": np.random.normal(10, 1, len(timestamps)),
            "limestone_moisture_pct": np.random.normal(5, 0.5, len(timestamps)),
            "clay_moisture_pct": np.random.normal(5, 0.5, len(timestamps)),
            "avg_particle_size_mm": np.random.normal(1.5, 0.2, len(timestamps)),
            "CaO_pct": np.random.normal(50, 3, len(timestamps)),
            "SiO2_pct": np.random.normal(18, 1, len(timestamps)),
            "Al2O3_pct": np.random.normal(10, 1, len(timestamps)),
            "Fe2O3_pct": np.random.normal(5, 0.5, len(timestamps)),
            "MgO_pct": np.random.normal(2, 0.2, len(timestamps)),
            "crusher_power_kw": np.random.normal(100, 10, len(timestamps)),
            "conveyor_speed_mps": np.random.normal(3, 0.2, len(timestamps)),
            "CO2_emission_kgph": np.random.normal(200, 15, len(timestamps)),
            "dust_concentration_mgpm3": np.random.normal(50, 5, len(timestamps)),
            "crusher_status": np.random.choice([0, 1], len(timestamps), p=[0.05, 0.95]),
            "energy_consumption_kwh": np.random.normal(1000, 70, len(timestamps)),
            "moisture_content_pct": np.random.normal(5, 0.5, len(timestamps))
        }
    else:
        raise ValueError("Invalid scenario. Choose from ['normal', 'critical_low', 'critical_high'].")

    df = pd.DataFrame(data)

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "stage1_raw_materials.csv")
    df.to_csv(output_file, index=False)
    logging.info(f"Stage 1 data saved to {output_file}")


def parse_args():
    parser = argparse.ArgumentParser(description="Stage 1 Raw Materials Data Generator")
    parser.add_argument("--start_date", type=str, default="2025-01-01",
                        help="Start date in YYYY-MM-DD format")
    parser.add_argument("--duration_days", type=int, default=7,
                        help="Number of days to simulate")
    parser.add_argument("--interval_minutes", type=int, default=10,
                        help="Interval between samples in minutes")
    parser.add_argument("--scenario", type=str, default="normal",
                        choices=["normal", "critical_low", "critical_high"],
                        help="Scenario type: normal, critical_low, critical_high")
    parser.add_argument("--output_dir", type=str, default="data/synthetic/raw",
                        help="Directory to save generated CSV")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        generate_stage1_raw_materials(
            start_date=args.start_date,
            duration_days=args.duration_days,
            interval_minutes=args.interval_minutes,
            scenario=args.scenario,
            output_dir=args.output_dir
        )
    except Exception as e:
        logging.error(f"Error generating Stage 1 data: {e}")
