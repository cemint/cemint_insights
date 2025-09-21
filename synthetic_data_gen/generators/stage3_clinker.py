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

class Stage3ClinkerGenerator:
    """
    Synthetic data generator for Stage 3: Clinker Production (Kiln & Cooler).

    Simulates:
    - Rotary kiln operating conditions
    - Flame & fuel parameters
    - Clinker cooler performance
    - Gas composition and flow
    - Energy consumption and alarms
    """

    def __init__(self, seed: int = None, scenario: str = "normal"):
        if seed:
            random.seed(seed)
        self.scenario = scenario

    def generate_record(self, timestamp: datetime.datetime = None):
        """
        Generate a single synthetic record for Stage 3.
        """
        if not timestamp:
            timestamp = datetime.datetime.now()

        if self.scenario == "normal":
            record = {
                "timestamp": timestamp.isoformat(),

                # Kiln Operation
                "kiln_speed_rpm": round(random.uniform(3.0, 4.5), 2),
                "kiln_main_drive_power_kw": round(random.uniform(450, 650), 2),
                "kiln_inlet_temp_c": round(random.uniform(950, 1050), 2),
                "kiln_outlet_temp_c": round(random.uniform(1350, 1450), 2),
                "kiln_shell_temp_c": round(random.uniform(250, 400), 2),
                "kiln_coating_thickness_mm": round(random.uniform(10, 30), 2),
                "kiln_refractory_status": random.choice(["Good", "Worn", "Critical"]),

                # Burner & Fuel
                "burner_flame_temp_c": round(random.uniform(1500, 1600), 2),
                "primary_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "secondary_air_flow_nm3_hr": round(random.uniform(10000, 20000), 2),
                "coal_feed_rate_tph": round(random.uniform(10, 20), 2),
                "oil_injection_lph": round(random.uniform(50, 100), 2),

                # Gas Composition
                "kiln_exit_o2_pct": round(random.uniform(2, 5), 2),
                "kiln_exit_co_ppm": round(random.uniform(50, 100), 2),
                "kiln_exit_no_x_ppm": round(random.uniform(100, 200), 2),
                "kiln_exit_so2_ppm": round(random.uniform(10, 20), 2),

                # Clinker Cooler
                "cooler_inlet_temp_c": round(random.uniform(300, 400), 2),
                "cooler_outlet_temp_c": round(random.uniform(100, 200), 2),
                "cooler_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "cooler_fan_power_kw": round(random.uniform(50, 100), 2),
                "clinker_discharge_rate_tph": round(random.uniform(100, 200), 2),
                "cooler_efficiency_pct": round(random.uniform(85, 95), 2),

                # Energy & Efficiency
                "specific_heat_consumption_kcal_kg": round(random.uniform(700, 800), 2),
                "kiln_specific_power_kwht": round(random.uniform(20, 30), 2),

                # Alarms / Flags
                "high_co_alarm": random.choice([0, 1]),
                "flame_instability_alarm": random.choice([0, 1]),
                "kiln_vibration_alarm": random.choice([0, 1]),
                "cooler_fan_failure_alarm": random.choice([0, 1]),

                # Missing fields
                "kiln_feed_tph": round(random.uniform(150, 200), 2),
                "kiln_main_burner_fuel_kgph": round(random.uniform(1000, 2000), 2),
                "kiln_secondary_air_temp_c": round(random.uniform(800, 900), 2),
                "kiln_exit_gas_temp_c": round(random.uniform(300, 400), 2),
                "kiln_O2_pct": round(random.uniform(2, 5), 2),
                "clinker_quality_lsf": round(random.uniform(90, 100), 2),
                "clinker_quality_silica_modulus": round(random.uniform(2, 3), 2),
                "clinker_free_lime_pct": round(random.uniform(1, 2), 2),
                "cooler_pressure_drop_pa": round(random.uniform(100, 200), 2),
                "kiln_NOx_ppm": round(random.uniform(100, 200), 2),
                "kiln_CO_ppm": round(random.uniform(50, 100), 2),
                "cooler_exit_temp_c": round(random.uniform(100, 200), 2),
            }
        elif self.scenario == "critical_low":
            record = {
                "timestamp": timestamp.isoformat(),

                # Kiln Operation
                "kiln_speed_rpm": round(random.uniform(2.0, 3.0), 2),
                "kiln_main_drive_power_kw": round(random.uniform(300, 450), 2),
                "kiln_inlet_temp_c": round(random.uniform(850, 950), 2),
                "kiln_outlet_temp_c": round(random.uniform(1250, 1350), 2),
                "kiln_shell_temp_c": round(random.uniform(250, 400), 2),
                "kiln_coating_thickness_mm": round(random.uniform(10, 30), 2),
                "kiln_refractory_status": random.choice(["Good", "Worn", "Critical"]),

                # Burner & Fuel
                "burner_flame_temp_c": round(random.uniform(1500, 1600), 2),
                "primary_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "secondary_air_flow_nm3_hr": round(random.uniform(10000, 20000), 2),
                "coal_feed_rate_tph": round(random.uniform(10, 20), 2),
                "oil_injection_lph": round(random.uniform(50, 100), 2),

                # Gas Composition
                "kiln_exit_o2_pct": round(random.uniform(2, 5), 2),
                "kiln_exit_co_ppm": round(random.uniform(50, 100), 2),
                "kiln_exit_no_x_ppm": round(random.uniform(100, 200), 2),
                "kiln_exit_so2_ppm": round(random.uniform(10, 20), 2),

                # Clinker Cooler
                "cooler_inlet_temp_c": round(random.uniform(300, 400), 2),
                "cooler_outlet_temp_c": round(random.uniform(100, 200), 2),
                "cooler_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "cooler_fan_power_kw": round(random.uniform(50, 100), 2),
                "clinker_discharge_rate_tph": round(random.uniform(100, 200), 2),
                "cooler_efficiency_pct": round(random.uniform(85, 95), 2),

                # Energy & Efficiency
                "specific_heat_consumption_kcal_kg": round(random.uniform(700, 800), 2),
                "kiln_specific_power_kwht": round(random.uniform(20, 30), 2),

                # Alarms / Flags
                "high_co_alarm": random.choice([0, 1]),
                "flame_instability_alarm": random.choice([0, 1]),
                "kiln_vibration_alarm": random.choice([0, 1]),
                "cooler_fan_failure_alarm": random.choice([0, 1]),

                # Missing fields
                "kiln_feed_tph": round(random.uniform(150, 200), 2),
                "kiln_main_burner_fuel_kgph": round(random.uniform(1000, 2000), 2),
                "kiln_secondary_air_temp_c": round(random.uniform(800, 900), 2),
                "kiln_exit_gas_temp_c": round(random.uniform(300, 400), 2),
                "kiln_O2_pct": round(random.uniform(2, 5), 2),
                "clinker_quality_lsf": round(random.uniform(90, 100), 2),
                "clinker_quality_silica_modulus": round(random.uniform(2, 3), 2),
                "clinker_free_lime_pct": round(random.uniform(1, 2), 2),
                "cooler_pressure_drop_pa": round(random.uniform(100, 200), 2),
                "kiln_NOx_ppm": round(random.uniform(100, 200), 2),
                "kiln_CO_ppm": round(random.uniform(50, 100), 2),
                "cooler_exit_temp_c": round(random.uniform(100, 200), 2),
            }
        elif self.scenario == "critical_high":
            record = {
                "timestamp": timestamp.isoformat(),

                # Kiln Operation
                "kiln_speed_rpm": round(random.uniform(4.5, 6.0), 2),
                "kiln_main_drive_power_kw": round(random.uniform(650, 800), 2),
                "kiln_inlet_temp_c": round(random.uniform(1050, 1150), 2),
                "kiln_outlet_temp_c": round(random.uniform(1450, 1550), 2),
                "kiln_shell_temp_c": round(random.uniform(250, 400), 2),
                "kiln_coating_thickness_mm": round(random.uniform(10, 30), 2),
                "kiln_refractory_status": random.choice(["Good", "Worn", "Critical"]),

                # Burner & Fuel
                "burner_flame_temp_c": round(random.uniform(1500, 1600), 2),
                "primary_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "secondary_air_flow_nm3_hr": round(random.uniform(10000, 20000), 2),
                "coal_feed_rate_tph": round(random.uniform(10, 20), 2),
                "oil_injection_lph": round(random.uniform(50, 100), 2),

                # Gas Composition
                "kiln_exit_o2_pct": round(random.uniform(2, 5), 2),
                "kiln_exit_co_ppm": round(random.uniform(50, 100), 2),
                "kiln_exit_no_x_ppm": round(random.uniform(100, 200), 2),
                "kiln_exit_so2_ppm": round(random.uniform(10, 20), 2),

                # Clinker Cooler
                "cooler_inlet_temp_c": round(random.uniform(300, 400), 2),
                "cooler_outlet_temp_c": round(random.uniform(100, 200), 2),
                "cooler_air_flow_nm3_hr": round(random.uniform(5000, 10000), 2),
                "cooler_fan_power_kw": round(random.uniform(50, 100), 2),
                "clinker_discharge_rate_tph": round(random.uniform(100, 200), 2),
                "cooler_efficiency_pct": round(random.uniform(85, 95), 2),

                # Energy & Efficiency
                "specific_heat_consumption_kcal_kg": round(random.uniform(700, 800), 2),
                "kiln_specific_power_kwht": round(random.uniform(20, 30), 2),

                # Alarms / Flags
                "high_co_alarm": random.choice([0, 1]),
                "flame_instability_alarm": random.choice([0, 1]),
                "kiln_vibration_alarm": random.choice([0, 1]),
                "cooler_fan_failure_alarm": random.choice([0, 1]),

                # Missing fields
                "kiln_feed_tph": round(random.uniform(150, 200), 2),
                "kiln_main_burner_fuel_kgph": round(random.uniform(1000, 2000), 2),
                "kiln_secondary_air_temp_c": round(random.uniform(800, 900), 2),
                "kiln_exit_gas_temp_c": round(random.uniform(300, 400), 2),
                "kiln_O2_pct": round(random.uniform(2, 5), 2),
                "clinker_quality_lsf": round(random.uniform(90, 100), 2),
                "clinker_quality_silica_modulus": round(random.uniform(2, 3), 2),
                "clinker_free_lime_pct": round(random.uniform(1, 2), 2),
                "cooler_pressure_drop_pa": round(random.uniform(100, 200), 2),
                "kiln_NOx_ppm": round(random.uniform(100, 200), 2),
                "kiln_CO_ppm": round(random.uniform(50, 100), 2),
                "cooler_exit_temp_c": round(random.uniform(100, 200), 2),
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
    gen = Stage3ClinkerGenerator(seed=42)
    try:
        data = gen.generate_batch(n=5)
        logging.info(json.dumps(data, indent=2))
    except Exception as e:
        logging.error(f"Error generating Stage 3 data: {e}")
