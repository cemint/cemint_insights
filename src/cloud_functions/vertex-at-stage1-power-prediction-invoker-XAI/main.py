import os
import json
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from google.cloud import pubsub_v1
from google.protobuf.json_format import MessageToJson 
# from google.cloud.aiplatform_v1.types import instance
import functions_framework
import proto

# --- Configuration ---
PROJECT_ID = os.environ.get('GCP_PROJECT') # Your GCP Project ID
LOCATION = os.environ.get('GCP_REGION') # Your Cloud Function region
VERTEX_AI_ENDPOINT_ID = os.environ.get('VERTEX_AI_ENDPOINT_ID') # Replace with your Vertex AI Endpoint ID
VERTEX_AI_MODEL_ID = os.environ.get('VERTEX_AI_MODEL_ID') # Replace with your Vertex AI Model ID (if needed for client init)
PUB_SUB_TOPIC_ID = os.environ.get('PUB_SUB_TOPIC_ID') # The Pub/Sub topic for alerts

# Initialize Vertex AI client
# You might need to specify the model_id if your endpoint serves a specific model
# For a deployed endpoint, you usually interact directly with the endpoint resource name
vertex_ai_client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"})
endpoint_name = vertex_ai_client.endpoint_path(
    project=PROJECT_ID, location=LOCATION, endpoint=VERTEX_AI_ENDPOINT_ID
)

# Initialize Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUB_SUB_TOPIC_ID)

# --- Helper Function for Efficiency Evaluation ---
def evaluate_efficiency(predicted_response):
    """
    Implement your custom logic here to evaluate the model's efficiency.
    This is a placeholder. You'll need to define what "efficiency" means
    for your model (e.g., accuracy, latency, specific metric thresholds).

    Args:
        prediction_response (dict): The response received from the Vertex AI endpoint.
        input_data (dict): The input data sent to the model.

    Returns:
        bool: True if efficiency is degraded, False otherwise.
        str: An alert message if degraded, None otherwise.
    """
    # Example: Check if a certain prediction confidence is below a threshold
    # This is highly dependent on your model's output structure
    try:
        # Check for the predicted power efficiency is above 1.5
        for response in predicted_response:
            if response.get('value') > 1.5:
                return True, f"Power Consumption Efficiency degraded!!! Value : {response.get('value')} "

    except Exception as e:
        print(f"Error evaluating efficiency: {e}")
        return False, f"Error during efficiency evaluation: {e}"

    return False, f"Power Consumption Efficiency within acceptable limits"

