import os
import json
import logging

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

SCHEMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/synthetic/schema"))

SCHEMAS = {}

try:
    # Dynamically load all JSON schema files from the schema directory
    for schema_file in os.listdir(SCHEMA_DIR):
        if schema_file.endswith("_schema.json"):
            stage_name = schema_file.replace("_schema.json", "")
            with open(os.path.join(SCHEMA_DIR, schema_file), "r") as f:
                SCHEMAS[stage_name] = json.load(f)
    logger.info("✅ All schemas loaded successfully.")
except Exception as e:
    logger.error(f"Error loading schemas: {e}")
    raise