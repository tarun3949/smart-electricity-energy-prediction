from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import io

app = Flask(__name__)

# =========================================================
# PROFESSIONAL HTML + CSS + JAVASCRIPT UI
# =========================================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Smart Energy Consumption Prediction</title>

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

    overflow:hidden;

    background:linear-gradient(-45deg,#0f172a,#1e3a8a,#2563eb,#0f766e);

    background-size:400% 400%;

    animation:bgAnimation 12s ease infinite;
}

@keyframes bgAnimation{

    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

.container{

    width:92%;

    max-width:1000px;

    padding:40px;

    border-radius:30px;

    background:rgba(255,255,255,0.1);

    backdrop-filter:blur(18px);

    box-shadow:0 10px 40px rgba(0,0,0,0.35);

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

    color:white;

    text-align:center;

    font-size:42px;

    margin-bottom:10px;
}

.subtitle{

    text-align:center;

    color:#dbeafe;

    margin-bottom:35px;

    font-size:17px;
}

.upload-box{

    border:2px dashed rgba(255,255,255,0.4);

    padding:35px;

    border-radius:20px;

    text-align:center;

    transition:0.3s;

    background:rgba(255,255,255,0.06);
}

.upload-box:hover{

    transform:scale(1.01);

    border-color:#38bdf8;
}

input[type=file]{

    margin-top:15px;

    color:white;

    font-size:15px;
}

button{

    margin-top:25px;

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

    box-shadow:0 12px 25px rgba(16,185,129,0.45);
}

.result{

    margin-top:35px;

    padding:25px;

    border-radius:18px;

    background:rgba(255,255,255,0.12);

    color:white;

    font-size:18px;

    line-height:1.8;

    min-height:120px;
}

.metric{

    color:#86efac;

    font-weight:600;
}

.footer{

    margin-top:20px;

    text-align:center;

    color:#d1d5db;

    font-size:14px;
}

.loader{

    display:none;

    margin-top:20px;

    border:5px solid rgba(255,255,255,0.2);

    border-top:5px solid #38bdf8;

    border-radius:50%;

    width:50px;

    height:50px;

    animation:spin 1s linear infinite;

    margin-left:auto;
    margin-right:auto;
}

@keyframes spin{

    100%{
        transform:rotate(360deg);
    }
}

</style>

</head>

<body>

<div class="container">

    <h1>⚡ Smart Energy Prediction System</h1>

    <div class="subtitle">
        Upload Household Electricity Dataset and Predict Energy Consumption using AI
    </div>

    <div class="upload-box">

        <h2 style="color:white;">📂 Upload CSV Dataset</h2>

        <input type="file" id="fileInput" accept=".csv">

        <br>

        <button onclick="uploadDataset()">
            Analyze Dataset
        </button>

        <div class="loader" id="loader"></div>

    </div>

    <div class="result" id="resultBox">

        Waiting for dataset upload...

    </div>

    <div class="footer">

        AI Powered Household Energy Consumption Prediction

    </div>

</div>

<script>

async function uploadDataset(){

    const fileInput = document.getElementById("fileInput");

    const resultBox = document.getElementById("resultBox");

    const loader = document.getElementById("loader");

    if(fileInput.files.length === 0){

        resultBox.innerHTML = "❌ Please upload a CSV file.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML = "⏳ Processing dataset and training AI model...";

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    try{

        const response = await fetch("/analyze", {

            method:"POST",

            body:formData

        });

        const data = await response.json();

        loader.style.display = "none";

        if(data.success){

            resultBox.innerHTML = `

                <h2>✅ Analysis Complete</h2>

                <p><span class="metric">Dataset Rows:</span> ${data.rows}</p>

                <p><span class="metric">Dataset Columns:</span> ${data.columns}</p>

                <p><span class="metric">Best Model:</span> Random Forest Regressor</p>

                <p><span class="metric">Prediction Accuracy (R² Score):</span> ${data.accuracy}%</p>

                <p><span class="metric">Average Household Consumption:</span> ${data.avg_usage} kWh</p>

                <p><span class="metric">Highest Consumption Family:</span> ${data.max_usage} kWh</p>

                <p><span class="metric">Lowest Consumption Family:</span> ${data.min_usage} kWh</p>

                <p><span class="metric">Insight:</span> ${data.insight}</p>

            `;

        }

        else{

            resultBox.innerHTML = "❌ Error: " + data.error;
        }

    }

    catch(error){

        loader.style.display = "none";

        resultBox.innerHTML = "❌ Server Error";
    }

}

</script>

</body>
</html>

"""

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():

    return render_template_string(HTML_PAGE)

# =========================================================
# DATASET ANALYSIS ROUTE
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        if "file" not in request.files:

            return jsonify({

                "success": False,
                "error": "No file uploaded"

            })

        file = request.files["file"]

        df = pd.read_csv(file)

        # =============================================
        # AUTO HANDLE CATEGORICAL COLUMNS
        # =============================================

        for col in df.columns:

            if df[col].dtype == "object":

                le = LabelEncoder()

                df[col] = le.fit_transform(df[col].astype(str))

        df = df.dropna()

        # =============================================
        # AUTO DETECT TARGET COLUMN
        # =============================================

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        target = numeric_cols[-1]

        X = df[numeric_cols[:-1]]

        y = df[target]

        # =============================================
        # TRAIN BEST MODEL
        # =============================================

        X_train, X_test, y_train, y_test = train_test_split(

            X, y,

            test_size=0.2,

            random_state=42

        )

        model = RandomForestRegressor(

            n_estimators=300,

            max_depth=12,

            random_state=42

        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        score = r2_score(y_test, preds)

        # =============================================
        # ENERGY INSIGHTS
        # =============================================

        avg_usage = round(float(y.mean()), 2)

        max_usage = round(float(y.max()), 2)

        min_usage = round(float(y.min()), 2)

        if avg_usage > 500:

            insight = "⚠️ High overall household power consumption detected."

        else:

            insight = "✅ Household energy consumption appears optimized."

        return jsonify({

            "success": True,

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "accuracy": round(score * 100, 2),

            "avg_usage": avg_usage,

            "max_usage": max_usage,

            "min_usage": min_usage,

            "insight": insight

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })

# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running"

    })

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
