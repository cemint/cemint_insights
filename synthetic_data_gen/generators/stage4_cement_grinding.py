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

class Stage4CementGrindingGenerator:
    """
    Synthetic data generator for Stage 4: Cement Grinding & Blending.

    Simulates:
    - Ball mill / vertical roller mill performance
    - Separator operation
    - Gypsum and additive blending
    - Energy consumption
    - Cement quality indicators
    """

    def __init__(self, seed: int = None, scenario: str = "normal"):
        if seed:
            random.seed(seed)
        self.scenario = scenario

    def generate_record(self, timestamp: datetime.datetime = None):
        if not timestamp:
            timestamp = datetime.datetime.now()

        if self.scenario == "normal":
            record = {
                "timestamp": timestamp.isoformat(),

                # Mill Operation
                "mill_motor_power_kw": round(random.uniform(2500, 4000), 2),
                "mill_outlet_temp_c": round(random.uniform(95, 120), 2),
                "mill_feed_rate_tph": round(random.uniform(120, 180), 2),
                "mill_vibration_mm_s": round(random.uniform(1, 3), 2),

                # Separator
                "separator_speed_rpm": round(random.uniform(900, 1100), 2),
                "separator_efficiency_pct": round(random.uniform(70, 90), 2),
                "separator_motor_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Additives
                "gypsum_feed_rate_tph": round(random.uniform(5, 15), 2),
                "flyash_feed_rate_tph": round(random.uniform(5, 15), 2),
                "slag_feed_rate_tph": round(random.uniform(5, 15), 2),
                "additive_blending_ratio": round(random.uniform(0.1, 0.5), 2),

                # Cement Quality
                "fineness_blaine_cm2_g": round(random.uniform(3000, 4000), 2),
                "residue_45_micron_pct": round(random.uniform(5, 10), 2),
                "cement_temp_c": round(random.uniform(80, 100), 2),

                # Energy
                "specific_power_consumption_kwh_t": round(random.uniform(20, 30), 2),

                # Alarms
                "mill_high_vibration_alarm": random.choice([0, 1]),
                "separator_blockage_alarm": random.choice([0, 1]),
                "mill_overload_alarm": random.choice([0, 1]),
                "separator_efficiency_drop_alarm": random.choice([0, 1]),

                # Additional Fields
                "clinker_feed_tph": round(random.uniform(100, 150), 2),
                "additive_feed_tph": round(random.uniform(10, 20), 2),
                "cement_mill_power_kw": round(random.uniform(300, 500), 2),
                "cement_mill_outlet_temp_c": round(random.uniform(90, 110), 2),
                "cement_strength_3d_mpa": round(random.uniform(20, 30), 2),
                "cement_strength_28d_mpa": round(random.uniform(40, 50), 2),
                "cement_mill_vibration_mm": round(random.uniform(1, 3), 2),
            }
        elif self.scenario == "critical_low":
            record = {
                "timestamp": timestamp.isoformat(),

                # Mill Operation
                "mill_motor_power_kw": round(random.uniform(2000, 2500), 2),
                "mill_outlet_temp_c": round(random.uniform(80, 95), 2),
                "mill_feed_rate_tph": round(random.uniform(100, 120), 2),
                "mill_vibration_mm_s": round(random.uniform(1, 3), 2),

                # Separator
                "separator_speed_rpm": round(random.uniform(700, 900), 2),
                "separator_efficiency_pct": round(random.uniform(50, 70), 2),
                "separator_motor_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Additives
                "gypsum_feed_rate_tph": round(random.uniform(3, 7), 2),
                "flyash_feed_rate_tph": round(random.uniform(3, 7), 2),
                "slag_feed_rate_tph": round(random.uniform(3, 7), 2),
                "additive_blending_ratio": round(random.uniform(0.05, 0.1), 2),

                # Cement Quality
                "fineness_blaine_cm2_g": round(random.uniform(2500, 3000), 2),
                "residue_45_micron_pct": round(random.uniform(10, 15), 2),
                "cement_temp_c": round(random.uniform(70, 80), 2),

                # Energy
                "specific_power_consumption_kwh_t": round(random.uniform(15, 20), 2),

                # Alarms
                "mill_high_vibration_alarm": random.choice([0, 1]),
                "separator_blockage_alarm": random.choice([0, 1]),
                "mill_overload_alarm": random.choice([0, 1]),
                "separator_efficiency_drop_alarm": random.choice([0, 1]),

                # Additional Fields
                "clinker_feed_tph": round(random.uniform(80, 100), 2),
                "additive_feed_tph": round(random.uniform(5, 10), 2),
                "cement_mill_power_kw": round(random.uniform(250, 350), 2),
                "cement_mill_outlet_temp_c": round(random.uniform(85, 95), 2),
                "cement_strength_3d_mpa": round(random.uniform(15, 20), 2),
                "cement_strength_28d_mpa": round(random.uniform(35, 40), 2),
                "cement_mill_vibration_mm": round(random.uniform(1, 3), 2),
            }
        elif self.scenario == "critical_high":
            record = {
                "timestamp": timestamp.isoformat(),

                # Mill Operation
                "mill_motor_power_kw": round(random.uniform(4000, 5000), 2),
                "mill_outlet_temp_c": round(random.uniform(120, 140), 2),
                "mill_feed_rate_tph": round(random.uniform(180, 250), 2),
                "mill_vibration_mm_s": round(random.uniform(3, 5), 2),

                # Separator
                "separator_speed_rpm": round(random.uniform(1100, 1300), 2),
                "separator_efficiency_pct": round(random.uniform(90, 95), 2),
                "separator_motor_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Additives
                "gypsum_feed_rate_tph": round(random.uniform(10, 20), 2),
                "flyash_feed_rate_tph": round(random.uniform(10, 20), 2),
                "slag_feed_rate_tph": round(random.uniform(10, 20), 2),
                "additive_blending_ratio": round(random.uniform(0.4, 0.6), 2),

                # Cement Quality
                "fineness_blaine_cm2_g": round(random.uniform(3500, 4500), 2),
                "residue_45_micron_pct": round(random.uniform(0, 5), 2),
                "cement_temp_c": round(random.uniform(90, 110), 2),

                # Energy
                "specific_power_consumption_kwh_t": round(random.uniform(25, 35), 2),

                # Alarms
                "mill_high_vibration_alarm": random.choice([0, 1]),
                "separator_blockage_alarm": random.choice([0, 1]),
                "mill_overload_alarm": random.choice([0, 1]),
                "separator_efficiency_drop_alarm": random.choice([0, 1]),

                # Additional Fields
                "clinker_feed_tph": round(random.uniform(120, 150), 2),
                "additive_feed_tph": round(random.uniform(15, 25), 2),
                "cement_mill_power_kw": round(random.uniform(400, 600), 2),
                "cement_mill_outlet_temp_c": round(random.uniform(95, 115), 2),
                "cement_strength_3d_mpa": round(random.uniform(25, 35), 2),
                "cement_strength_28d_mpa": round(random.uniform(45, 55), 2),
                "cement_mill_vibration_mm": round(random.uniform(2, 4), 2),
            }
        else:
            raise ValueError("Invalid scenario. Choose from ['normal', 'critical_low', 'critical_high'].")

        return record

    def generate_batch(self, n: int = 10, start_time: datetime.datetime = None, interval_seconds: int = 60):
        validate_inputs(n, interval_seconds)

        if not start_time:
            start_time = datetime.datetime.now()

        batch = []
        for i in range(n):
            ts = start_time + datetime.timedelta(seconds=i * interval_seconds)
            batch.append(self.generate_record(timestamp=ts))

        return batch

if __name__ == "__main__":
    gen = Stage4CementGrindingGenerator(seed=42)
    try:
        data = gen.generate_batch(n=5)
        logging.info(json.dumps(data, indent=2))
    except Exception as e:
        logging.error(f"Error generating Stage 4 data: {e}")
