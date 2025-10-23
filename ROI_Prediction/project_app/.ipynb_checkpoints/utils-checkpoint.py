import pickle
import json
import numpy as np
import config

class StudentPerformance:

    def __init__(self, study_hours, attendance, internet_access, extra_classes, health_status, parent_edu, family_income):
        self.study_hours = study_hours
        self.attendance = attendance
        self.internet_access = internet_access
        self.extra_classes = extra_classes
        self.health_status = health_status
        self.parent_edu = parent_edu
        self.family_income = family_income

    def load_model(self):
        with open(config.MODEL_FILE_PATH, 'rb') as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH, 'r') as f:
            self.project_data = json.load(f)

    def get_predicted_result(self):
        self.load_model()
        columns = self.project_data['columns']
        test_array = np.zeros(len(columns))

        test_array[0] = self.study_hours
        test_array[1] = self.attendance
        test_array[2] = self.internet_access
        test_array[3] = self.extra_classes
        test_array[4] = self.health_status

        # One-hot encode parental education
        if f'ParentalEducation_{self.parent_edu}' in columns:
            idx = columns.index(f'ParentalEducation_{self.parent_edu}')
            test_array[idx] = 1

        # One-hot encode family income
        if f'FamilyIncome_{self.family_income}' in columns:
            idx = columns.index(f'FamilyIncome_{self.family_income}')
            test_array[idx] = 1

        prediction = self.model.predict([test_array])[0]
        return "Pass" if prediction == 1 else "Fail"
