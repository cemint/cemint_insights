"""
src/services/recommender.py
---------------------------

Generates process optimization recommendations based on AI insights.
This can be enhanced later to use Gemini prompts, Vertex AI, or other ML models.
"""

def generate_recommendation(stage: str, parameters: dict):
    """
    Generate simple heuristic-based recommendations for PoC.

    Args:
        stage (str): plant stage ("raw_mill", "kiln", "utilities")
        parameters (dict): current process parameters

    Returns:
        dict: recommended actions
    """
    recommendations = {}

    if stage == "raw_mill":
        # Example: adjust mill load or grinding speed
        mill_load = parameters.get("mill_load", 80)
        if mill_load > 90:
            recommendations["action"] = "Reduce mill load by 5%"
        elif mill_load < 70:
            recommendations["action"] = "Increase mill load by 5%"
        else:
            recommendations["action"] = "Mill load is optimal"

    elif stage == "kiln":
        # Example: adjust burner temp
        temp = parameters.get("temperature", 1400)
        if temp > 1450:
            recommendations["action"] = "Reduce burner temperature by 20°C"
        elif temp < 1350:
            recommendations["action"] = "Increase burner temperature by 20°C"
        else:
            recommendations["action"] = "Kiln temperature is optimal"

    elif stage == "utilities":
        # Example: adjust fan or pump speed
        energy_consumption = parameters.get("energy", 1000)
        if energy_consumption > 1200:
            recommendations["action"] = "Optimize fan/pump speed to reduce energy"
        else:
            recommendations["action"] = "Utility energy usage is within normal range"

    else:
        recommendations["action"] = "Stage not recognized. No recommendation."

    return recommendations

# -------------------------------
# Example standalone test
# -------------------------------
if __name__ == "__main__":
    test_params = {"mill_load": 95}
    print(generate_recommendation("raw_mill", test_params))

    test_params = {"temperature": 1460}
    print(generate_recommendation("kiln", test_params))
