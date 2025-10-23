from flask import Flask, request, render_template, flash, redirect, url_for
import config
from project_app.utils import AdBudgetOptimiser

app = Flask(__name__)
#app.secret_key = "replace-with-a-random-secret"  # needed for flash messages

@app.route("/")
def campaign_home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
def predict_campaign_performance():
    try:
        data = request.form

        # Collect & cast inputs
        Campaign_Type = data.get("Campaign_Type", "").strip() #.get() prevents KeyError when a field is missing.
        Device_Type   = data.get("Device_Type", "").strip()
        Month         = int(data.get("Month", "").strip())
        CPA           = float(data.get("CPA", "").strip())
        Revenue       = float(data.get("Revenue", "").strip())

        # Basic server-side validation (defense in depth)
        if Campaign_Type == "" or Device_Type == "":
            flash("Please select Campaign Type and Device Type.", "warning")
            return redirect(url_for("campaign_home"))
        if not (1 <= Month <= 12):
            flash("Month must be an integer from 1 to 12.", "warning")
            return redirect(url_for("campaign_home"))
        if CPA < 0 or Revenue < 0:
            flash("CPA/Revenue must be non-negative numbers.", "warning")
            return redirect(url_for("campaign_home"))

        # Predict
        model = AdBudgetOptimiser(Campaign_Type, Device_Type, Month, CPA, Revenue)
        result = model.get_predicted_result()

        # Pretty print if it's numeric
        try:
            result_text = f"Predicted Result: {float(result):.4f}"
        except Exception:
            result_text = f"Predicted Result: {result}"

        return render_template("home.html", prediction_text=result_text)

    except Exception as e:
        # Show user-friendly error
        flash(f"Error while predicting: {e}", "danger")
        return redirect(url_for("campaign_home"))

if __name__ == "__main__":
    print("Ad-Budget Optimiser Model".center(80, "*"))
    app.run(host="0.0.0.0", port=config.PORT_NUMBER, debug=True)
