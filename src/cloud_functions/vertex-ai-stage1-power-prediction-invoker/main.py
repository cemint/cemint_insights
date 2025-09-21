import os
import json
from google.cloud import aiplatform
from google.cloud import pubsub_v1
from google.protobuf.json_format import MessageToJson 
import functions_framework
import proto

# --- Configuration ---
PROJECT_ID = os.environ.get('GCP_PROJECT') # Your GCP Project ID
LOCATION = os.environ.get('GCP_REGION') # Your Cloud Function region
VERTEX_AI_ENDPOINT_ID = os.environ.get('VERTEX_AI_ENDPOINT_ID') # Replace with your Vertex AI Endpoint ID
VERTEX_AI_MODEL_ID = os.environ.get('VERTEX_AI_MODEL_ID') # Replace with your Vertex AI Model ID (if needed for client init)
PUB_SUB_TOPIC_ID = os.environ.get('PUB_SUB_TOPIC_ID') # The Pub/Sub topic for alerts

# Initialize Vertex AI client
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
    Args:
        prediction_response (dict): The response received from the Vertex AI endpoint.

    Returns:
        bool: True if efficiency is degraded, False otherwise.
        str: An alert message if degraded, None otherwise.
    """
    # Example: Check if a certain prediction confidence is below a threshold
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
        # Make prediction request to Vertex AI endpoint
        predict_response = vertex_ai_client.predict(endpoint=endpoint_name, instances=input_data)
        print(f"Length of predictions : {len(predict_response.predictions)}")
        prediction_results = []
        for prediction_val in predict_response.predictions:
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