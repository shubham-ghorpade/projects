import os

# Change these if you’d like
PORT_NUMBER = 5005

# Resolve paths regardless of where you run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE_PATH = os.path.join(BASE_DIR, "project_app", "Ad_budget_opti.pkl")
JSON_FILE_PATH  = os.path.join(BASE_DIR, "project_app", "project_data.json")
