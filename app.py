from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import logging
from datetime import datetime

# =========================================================
# INITIALIZE FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================================================
# LOAD TRAINED MODEL
# =========================================================

try:
    model = pickle.load(open("model.pkl", "rb"))
    logging.info("✅ Machine Learning Model Loaded Successfully")

except Exception as e:
    model = None
    logging.error(f"❌ Error Loading Model: {e}")

# =========================================================
# APPLICATION INFORMATION
# =========================================================

APP_NAME = "Smart Electricity Energy Prediction System"
VERSION = "2.0"

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        app_name=APP_NAME,
        version=VERSION
    )

# =========================================================
# HEALTH CHECK ROUTE
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",
        "application": APP_NAME,
        "version": VERSION,
        "timestamp": str(datetime.now())
    })

# =========================================================
# PREDICTION ROUTE
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # =================================================
        # RECEIVE JSON DATA
        # =================================================

        data = request.get_json()

        logging.info(f"📥 Incoming Data: {data}")

        # =================================================
        # INPUT VALIDATION
        # =================================================

        required_fields = [

            "Hour",
            "Day_of_Week",
            "Month",
            "Num_Appliances",
            "Household_Size",
            "Temperature_C",
            "Previous_Usage_kWh",
            "Is_Weekend",
            "Solar_Panel"
        ]

        for field in required_fields:

            if field not in data:

                return jsonify({

                    "success": False,
                    "error": f"Missing field: {field}"

                }), 400

        # =================================================
        # CONVERT INPUT VALUES
        # =================================================

        Hour = int(data["Hour"])
        Day_of_Week = int(data["Day_of_Week"])
        Month = int(data["Month"])
        Num_Appliances = int(data["Num_Appliances"])
        Household_Size = int(data["Household_Size"])
        Temperature_C = float(data["Temperature_C"])
        Previous_Usage_kWh = float(data["Previous_Usage_kWh"])
        Is_Weekend = int(data["Is_Weekend"])
        Solar_Panel = int(data["Solar_Panel"])

        # =================================================
        # FEATURE ENGINEERING
        # =================================================

        Average_Usage_Per_Person = (
            Previous_Usage_kWh / Household_Size
            if Household_Size > 0 else 0
        )

        Appliance_Density = (
            Num_Appliances / Household_Size
            if Household_Size > 0 else 0
        )

        Peak_Hour_Flag = 1 if Hour >= 18 and Hour <= 23 else 0

        Summer_Season = 1 if Month in [4, 5, 6] else 0

        # =================================================
        # CREATE MODEL INPUT ARRAY
        # =================================================

        features = np.array([[

            Hour,
            Day_of_Week,
            Month,
            Num_Appliances,
            Household_Size,
            Temperature_C,
            Previous_Usage_kWh,
            Is_Weekend,
            Solar_Panel,
            Average_Usage_Per_Person,
            Appliance_Density,
            Peak_Hour_Flag,
            Summer_Season

        ]])

        logging.info(f"📊 Features Prepared: {features}")

        # =================================================
        # MODEL PREDICTION
        # =================================================

        if model is None:

            return jsonify({

                "success": False,
                "error": "Model not loaded properly"

            }), 500

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        # =================================================
        # INTERPRET RESULTS
        # =================================================

        if prediction == 1:

            usage_level = "High Usage"

            message = (
                "⚠️ High Electricity Usage Predicted"
            )

            recommendation = (
                "Reduce appliance usage during peak hours "
                "to minimize electricity consumption."
            )

            color = "red"

        else:

            usage_level = "Low Usage"

            message = (
                "✅ Low Electricity Usage Predicted"
            )

            recommendation = (
                "Energy consumption is under control. "
                "Maintain efficient electricity usage."
            )

            color = "green"

        # =================================================
        # RESPONSE OBJECT
        # =================================================

        response = {

            "success": True,

            "prediction": int(prediction),

            "usage_level": usage_level,

            "message": message,

            "confidence_score": round(
                float(probability) * 100,
                2
            ),

            "recommendation": recommendation,

            "theme_color": color,

            "timestamp": str(datetime.now())

        }

        logging.info(f"✅ Prediction Completed: {response}")

        return jsonify(response)

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except ValueError as ve:

        logging.error(f"❌ Value Error: {ve}")

        return jsonify({

            "success": False,
            "error": "Invalid numeric input provided"

        }), 400

    except Exception as e:

        logging.error(f"❌ Prediction Error: {e}")

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

# =========================================================
# ABOUT ROUTE
# =========================================================

@app.route("/about")
def about():

    return jsonify({

        "application": APP_NAME,

        "description": (
            "AI-powered electricity energy prediction "
            "system using Machine Learning."
        ),

        "model": "Random Forest Classifier",

        "developer": "Tarun",

        "version": VERSION
    })

# =========================================================
# MAIN APPLICATION
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("⚡ SMART ELECTRICITY ENERGY PREDICTION SYSTEM")
    print("=" * 60)
    print("🚀 Flask Server Starting...")
    print("🌐 URL : http://127.0.0.1:5000")
    print("🤖 Model : Random Forest Classifier")
    print("=" * 60)

    app.run(

        host="0.0.0.0",
        port=5000,
        debug=True

    )