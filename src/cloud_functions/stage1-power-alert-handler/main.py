import os
import json
import base64
from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)

# --- Configuration ---
# Get these from Cloud Run environment variables
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'cement-ai-470817')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET_ID', 'cementAI_syn_data_stage1')
BIGQUERY_TABLE = os.environ.get('BIGQUERY_TABLE_ID', 'Power_Eff_Degradation_Triggers')

# Initialize BigQuery client outside the request handler for efficiency
bigquery_client = bigquery.Client(project=PROJECT_ID)

@app.route('/', methods=['POST'])
def index():
    """
    Receives Pub/Sub push messages, decodes them, and inserts into BigQuery.
    """
    if not request.is_json:
        print("Received non-JSON request.")
        return 'Bad Request: Request must be JSON', 400

    try:
        envelope = request.get_json()
        if not envelope or 'message' not in envelope:
            print("Invalid Pub/Sub message format: 'message' key missing.")
            return 'Bad Request: Invalid Pub/Sub message format', 400

        pubsub_message = envelope['message']

        if 'data' in pubsub_message:
            # Pub/Sub message data is base64 encoded
            message_data_encoded = pubsub_message['data']
            message_data_decoded = base64.b64decode(message_data_encoded).decode('utf-8')
            print(f"Decoded Pub/Sub message data: {message_data_decoded}")

            # Assuming the Pub/Sub message data is a JSON string
            try:
                row_to_insert = json.loads(message_data_decoded)
            except json.JSONDecodeError as e:
                print(f"Error decoding message data as JSON: {e}")
                return f'Bad Request: Message data is not valid JSON - {e}', 400

            # BigQuery expects a list of rows, even for a single row insert
            rows_to_insert = [row_to_insert]

            table_ref = bigquery_client.dataset(BIGQUERY_DATASET).table(BIGQUERY_TABLE)
            errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)

            if errors:
                print(f"Errors encountered while inserting rows: {errors}")
                return jsonify({'message': 'BigQuery insert errors', 'errors': errors}), 500
            else:
                print(f"Successfully inserted message into BigQuery table {BIGQUERY_DATASET}.{BIGQUERY_TABLE}")
                return 'Message processed and inserted into BigQuery', 200

        else:
            print("Pub/Sub message has no 'data' attribute.")
            return 'No data in Pub/Sub message', 200 # Or 400 if data is always expected

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f'Internal Server Error: {e}', 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used in production.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))




