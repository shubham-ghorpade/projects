from flask import Flask, jsonify, render_template, request

import config
from project.utilis import Leadpredictor

app = Flask(__name__)

@app.route('/')
def lead_pred_model():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # <-- Parse JSON, not form
        print("Received JSON:", data)

        Do_Not_Email = int(data['Do_Not_Email'])
        TotalVisits = int(data['TotalVisits'])
        Total_Time_Spent_on_Website = int(data['Total_Time_Spent_on_Website'])
        Page_Views_Per_Visit = int(data['Page_Views_Per_Visit'])
        Asymmetrique_Activity_Index = data['Asymmetrique_Activity_Index']
        Asymmetrique_Profile_Index = data['Asymmetrique_Profile_Index']
        Asymmetrique_Activity_Score = int(data['Asymmetrique_Activity_Score'])
        Asymmetrique_Profile_Score = int(data['Asymmetrique_Profile_Score'])
        Lead_Origin = data['Lead_Origin']
        Lead_Source = data['Lead_Source']
        Country = data['Country']
        How_did_you_hear_about_X_Education = data['How_did_you_hear_about_X_Education']
        What_is_your_current_occupation = data['What_is_your_current_occupation']
        Tags = data['Tags']
        Lead_Quality = data['Lead_Quality']
        Lead_Profile = data['Lead_Profile']

        predictor = Leadpredictor(
            Do_Not_Email, TotalVisits, Total_Time_Spent_on_Website,
            Page_Views_Per_Visit, Asymmetrique_Activity_Index,
            Asymmetrique_Profile_Index, Asymmetrique_Activity_Score,
            Asymmetrique_Profile_Score, Lead_Origin, Lead_Source,
            Country, How_did_you_hear_about_X_Education,
            What_is_your_current_occupation, Tags, Lead_Quality, Lead_Profile
        )

        prediction = predictor.Get_lead_prediction()
        return jsonify({'predicted': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ =='__main__':
    app.run(host='0.0.0.0',port = config.PORT_NUMBER,debug=True)