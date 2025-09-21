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


class Stage5StoragePackingGenerator:
    """
    Synthetic data generator for Stage 5: Storage, Packing & Dispatch.

    Simulates:
    - Silo storage conditions
    - Packing plant performance
    - Bulk loading and bagging
    - Inventory and logistics
    - Alarms and anomalies
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

                # Storage Silos
                "silo_level_pct": round(random.uniform(40, 95), 2),
                "silo_pressure_mbar": round(random.uniform(50, 120), 2),
                "silo_temp_c": round(random.uniform(40, 60), 2),
                "aeration_airflow_nm3_hr": round(random.uniform(3000, 5000), 2),
                "silo_pressure_pa": round(random.uniform(5000, 10000), 2),

                # Packing Plant
                "packing_machine_speed_bags_min": round(random.uniform(80, 120), 2),
                "packing_machine_efficiency_pct": round(random.uniform(85, 95), 2),
                "packing_machine_power_kw": round(random.uniform(50, 100), 2),
                "bag_weight_kg": round(random.uniform(50, 55), 2),
                "bag_reject_rate_pct": round(random.uniform(1, 5), 2),
                "rejected_bags_count": random.randint(0, 10),
                "packing_machine_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Bulk Loading
                "bulk_loading_rate_tph": round(random.uniform(100, 200), 2),
                "truck_loading_time_min": round(random.uniform(10, 20), 2),
                "inventory_turnover_rate": round(random.uniform(1, 5), 2),

                # Dispatch & Inventory
                "daily_dispatch_tonnes": round(random.uniform(1000, 2000), 2),
                "dispatch_rate_tph": round(random.uniform(100, 200), 2),
                "inventory_level_tonnes": round(random.uniform(500, 1000), 2),
                "customer_complaints_count": random.randint(0, 5),

                # Alarms
                "silo_overpressure_alarm": random.choice([0, 1]),
                "packing_machine_jam_alarm": random.choice([0, 1]),
                "truck_delay_alarm": random.choice([0, 1]),

                # Emissions
                "dust_emission_mgNm3": round(random.uniform(10, 50), 2),
            }
        elif self.scenario == "critical_low":
            record = {
                "timestamp": timestamp.isoformat(),

                # Storage Silos
                "silo_level_pct": round(random.uniform(20, 40), 2),
                "silo_pressure_mbar": round(random.uniform(30, 50), 2),
                "silo_temp_c": round(random.uniform(30, 40), 2),
                "aeration_airflow_nm3_hr": round(random.uniform(1000, 3000), 2),
                "silo_pressure_pa": round(random.uniform(2000, 5000), 2),

                # Packing Plant
                "packing_machine_speed_bags_min": round(random.uniform(60, 80), 2),
                "packing_machine_efficiency_pct": round(random.uniform(70, 85), 2),
                "packing_machine_power_kw": round(random.uniform(30, 50), 2),
                "bag_weight_kg": round(random.uniform(45, 50), 2),
                "bag_reject_rate_pct": round(random.uniform(5, 10), 2),
                "rejected_bags_count": random.randint(5, 15),
                "packing_machine_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Bulk Loading
                "bulk_loading_rate_tph": round(random.uniform(50, 100), 2),
                "truck_loading_time_min": round(random.uniform(20, 30), 2),
                "inventory_turnover_rate": round(random.uniform(0.5, 2), 2),

                # Dispatch & Inventory
                "daily_dispatch_tonnes": round(random.uniform(500, 1000), 2),
                "dispatch_rate_tph": round(random.uniform(50, 100), 2),
                "inventory_level_tonnes": round(random.uniform(100, 300), 2),
                "customer_complaints_count": random.randint(1, 10),

                # Alarms
                "silo_overpressure_alarm": random.choice([0, 1]),
                "packing_machine_jam_alarm": random.choice([0, 1]),
                "truck_delay_alarm": random.choice([0, 1]),

                # Emissions
                "dust_emission_mgNm3": round(random.uniform(5, 15), 2),
            }
        elif self.scenario == "critical_high":
            record = {
                "timestamp": timestamp.isoformat(),

                # Storage Silos
                "silo_level_pct": round(random.uniform(95, 100), 2),
                "silo_pressure_mbar": round(random.uniform(120, 150), 2),
                "silo_temp_c": round(random.uniform(60, 80), 2),
                "aeration_airflow_nm3_hr": round(random.uniform(5000, 7000), 2),
                "silo_pressure_pa": round(random.uniform(10000, 15000), 2),

                # Packing Plant
                "packing_machine_speed_bags_min": round(random.uniform(100, 140), 2),
                "packing_machine_efficiency_pct": round(random.uniform(90, 98), 2),
                "packing_machine_power_kw": round(random.uniform(70, 120), 2),
                "bag_weight_kg": round(random.uniform(55, 60), 2),
                "bag_reject_rate_pct": round(random.uniform(0, 2), 2),
                "rejected_bags_count": random.randint(0, 5),
                "packing_machine_status": random.choice([0, 1]),  # 0: Off, 1: On

                # Bulk Loading
                "bulk_loading_rate_tph": round(random.uniform(150, 250), 2),
                "truck_loading_time_min": round(random.uniform(5, 10), 2),
                "inventory_turnover_rate": round(random.uniform(3, 7), 2),

                # Dispatch & Inventory
                "daily_dispatch_tonnes": round(random.uniform(1500, 2500), 2),
                "dispatch_rate_tph": round(random.uniform(150, 250), 2),
                "inventory_level_tonnes": round(random.uniform(800, 1200), 2),
                "customer_complaints_count": random.randint(0, 3),

                # Alarms
                "silo_overpressure_alarm": random.choice([0, 1]),
                "packing_machine_jam_alarm": random.choice([0, 1]),
                "truck_delay_alarm": random.choice([0, 1]),

                # Emissions
                "dust_emission_mgNm3": round(random.uniform(20, 60), 2),
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
    gen = Stage5StoragePackingGenerator(seed=42)
    try:
        data = gen.generate_batch(n=5)
        logging.info(json.dumps(data, indent=2))
    except Exception as e:
        logging.error(f"Error generating Stage 5 data: {e}")
