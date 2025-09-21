import random
import datetime
import json
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_inputs(batch_size, interval_seconds):
    if batch_size <= 0:
        raise ValueError("Batch size must be a positive integer.")

    if interval_seconds <= 0:
        raise ValueError("Interval seconds must be a positive integer.")


class Stage2GrindingPreheaterGenerator:
    """
    Synthetic data generator for Stage 2: Grinding & Preheater in a cement plant.

    This simulates sensor readings and process parameters:
    - Grinding Mills (ball mill/vertical roller mill) data
    - Separator efficiency and particle size distribution
    - Preheater cyclone performance
    - Process gas temperatures and flow rates
    - Energy consumption
    """

    def __init__(self, seed: int = None, scenario: str = "normal"):
        if seed:
            random.seed(seed)
        self.scenario = scenario

    def generate_record(self, timestamp: datetime.datetime = None):
        """
        Generate a single synthetic record for Stage 2.
        """
        if not timestamp:
            timestamp = datetime.datetime.now()

        if self.scenario == "normal":
            record = {
                "timestamp": timestamp.isoformat(),

                # Grinding Mill Parameters
                "mill_power_kw": round(random.uniform(3500, 5000), 2),
                "mill_motor_load_pct": round(random.uniform(70, 95), 2),
                "mill_outlet_temp_c": round(random.uniform(90, 120), 2),
                "mill_feed_rate_tph": round(random.uniform(180, 250), 2),
                "raw_mill_feed_tph": round(random.uniform(150, 250), 2),
                "raw_mill_power_kw": round(random.uniform(300, 500), 2),

                # Separator & Particle Size
                "separator_speed_rpm": round(random.uniform(900, 1100), 2),
                "separator_efficiency_pct": round(random.uniform(70, 90), 2),
                "residue_on_90um_pct": round(random.uniform(5, 15), 2),
                "residue_on_212um_pct": round(random.uniform(1, 5), 2),
                "separator_motor_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Preheater Cyclones
                "preheater_inlet_temp_c": round(random.uniform(300, 400), 2),
                "preheater_outlet_temp_c": round(random.uniform(800, 900), 2),
                "cyclone_pressure_drop_mbar": round(random.uniform(50, 100), 2),
                "preheater_O2_pct": round(random.uniform(2, 5), 2),
                "preheater_CO_pct": round(random.uniform(0.1, 0.5), 2),
                "gas_flow_rate_nm3h": round(random.uniform(10000, 20000), 2),
                "dust_load_mgNm3": round(random.uniform(10, 50), 2),
                "preheater_cyclone_efficiency_pct": round(random.uniform(85, 95), 2),

                # Gas Flow & Composition
                "co2_pct": round(random.uniform(10, 15), 2),
                "co_ppm": round(random.uniform(50, 100), 2),
                "so2_ppm": round(random.uniform(10, 20), 2),
                "no_x_ppm": round(random.uniform(100, 200), 2),

                # Energy & Efficiency
                "specific_power_consumption_kwh_t": round(random.uniform(20, 30), 2),
                "separator_fan_power_kw": round(random.uniform(50, 100), 2),
                "preheater_fan_power_kw": round(random.uniform(100, 200), 2),

                # Alarms / Flags
                "high_temp_alarm": random.choice([0, 1]),
                "high_vibration_alarm": random.choice([0, 1]),
                "separator_blockage_alarm": random.choice([0, 1]),
                "fan_failure_alarm": random.choice([0, 1]),
            }
        elif self.scenario == "critical_low":
            record = {
                "timestamp": timestamp.isoformat(),

                # Grinding Mill Parameters
                "mill_power_kw": round(random.uniform(3000, 3500), 2),
                "mill_motor_load_pct": round(random.uniform(50, 70), 2),
                "mill_outlet_temp_c": round(random.uniform(80, 90), 2),
                "mill_feed_rate_tph": round(random.uniform(100, 150), 2),
                "raw_mill_feed_tph": round(random.uniform(100, 150), 2),
            }
        elif self.scenario == "critical_high":
            record = {
                "timestamp": timestamp.isoformat(),

                # Grinding Mill Parameters
                "mill_power_kw": round(random.uniform(5000, 5500), 2),
                "mill_motor_load_pct": round(random.uniform(95, 110), 2),
                "mill_outlet_temp_c": round(random.uniform(120, 140), 2),
                "mill_feed_rate_tph": round(random.uniform(250, 300), 2),
                "raw_mill_feed_tph": round(random.uniform(250, 300), 2),
            }
        else:
            raise ValueError("Invalid scenario. Choose from ['normal', 'critical_low', 'critical_high'].")

        return record

    def generate_batch(self, n: int = 10, start_time: datetime.datetime = None, interval_seconds: int = 60):
        """
        Generate a batch of synthetic records over time.
        """
        validate_inputs(n, interval_seconds)

        if not start_time:
            start_time = datetime.datetime.now()

        batch = []
        for i in range(n):
            ts = start_time + datetime.timedelta(seconds=i * interval_seconds)
            batch.append(self.generate_record(timestamp=ts))

        return batch


if __name__ == "__main__":
    gen = Stage2GrindingPreheaterGenerator(seed=42)
    try:
        data = gen.generate_batch(n=5)
        logging.info(json.dumps(data, indent=2))
    except Exception as e:
        logging.error(f"Error generating Stage 2 data: {e}")
