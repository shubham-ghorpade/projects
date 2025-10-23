from flask import Flask, request, render_template
import config
from project_app.utils import CampaignResponsePrediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    # Extract numeric inputs
    age = float(data['age'])
    balance = float(data['balance'])
    day = int(data['day'])
    duration = float(data['duration'])
    campaign = int(data['campaign'])
    pdays = int(data['pdays'])
    previous = int(data['previous'])

    # Extract categorical inputs
    marital = data['marital']
    education = data['education']
    default = data['default']
    housing = data['housing']
    loan = data['loan']
    contact = data['contact']
    month = data['month']
    poutcome = data['poutcome']

    # Extract job checkboxes (1 if checked, else 0)
    job_admin = 1 if 'job_admin.' in data else 0
    job_blue_collar = 1 if 'job_blue_collar' in data else 0
    job_entrepreneur = 1 if 'job_entrepreneur' in data else 0
    job_housemaid = 1 if 'job_housemaid' in data else 0
    job_management = 1 if 'job_management' in data else 0
    job_retired = 1 if 'job_retired' in data else 0
    job_self_employed = 1 if 'job_self-employed' in data else 0
    job_services = 1 if 'job_services' in data else 0
    job_student = 1 if 'job_student' in data else 0
    job_technician = 1 if 'job_technician' in data else 0
    job_unemployed = 1 if 'job_unemployed' in data else 0
    job_unknown = 1 if 'job_unknown' in data else 0

    # Create model input object
    predictor = CampaignResponsePrediction(
        age, marital, education, default, balance, housing, loan, contact,
        day, month, duration, campaign, pdays, previous, poutcome,
        job_admin, job_blue_collar, job_entrepreneur, job_housemaid, job_management,
        job_retired, job_self_employed, job_services, job_student, job_technician,
        job_unemployed, job_unknown
    )

    result = predictor.get_predicted_result()

    return render_template('home.html', prediction_text=f'Customer Response Prediction: {result}')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT_NUMBER, debug=True)
