from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import os

# =========================================================
# INITIALIZE FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

MODEL_PATH = "model.pkl"

try:

    model = pickle.load(open(MODEL_PATH, "rb"))

    print("✅ Machine Learning Model Loaded Successfully")

except Exception as e:

    model = None

    print(f"❌ Error Loading Model: {e}")

# =========================================================
# APPLICATION DETAILS
# =========================================================

APP_NAME = "Smart Electricity Energy Prediction System"
VERSION = "1.0"

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

        "version": VERSION

    })

# =========================================================
# PREDICTION ROUTE
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # =================================================
        # GET JSON DATA FROM FRONTEND
        # =================================================

        data = request.get_json()

        # =================================================
        # VALIDATE INPUT
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
        # CONVERT INPUTS
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
        # FEATURE ARRAY
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
            Solar_Panel

        ]])

        # =================================================
        # MODEL PREDICTION
        # =================================================

        if model is None:

            return jsonify({

                "success": False,

                "error": "Model file not loaded properly"

            }), 500

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        # =================================================
        # PREDICTION RESULT
        # =================================================

        if prediction == 1:

            result = "⚠️ High Electricity Usage Predicted"

            recommendation = (

                "Try reducing appliance usage during peak hours "
                "to lower electricity consumption."

            )

            color = "red"

        else:

            result = "✅ Low Electricity Usage Predicted"

            recommendation = (

                "Electricity consumption is normal and efficient."

            )

            color = "green"

        # =================================================
        # RETURN RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "prediction": result,

            "confidence": round(float(probability) * 100, 2),

            "recommendation": recommendation,

            "theme_color": color

        })

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except ValueError:

        return jsonify({

            "success": False,

            "error": "Invalid numeric input values"

        }), 400

    except Exception as e:

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

        "version": VERSION,

        "machine_learning_model": "Random Forest Classifier",

        "features_used": [

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

    })

# =========================================================
# MAIN FUNCTION
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("⚡ SMART ELECTRICITY ENERGY PREDICTION SYSTEM")

    print("=" * 60)

    print("🚀 Flask Server Running Successfully")

    print("🌐 URL : http://127.0.0.1:5000")

    print("🤖 Model : Random Forest Classifier")

    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
