import pickle
import json
import numpy as np
import config as config

class Leadpredictor():
    def __init__(self,
                 Do_Not_Email, TotalVisits, Total_Time_Spent_on_Website, Page_Views_Per_Visit,
                 Asymmetrique_Activity_Index, Asymmetrique_Profile_Index,
                 Asymmetrique_Activity_Score, Asymmetrique_Profile_Score,
                 Lead_Origin, Lead_Source, Country,
                 How_did_you_hear_about_X_Education, What_is_your_current_occupation,
                 Tags, Lead_Quality, Lead_Profile):

        self.Do_Not_Email = Do_Not_Email
        self.TotalVisits = TotalVisits
        self.Total_Time_Spent_on_Website = Total_Time_Spent_on_Website
        self.Page_Views_Per_Visit = Page_Views_Per_Visit
        self.Asymmetrique_Activity_Index = Asymmetrique_Activity_Index
        self.Asymmetrique_Profile_Index = Asymmetrique_Profile_Index
        self.Asymmetrique_Activity_Score = Asymmetrique_Activity_Score
        self.Asymmetrique_Profile_Score = Asymmetrique_Profile_Score

        # 🔹 Correct one-hot column names
        self.Lead_Origin = "Lead_Origin_" + Lead_Origin
        self.Lead_Source = "Lead_Source_" + Lead_Source
        self.Country = "Country_" + Country
        self.How_did_you_hear_about_X_Education = "How_did_you_hear_about_X_Education_" + How_did_you_hear_about_X_Education
        self.What_is_your_current_occupation = "What_is_your_current_occupation_" + What_is_your_current_occupation
        self.Tags = "Tags_" + Tags
        self.Lead_Quality = "Lead_Quality_" + Lead_Quality
        self.Lead_Profile = "Lead_Profile_" + Lead_Profile

    def load_model(self):
        with open(config.MODEL_FILE_PATH, 'rb') as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH, 'r') as f:
            self.project_data = json.load(f)

    def Get_lead_prediction(self):
        self.load_model()
        test_array = np.zeros(len(self.project_data['columns']))

        # 🔹 Numerical features
        test_array[0] = self.Do_Not_Email
        test_array[1] = self.TotalVisits
        test_array[2] = self.Total_Time_Spent_on_Website
        test_array[3] = self.Page_Views_Per_Visit
        test_array[4] = self.project_data['Asymmetrique_Activity_Index'][self.Asymmetrique_Activity_Index]
        test_array[5] = self.project_data['Asymmetrique_Profile_Index'][self.Asymmetrique_Profile_Index]
        test_array[6] = self.Asymmetrique_Activity_Score
        test_array[7] = self.Asymmetrique_Profile_Score

        # 🔹 One-hot categorical features
        for col_name in [
            self.Lead_Origin, self.Lead_Source, self.Country,
            self.How_did_you_hear_about_X_Education, self.What_is_your_current_occupation,
            self.Tags, self.Lead_Quality, self.Lead_Profile
        ]:
            if col_name in self.project_data['columns']:
                col_index = self.project_data['columns'].index(col_name)
                test_array[col_index] = 1

        print("Test Array:", test_array)
        lead_predict = self.model.predict([test_array])[0]
        return lead_predict


if __name__ == '__main__':
    predictor = Leadpredictor(
        Do_Not_Email=0,
        TotalVisits=8,
        Total_Time_Spent_on_Website=286,
        Page_Views_Per_Visit=8,
        Asymmetrique_Activity_Index='Medium',
        Asymmetrique_Profile_Index='Medium',
        Asymmetrique_Activity_Score=14,
        Asymmetrique_Profile_Score=16,
        Lead_Origin='API',
        Lead_Source='Direct',
        Country='India',
        How_did_you_hear_about_X_Education='Advertisements_Media',
        What_is_your_current_occupation='Housewife',
        Tags='Ineligible',
        Lead_Quality='High',
        Lead_Profile='Other'
    )

    prediction = predictor.Get_lead_prediction()
    print("Prediction:", prediction)
