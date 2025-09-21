import argparse
import os
import datetime
import pandas as pd
import logging

from generators.stage1_raw_materials import generate_stage1_raw_materials as Stage1RawMaterialsGenerator
from generators.stage2_grinding_preheater import Stage2GrindingPreheaterGenerator
from generators.stage3_clinker import Stage3ClinkerGenerator
from generators.stage4_cement_grinding import Stage4CementGrindingGenerator
from generators.stage5_packaging_dispatch import Stage5StoragePackingGenerator

BASE_OUTPUT_DIR = os.path.join("data", "synthetic", "raw")


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_to_csv(data, filename, run_dir):
    """Save list of dicts to CSV inside timestamped folder."""
    df = pd.DataFrame(data)
    os.makedirs(run_dir, exist_ok=True)
    file_path = os.path.join(run_dir, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
    df.to_csv(file_path, index=False)
    print(f"✅ Saved {len(df)} rows -> {file_path}")


def validate_inputs(rows, interval, start_date):
    if rows <= 0:
        raise ValueError("Rows must be a positive integer.")

    if interval <= 0:
        raise ValueError("Interval must be a positive integer.")

    try:
        datetime.datetime.fromisoformat(start_date)
    except ValueError:
        raise ValueError("Invalid start_date format. Use ISO format (e.g., 2025-01-01T00:00:00).")


def generate_stage_data(generator_class, stage_name, args, run_dir):
    """Run one stage generator and save CSV."""
    try:
        print(f"⚙️ Generating data for {stage_name}...")

        if stage_name == "Stage1_Raw_Materials":
            # Call the function directly for Stage 1
            generator_class(
                start_date=args.start_date.strftime("%Y-%m-%d"),
                duration_days=args.rows // (24 * 60 // args.interval),
                interval_minutes=args.interval,
                scenario=args.scenario,
                output_dir=run_dir
            )
        else:
            gen = generator_class(seed=42)
            batch = gen.generate_batch(
                n=args.rows,
                start_time=args.start_date,
                interval_seconds=args.interval
            )

            # Ensure files are saved directly under data/synthetic/raw/<timestamp>/
            output_file = os.path.join(run_dir, f"{stage_name.lower()}_data_{args.start_date.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
            save_to_csv(batch, os.path.basename(output_file), run_dir)
    except Exception as e:
        print(f"❌ Error generating data for {stage_name}: {e}")


def run_all_stages(scenario="normal"):
    """Run all stages with the given scenario."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = os.path.join(BASE_OUTPUT_DIR, timestamp)

    # Stage 1
    Stage1RawMaterialsGenerator(
        start_date="2025-01-01",
        duration_days=7,
        interval_minutes=10,
        scenario=scenario,
        output_dir=run_dir
    )

    # Stage 2
    stage2_gen = Stage2GrindingPreheaterGenerator()
    stage2_data = [stage2_gen.generate_record() for _ in range(100)]
    save_to_csv(stage2_data, "stage2_grinding_preheater.csv", run_dir)

    # Stage 3
    stage3_gen = Stage3ClinkerGenerator()
    stage3_data = [stage3_gen.generate_record() for _ in range(100)]
    save_to_csv(stage3_data, "stage3_clinker.csv", run_dir)

    # Stage 4
    stage4_gen = Stage4CementGrindingGenerator()
    stage4_data = [stage4_gen.generate_record() for _ in range(100)]
    save_to_csv(stage4_data, "stage4_cement_grinding.csv", run_dir)

    # Stage 5
    stage5_gen = Stage5StoragePackingGenerator()
    stage5_data = [stage5_gen.generate_record() for _ in range(100)]
    save_to_csv(stage5_data, "stage5_packaging_dispatch.csv", run_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Run all synthetic data generators for cement manufacturing stages.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-r", "--rows", type=int, default=60,
        help="Number of rows/records to generate (e.g., 60 for 60 samples)."
    )
    parser.add_argument(
        "-i", "--interval", type=int, default=60,
        help="Interval in seconds between records."
    )
    parser.add_argument(
        "-s", "--start-date", type=str, default=datetime.datetime.now().isoformat(),
        help="Start date in ISO format (e.g., 2025-01-01T00:00:00)."
    )
    parser.add_argument(
        "--scenario", type=str, default="normal",
        help="Scenario name for the data generation (e.g., 'normal', 'stress_test')."
    )

    args = parser.parse_args()

    try:
        validate_inputs(args.rows, args.interval, args.start_date)
        args.start_date = datetime.datetime.fromisoformat(args.start_date)

        # Create a timestamped output directory inside data/synthetic
        run_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_dir = os.path.join("data/synthetic", run_id)

        print(f"\n🚀 Starting synthetic data generation")
        print(f"📂 Output directory: {run_dir}")
        print(f"📊 Rows: {args.rows}, Interval: {args.interval}s, Start Date: {args.start_date}, Scenario: {args.scenario}\n")

        stages = [
            ("Stage1_Raw_Materials", Stage1RawMaterialsGenerator),
            ("Stage2_Grinding_Preheater", Stage2GrindingPreheaterGenerator),
            ("Stage3_Clinker", Stage3ClinkerGenerator),
            ("Stage4_Cement_Grinding", Stage4CementGrindingGenerator),
            ("Stage5_Storage_Packing", Stage5StoragePackingGenerator),
        ]

        for stage_name, generator_class in stages:
            generate_stage_data(generator_class, stage_name, args, run_dir)

        print("\n✅ Synthetic dataset generation completed for all stages!")
    except Exception as e:
        print(f"❌ Error in main execution: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all synthetic data generators.")
    parser.add_argument("--scenario", type=str, default="normal", choices=["normal", "critical_low", "critical_high"],
                        help="Scenario type: normal, critical_low, critical_high")
    args = parser.parse_args()

    run_all_stages(scenario=args.scenario)
