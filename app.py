from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# =========================================================
# PROFESSIONAL DARK UI
# =========================================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Smart Energy Consumption Prediction</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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

    background:#0f172a;

    overflow:auto;

    padding:30px;
}

.background{

    position:fixed;

    width:100%;

    height:100%;

    background:linear-gradient(-45deg,#020617,#0f172a,#1e293b,#0f172a);

    background-size:400% 400%;

    animation:bgMove 15s ease infinite;

    z-index:-1;
}

@keyframes bgMove{

    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

.container{

    width:95%;

    max-width:1100px;

    background:rgba(15,23,42,0.92);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:30px;

    padding:40px;

    backdrop-filter:blur(15px);

    box-shadow:0 10px 50px rgba(0,0,0,0.5);

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

    font-size:42px;

    margin-bottom:10px;
}

.subtitle{

    text-align:center;

    color:#94a3b8;

    margin-bottom:35px;

    font-size:16px;
}

.upload-section{

    background:#111827;

    border:2px dashed #334155;

    border-radius:22px;

    padding:35px;

    text-align:center;

    transition:0.3s;
}

.upload-section:hover{

    border-color:#3b82f6;

    transform:scale(1.01);
}

input[type=file]{

    margin-top:18px;

    color:#e2e8f0;

    font-size:15px;
}

button{

    margin-top:25px;

    padding:16px 45px;

    border:none;

    border-radius:50px;

    background:linear-gradient(135deg,#2563eb,#06b6d4);

    color:white;

    font-size:17px;

    font-weight:600;

    cursor:pointer;

    transition:0.4s;
}

button:hover{

    transform:translateY(-5px) scale(1.03);

    box-shadow:0 10px 25px rgba(37,99,235,0.4);
}

.loader{

    margin:25px auto;

    border:5px solid rgba(255,255,255,0.1);

    border-top:5px solid #3b82f6;

    border-radius:50%;

    width:55px;

    height:55px;

    animation:spin 1s linear infinite;

    display:none;
}

@keyframes spin{

    100%{
        transform:rotate(360deg);
    }
}

.result{

    margin-top:35px;

    background:#111827;

    border-radius:25px;

    padding:30px;

    color:white;

    min-height:120px;
}

.grid{

    display:grid;

    grid-template-columns:repeat(auto-fit,minmax(240px,1fr));

    gap:20px;

    margin-top:25px;
}

.card{

    background:#1e293b;

    padding:25px;

    border-radius:20px;

    text-align:center;

    transition:0.3s;
}

.card:hover{

    transform:translateY(-5px);

    background:#243041;
}

.card h3{

    color:#93c5fd;

    font-size:16px;

    margin-bottom:10px;
}

.card p{

    font-size:24px;

    font-weight:700;
}

.chart-container{

    margin-top:40px;

    display:flex;

    justify-content:center;
}

canvas{

    max-width:380px;
}

.footer{

    text-align:center;

    color:#64748b;

    margin-top:25px;

    font-size:14px;
}

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <h1>Smart Energy Consumption Prediction</h1>

    <div class="subtitle">
        Upload Household Electricity Dataset and Analyze Power Consumption Using Artificial Intelligence
    </div>

    <div class="upload-section">

        <h2 style="color:white;">Upload CSV Dataset</h2>

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

    <div class="chart-container">

        <canvas id="donutChart"></canvas>

    </div>

    <div class="footer">

        AI Powered Household Electricity Consumption Analytics

    </div>

</div>

<script>

let donutChart;

async function uploadDataset(){

    const fileInput = document.getElementById("fileInput");

    const resultBox = document.getElementById("resultBox");

    const loader = document.getElementById("loader");

    if(fileInput.files.length === 0){

        resultBox.innerHTML = "Please upload a CSV file.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML = "Processing dataset and training AI model...";

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

                <div class="grid">

                    <div class="card">
                        <h3>Dataset Rows</h3>
                        <p>${data.rows}</p>
                    </div>

                    <div class="card">
                        <h3>Dataset Columns</h3>
                        <p>${data.columns}</p>
                    </div>

                    <div class="card">
                        <h3>Model Accuracy</h3>
                        <p>${data.accuracy}%</p>
                    </div>

                    <div class="card">
                        <h3>Average Consumption</h3>
                        <p>${data.avg_usage}</p>
                    </div>

                    <div class="card">
                        <h3>Maximum Consumption</h3>
                        <p>${data.max_usage}</p>
                    </div>

                    <div class="card">
                        <h3>Minimum Consumption</h3>
                        <p>${data.min_usage}</p>
                    </div>

                </div>

                <div style="margin-top:30px;font-size:17px;color:#cbd5e1;">
                    ${data.insight}
                </div>

            `;

            createDonutChart(
                data.avg_usage,
                data.max_usage,
                data.min_usage
            );

        }

        else{

            resultBox.innerHTML = "Error: " + data.error;
        }

    }

    catch(error){

        loader.style.display = "none";

        resultBox.innerHTML = "Server Error";
    }

}

function createDonutChart(avg,max,min){

    const ctx = document.getElementById("donutChart");

    if(donutChart){

        donutChart.destroy();
    }

    donutChart = new Chart(ctx, {

        type:'doughnut',

        data:{

            labels:[
                'Average Consumption',
                'Maximum Consumption',
                'Minimum Consumption'
            ],

            datasets:[{

                data:[avg,max,min],

                backgroundColor:[
                    '#3b82f6',
                    '#06b6d4',
                    '#10b981'
                ],

                borderWidth:0
            }]
        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    labels:{
                        color:'white',
                        font:{
                            size:14
                        }
                    }
                }
            }
        }
    });
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
# DATASET ANALYSIS
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

        df.dropna(inplace=True)

        # =============================================
        # ENCODE CATEGORICAL COLUMNS
        # =============================================

        for col in df.columns:

            if df[col].dtype == "object":

                le = LabelEncoder()

                df[col] = le.fit_transform(df[col].astype(str))

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if len(numeric_cols) < 2:

            return jsonify({

                "success": False,
                "error": "Dataset needs at least 2 numeric columns"

            })

        # =============================================
        # TARGET COLUMN
        # =============================================

        target = numeric_cols[-1]

        X = df[numeric_cols[:-1]]

        y = df[target]

        # =============================================
        # TRAIN MODEL
        # =============================================

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42

        )

        model = RandomForestRegressor(

            n_estimators=300,

            max_depth=14,

            random_state=42

        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        accuracy = r2_score(y_test, preds)

        # =============================================
        # METRICS
        # =============================================

        avg_usage = round(float(y.mean()), 2)

        max_usage = round(float(y.max()), 2)

        min_usage = round(float(y.min()), 2)

        if avg_usage > 500:

            insight = "High household electricity consumption detected. Energy optimization is recommended."

        else:

            insight = "Electricity usage appears optimized and balanced."

        return jsonify({

            "success": True,

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "accuracy": round(accuracy * 100, 2),

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

        "status":"running"

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
