import pickle
import json
import numpy as np
import config
import os

class AdBudgetOptimiser:
  

    def __init__(self, Campaign_Type, Device_Type, Month, CPA, Revenue):
        self.Campaign_Type = Campaign_Type
        self.Device_Type = Device_Type
        self.Month = Month
        self.CPA = CPA
        self.Revenue = Revenue
        self.model = None
        self.project_data = None

    def load_model(self):
        model_path = config.MODEL_FILE_PATH
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def load_project_data(self):
        json_path = config.JSON_FILE_PATH
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"project_data.json not found at: {json_path}")
        with open(json_path, "r") as f:
            self.project_data = json.load(f)
        if "columns" not in self.project_data:
            raise KeyError("Key 'columns' not found in project_data.json")

    def build_feature_vector(self):
        columns = self.project_data["columns"]
        vec = np.zeros(len(columns), dtype=float)

        # Numeric features
        vec[columns.index("Month")] = float(self.Month)
        vec[columns.index("CPA")] = float(self.CPA)
        vec[columns.index("Revenue")] = float(self.Revenue)

        # Encoded categorical features
        campaign_mapping = self.project_data["Campaign_Type"]
        device_mapping = self.project_data["Device_Type"]

        if self.Campaign_Type not in campaign_mapping:
            raise ValueError(f"Unknown Campaign_Type: {self.Campaign_Type}")
        if self.Device_Type not in device_mapping:
            raise ValueError(f"Unknown Device_Type: {self.Device_Type}")

        vec[columns.index("Campaign_Type")] = campaign_mapping[self.Campaign_Type]
        vec[columns.index("Device_Type")] = device_mapping[self.Device_Type]

        return vec

    def get_predicted_result(self):
        self.load_model()
        self.load_project_data()
        x = self.build_feature_vector().reshape(1, -1)
        pred = self.model.predict(x)
        if hasattr(pred, "__len__") and len(pred) == 1:
            return pred[0]
        return pred
