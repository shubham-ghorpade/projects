import pickle
import json
import numpy as np
import config
import os


class CampaignResponsePrediction:
    def __init__(self, age, marital, education, default, balance, housing, loan,
                 contact, day, month, duration, campaign, pdays, previous, poutcome,
                 job_admin, job_blue_collar, job_entrepreneur, job_housemaid, job_management,
                 job_retired, job_self_employed, job_services, job_student, job_technician,
                 job_unemployed, job_unknown):

        self.age = age
        self.marital = marital
        self.education = education
        self.default = default
        self.balance = balance
        self.housing = housing
        self.loan = loan
        self.contact = contact
        self.day = day
        self.month = month
        self.duration = duration
        self.campaign = campaign
        self.pdays = pdays
        self.previous = previous
        self.poutcome = poutcome

        # job one-hot encodings
        self.job_admin = job_admin
        self.job_blue_collar = job_blue_collar
        self.job_entrepreneur = job_entrepreneur
        self.job_housemaid = job_housemaid
        self.job_management = job_management
        self.job_retired = job_retired
        self.job_self_employed = job_self_employed
        self.job_services = job_services
        self.job_student = job_student
        self.job_technician = job_technician
        self.job_unemployed = job_unemployed
        self.job_unknown = job_unknown

    def load_model(self):
        if not os.path.exists(config.MODEL_FILE_PATH):
            raise FileNotFoundError("Model file not found.")
        with open(config.MODEL_FILE_PATH, 'rb') as f:
            self.model = pickle.load(f)

    def load_project_data(self):
        if not os.path.exists(config.JSON_FILE_PATH):
            raise FileNotFoundError("project_data.json not found.")
        with open(config.JSON_FILE_PATH, 'r') as f:
            self.project_data = json.load(f)

    def get_predicted_result(self):
        self.load_model()
        self.load_project_data()

        columns = self.project_data['columns']
        test_array = np.zeros(len(columns))

        # Fill values
        test_array[columns.index('age')] = self.age
        test_array[columns.index('marital')] = self.project_data['marital'][self.marital]
        test_array[columns.index('education')] = self.project_data['education'][self.education]
        test_array[columns.index('default')] = self.project_data['default'][self.default]
        test_array[columns.index('balance')] = self.balance
        test_array[columns.index('housing')] = self.project_data['housing'][self.housing]
        test_array[columns.index('loan')] = self.project_data['loan'][self.loan]
        test_array[columns.index('contact')] = self.project_data['contact'][self.contact]
        test_array[columns.index('day')] = self.day
        test_array[columns.index('month')] = self.project_data['month'][self.month]
        test_array[columns.index('duration')] = self.duration
        test_array[columns.index('campaign')] = self.campaign
        test_array[columns.index('pdays')] = self.pdays
        test_array[columns.index('previous')] = self.previous
        test_array[columns.index('poutcome')] = self.project_data['poutcome'][self.poutcome]

        # Jobs (already numeric 0/1)
        test_array[columns.index('job_admin.')] = self.job_admin
        test_array[columns.index('job_blue_collar')] = self.job_blue_collar
        test_array[columns.index('job_entrepreneur')] = self.job_entrepreneur
        test_array[columns.index('job_housemaid')] = self.job_housemaid
        test_array[columns.index('job_management')] = self.job_management
        test_array[columns.index('job_retired')] = self.job_retired
        test_array[columns.index('job_self-employed')] = self.job_self_employed
        test_array[columns.index('job_services')] = self.job_services
        test_array[columns.index('job_student')] = self.job_student
        test_array[columns.index('job_technician')] = self.job_technician
        test_array[columns.index('job_unemployed')] = self.job_unemployed
        test_array[columns.index('job_unknown')] = self.job_unknown

        prediction = self.model.predict([test_array])[0]
        return "Yes (Customer will Respond)" if prediction == 1 else "No (Customer will NOT Respond)"