# --- Cloud Function Entry Point ---
@functions_framework.http
def predict_and_alert(request):
    """
    Cloud Function (2nd gen) triggered by HTTP request.
    Invokes Vertex AI endpoint, evaluates efficiency, and publishes alerts.
    """
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    request_json = request.get_json(silent=True)
    if not request_json:
        return 'Invalid JSON payload', 400

    input_data = request_json.get('instances') # Assuming input is in 'instances' key, as per Vertex AI format
    if not input_data:
        return 'Missing "instances" in request body', 400
    instance_timestamp = input_data[0].get('timestamp') if isinstance(input_data, list) and input_data else None    

    try:
        # Make explanation request to Vertex AI endpoint
        # Note the change from .predict to .explain
        print("--- Making Explanation Request to Vertex AI Endpoint ---")
        explain_response = vertex_ai_client.explain(endpoint=endpoint_name, instances=input_data)

        # The explain_response object will contain both predictions and attributions.
        # The exact structure depends on your model and explanation method.

        # Accessing predictions (similar to before, but might be nested)
        predict_response = explain_response.predictions

        # Accessing explanations/attributions
        # This is the new part!
        # For tabular data, attributions are usually under explain_response.explanations[0].attributions.feature_attributions
        # You might need to inspect the exact structure or refer to Vertex AI documentation for your model type.
        explanations = explain_response.explanations[0]

        print("--- Raw Prediction Response ---")
        print(f"Type: {type(predict_response)}")
        print(f"Content: {predict_response}")

        print("\n--- Raw Explanations Response ---")
        print(f"Type: {type(explanations)}")
        print(f"Content: {explanations}\n")

        # Loop through explanations to get feature attributions
        feature_attributions_list = []
        for explanation in explanations:
            if explanation.attributions and explanation.attributions.feature_attributions:
                # feature_attributions is typically a dictionary where keys are feature names
                # and values are their attribution scores.
                feature_attributions = dict(explanation.attributions.feature_attributions)
                feature_attributions_list.append(feature_attributions)
                print(f"Feature Attributions for instance: {feature_attributions}")
            else:
                print("No feature attributions found for this explanation.")

        print(f"Complete list of feature attributions: {json.dumps(feature_attributions_list, indent=2)}")

        print(f"Length of predictions : {len(predict_response)}")
        prediction_results = []
        for prediction_val in predict_response:
            # Check if it's the MapComposite type
            if isinstance(prediction_val, proto.marshal.collections.maps.MapComposite):
                processed_prediction = dict(prediction_val)
            elif hasattr(prediction_val, 'DESCRIPTOR'):
                # This block handles standard protobuf messages like Value
                from google.protobuf.json_format import MessageToJson # Import here if only used conditionally
                processed_prediction = json.loads(MessageToJson(prediction_val))
            elif isinstance(prediction_val, (dict, list, str, int, float, bool)):
                # This block handles native Python types that don't need conversion
                processed_prediction = prediction_val
            else:
                # Fallback for unexpected types
                print(f"Warning: Unexpected prediction_val type: {type(prediction_val)}. Attempting string conversion.")
                processed_prediction = str(prediction_val)

             # Log the processed prediction for debugging
            print(f"Processed Prediction: {json.dumps(processed_prediction, indent=2)}")
            
            # Append the processed result to our list
            prediction_results.append(processed_prediction)

        print("--- Finished Prediction Processing, Validating efficiency ") # Added for clarity in logs

        #Evaluate efficiency
        is_degraded = False
        alert_message = None
        if prediction_results:
            is_degraded, alert_message = evaluate_efficiency(prediction_results)

        print(f"Prediction processing complete. Degraded Status : {is_degraded}, Msg : {alert_message}")
 

        if is_degraded:
            print(f"Efficiency degraded! Publishing alert: {alert_message}")
            alert_payload = {
                "timestamp": instance_timestamp or request.headers.get('X-Cloud-Trace-Context', 'unknown'), # Use instance timestamp or fallback
                "model_id": VERTEX_AI_MODEL_ID,
                "endpoint_id": VERTEX_AI_ENDPOINT_ID,
                "alert_type": "power_efficiency_degradation",
                "message": alert_message,
                "suggestion": "Decrease the Crusher Power or add more raw materials(limestone, clay or iron ore)"
            }
            
            # Publish alert to Pub/Sub
            future = publisher.publish(topic_path, json.dumps(alert_payload).encode("utf-8"))
            future.result() # Wait for the publish operation to complete
            print(f"Alert Published: {alert_payload}")
            return json.dumps({"status": "prediction_processed", "alert_triggered": True, "alert_message": alert_message}), 200
        else:
            print("Efficiency within acceptable limits.")
            return json.dumps({"status": "prediction_processed", "alert_triggered": False}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally publish an error alert
        error_alert_payload = {
            "timestamp": instance_timestamp or request.headers.get('X-Cloud-Trace-Context', 'unknown'), # Use instance timestamp or fallback
            "model_id": VERTEX_AI_MODEL_ID,
            "endpoint_id": VERTEX_AI_ENDPOINT_ID,
            "alert_type": "prediction_error",
            "message": f"Error during prediction or processing: {e}",
            "suggestion": "No suggestions available at this time."
        }
        publisher.publish(topic_path, json.dumps(error_alert_payload).encode("utf-8")).result()
        return f"Error processing request: {e}", 500