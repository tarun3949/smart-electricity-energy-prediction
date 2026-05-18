```python
from flask import Flask, request, jsonify, render_template_string
import numpy as np
import pickle

# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

# =====================================================
# LOAD MODEL
# =====================================================

try:
    model = pickle.load(open("model.pkl", "rb"))
    print("✅ Model Loaded Successfully")

except Exception as e:
    model = None
    print("❌ Model Error:", e)

# =====================================================
# HTML + CSS + JAVASCRIPT
# =====================================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Smart Electricity Prediction</title>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:'Poppins',sans-serif;
        }

        body{

            min-height:100vh;

            display:flex;

            justify-content:center;

            align-items:center;

            background:linear-gradient(135deg,#0f172a,#1e293b,#2563eb);

            overflow:hidden;
        }

        .container{

            width:95%;

            max-width:1000px;

            padding:40px;

            border-radius:25px;

            background:rgba(255,255,255,0.12);

            backdrop-filter:blur(18px);

            box-shadow:0 10px 40px rgba(0,0,0,0.4);

            animation:fadeIn 1s ease;

        }

        @keyframes fadeIn{

            from{
                opacity:0;
                transform:translateY(30px);
            }

            to{
                opacity:1;
                transform:translateY(0);
            }
        }

        h1{

            text-align:center;

            color:white;

            margin-bottom:10px;

            font-size:40px;
        }

        p{

            text-align:center;

            color:#d1d5db;

            margin-bottom:35px;
        }

        .grid{

            display:grid;

            grid-template-columns:repeat(auto-fit,minmax(220px,1fr));

            gap:20px;
        }

        .input-box{

            display:flex;

            flex-direction:column;
        }

        label{

            color:white;

            margin-bottom:8px;

            font-size:14px;
        }

        input{

            padding:14px;

            border:none;

            border-radius:12px;

            background:rgba(255,255,255,0.18);

            color:white;

            outline:none;

            font-size:15px;

            transition:0.3s;
        }

        input:focus{

            background:rgba(255,255,255,0.28);

            transform:scale(1.02);
        }

        input::placeholder{

            color:#d1d5db;
        }

        .btn-container{

            display:flex;

            justify-content:center;

            margin-top:35px;
        }

        button{

            padding:16px 45px;

            border:none;

            border-radius:50px;

            background:linear-gradient(135deg,#2563eb,#10b981);

            color:white;

            font-size:18px;

            font-weight:600;

            cursor:pointer;

            transition:0.4s;
        }

        button:hover{

            transform:translateY(-4px) scale(1.03);

            box-shadow:0 10px 25px rgba(16,185,129,0.4);
        }

        .result{

            margin-top:35px;

            background:rgba(255,255,255,0.12);

            padding:25px;

            border-radius:18px;

            text-align:center;

            color:white;

            font-size:22px;
        }

        .confidence{

            margin-top:10px;

            color:#d1fae5;

            font-size:17px;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>⚡ Smart Electricity Prediction</h1>

    <p>AI Powered Energy Usage Prediction System</p>

    <div class="grid">

        <div class="input-box">
            <label>Hour</label>
            <input type="number" id="Hour" placeholder="0-23">
        </div>

        <div class="input-box">
            <label>Day of Week</label>
            <input type="number" id="Day_of_Week" placeholder="1-7">
        </div>

        <div class="input-box">
            <label>Month</label>
            <input type="number" id="Month" placeholder="1-12">
        </div>

        <div class="input-box">
            <label>Number of Appliances</label>
            <input type="number" id="Num_Appliances">
        </div>

        <div class="input-box">
            <label>Household Size</label>
            <input type="number" id="Household_Size">
        </div>

        <div class="input-box">
            <label>Temperature °C</label>
            <input type="number" id="Temperature_C">
        </div>

        <div class="input-box">
            <label>Previous Usage kWh</label>
            <input type="number" id="Previous_Usage_kWh">
        </div>

        <div class="input-box">
            <label>Weekend (0/1)</label>
            <input type="number" id="Is_Weekend">
        </div>

        <div class="input-box">
            <label>Solar Panel (0/1)</label>
            <input type="number" id="Solar_Panel">
        </div>

    </div>

    <div class="btn-container">

        <button onclick="predictUsage()">

            Predict Usage

        </button>

    </div>

    <div class="result" id="resultBox">

        Waiting for Prediction...

    </div>

</div>

<script>

async function predictUsage(){

    const resultBox = document.getElementById("resultBox");

    resultBox.innerHTML = "⏳ Predicting...";

    const response = await fetch("/predict", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            Hour:document.getElementById("Hour").value,

            Day_of_Week:document.getElementById("Day_of_Week").value,

            Month:document.getElementById("Month").value,

            Num_Appliances:document.getElementById("Num_Appliances").value,

            Household_Size:document.getElementById("Household_Size").value,

            Temperature_C:document.getElementById("Temperature_C").value,

            Previous_Usage_kWh:document.getElementById("Previous_Usage_kWh").value,

            Is_Weekend:document.getElementById("Is_Weekend").value,

            Solar_Panel:document.getElementById("Solar_Panel").value

        })

    });

    const data = await response.json();

    if(data.success){

        resultBox.innerHTML = `

            ${data.prediction}

            <div class="confidence">

                Confidence: ${data.confidence}%

                <br><br>

                ${data.recommendation}

            </div>

        `;

    }

    else{

        resultBox.innerHTML = "❌ Error: " + data.error;

    }

}

</script>

</body>
</html>

"""

# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():

    return render_template_string(HTML_PAGE)

# =====================================================
# PREDICTION ROUTE
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        features = np.array([[

            int(data["Hour"]),
            int(data["Day_of_Week"]),
            int(data["Month"]),
            int(data["Num_Appliances"]),
            int(data["Household_Size"]),
            float(data["Temperature_C"]),
            float(data["Previous_Usage_kWh"]),
            int(data["Is_Weekend"]),
            int(data["Solar_Panel"])

        ]])

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        if prediction == 1:

            result = "⚠️ High Electricity Usage Predicted"

            recommendation = (
                "Reduce appliance usage during peak hours."
            )

        else:

            result = "✅ Low Electricity Usage Predicted"

            recommendation = (
                "Electricity usage is efficient and stable."
            )

        return jsonify({

            "success": True,

            "prediction": result,

            "confidence": round(float(probability) * 100, 2),

            "recommendation": recommendation

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```
