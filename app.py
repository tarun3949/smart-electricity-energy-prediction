from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# ================================
# FRONTEND UI UPGRADE ONLY
# BACKEND NOT CHANGED
# REPLACE ONLY HTML_PAGE
# ================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Smart Electricity Intelligence
</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{
    background:#020617;
    overflow-x:hidden;
    color:white;
    min-height:100vh;
}

/* =======================================
THUNDER BACKGROUND
======================================= */

.background{
    position:fixed;
    width:100%;
    height:100%;
    overflow:hidden;
    z-index:-3;
    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827,
        #020617
    );
    background-size:400% 400%;
    animation:bgMove 15s ease infinite;
}

@keyframes bgMove{

    0%{
        background-position:0% 50%;
    }

    50%{
        background-position:100% 50%;
    }

    100%{
        background-position:0% 50%;
    }
}

/* =======================================
THUNDER EFFECT
======================================= */

.thunder{

    position:fixed;
    width:4px;
    height:200px;
    background:white;
    top:-200px;
    opacity:0;
    box-shadow:
    0 0 25px white,
    0 0 50px #38bdf8,
    0 0 80px #60a5fa;

    animation:lightning 6s linear infinite;
}

.thunder:nth-child(1){
    left:15%;
    animation-delay:1s;
}

.thunder:nth-child(2){
    left:45%;
    animation-delay:3s;
}

.thunder:nth-child(3){
    left:75%;
    animation-delay:5s;
}

@keyframes lightning{

    0%{
        opacity:0;
        top:-200px;
    }

    5%{
        opacity:1;
    }

    10%{
        opacity:0;
        top:100%;
    }

    100%{
        opacity:0;
    }
}

/* =======================================
MAIN CONTAINER
======================================= */

.container{
    width:95%;
    max-width:1450px;
    margin:auto;
    padding:40px 20px;
}

/* =======================================
HEADER
======================================= */

.header{
    text-align:center;
    animation:fadeIn 1s ease;
}

.header h1{

    font-size:62px;
    font-weight:700;

    background:
    linear-gradient(
        90deg,
        #60a5fa,
        #06b6d4,
        #34d399
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.header p{

    margin-top:12px;
    color:#94a3b8;
    font-size:19px;
}

.live-box{

    margin-top:25px;

    display:inline-flex;
    align-items:center;
    gap:10px;

    padding:12px 24px;

    border-radius:50px;

    background:rgba(15,23,42,0.7);

    border:1px solid rgba(255,255,255,0.08);

    backdrop-filter:blur(10px);
}

.live-dot{

    width:12px;
    height:12px;

    border-radius:50%;

    background:#22c55e;

    animation:pulse 1s infinite;
}

@keyframes pulse{

    0%{
        opacity:1;
    }

    50%{
        opacity:0.3;
    }

    100%{
        opacity:1;
    }
}

/* =======================================
UPLOAD BOX
======================================= */

.upload-box{

    margin-top:45px;

    background:
    rgba(15,23,42,0.85);

    border-radius:30px;

    padding:50px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.08);

    backdrop-filter:blur(18px);

    box-shadow:
    0 10px 40px rgba(0,0,0,0.4);

    transition:0.5s;
}

.upload-box:hover{

    transform:translateY(-8px);

    box-shadow:
    0 15px 60px rgba(59,130,246,0.25);
}

.upload-icon{

    font-size:90px;

    animation:float 3s ease infinite;
}

@keyframes float{

    0%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-15px);
    }

    100%{
        transform:translateY(0px);
    }
}

.upload-box h2{

    margin-top:10px;
    font-size:34px;
}

.upload-box p{

    margin-top:12px;
    color:#94a3b8;
}

input[type=file]{

    margin-top:30px;

    background:#1e293b;

    padding:14px;

    border-radius:15px;

    color:white;
}

input[type=text]{

    width:350px;

    margin-top:25px;

    padding:16px;

    border:none;

    border-radius:50px;

    background:#1e293b;

    color:white;

    outline:none;

    font-size:16px;
}

button{

    margin-top:30px;

    padding:16px 45px;

    border:none;

    border-radius:50px;

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );

    color:white;

    font-size:17px;

    font-weight:600;

    cursor:pointer;

    transition:0.4s;
}

button:hover{

    transform:
    translateY(-5px)
    scale(1.03);

    box-shadow:
    0 10px 35px rgba(37,99,235,0.5);
}

/* =======================================
LOADER
======================================= */

.loader{

    width:75px;
    height:75px;

    border-radius:50%;

    border:7px solid rgba(255,255,255,0.08);

    border-top:7px solid #38bdf8;

    margin:35px auto;

    display:none;

    animation:spin 1s linear infinite;
}

@keyframes spin{

    100%{
        transform:rotate(360deg);
    }
}

/* =======================================
DASHBOARD
======================================= */

.dashboard{
    margin-top:45px;
}

.grid{

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(240px,1fr));

    gap:25px;
}

.card{

    position:relative;

    overflow:hidden;

    background:
    rgba(17,24,39,0.9);

    padding:32px;

    border-radius:28px;

    border:1px solid rgba(255,255,255,0.06);

    transition:0.4s;
}

.card:hover{

    transform:translateY(-10px);
}

.card::before{

    content:"";

    position:absolute;

    width:180%;
    height:180%;

    background:
    linear-gradient(
        45deg,
        transparent,
        rgba(255,255,255,0.08),
        transparent
    );

    top:-120%;
    left:-120%;

    transition:1s;
}

.card:hover::before{

    top:120%;
    left:120%;
}

.card h3{

    color:#93c5fd;

    margin-bottom:15px;

    font-size:17px;
}

.card p{

    font-size:34px;

    font-weight:700;
}

/* =======================================
CHARTS
======================================= */

.chart-box{

    margin-top:40px;

    background:#111827;

    border-radius:28px;

    padding:35px;
}

/* =======================================
INSIGHT BOX
======================================= */

.info-box{

    margin-top:35px;

    background:#111827;

    border-radius:28px;

    padding:35px;

    line-height:1.9;
}

.info-box h2{

    color:#60a5fa;
}

/* =======================================
FEATURE BOXES
======================================= */

.feature-grid{

    margin-top:40px;

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(280px,1fr));

    gap:25px;
}

.feature-card{

    background:
    linear-gradient(
        135deg,
        #111827,
        #1e293b
    );

    border-radius:25px;

    padding:30px;

    transition:0.4s;
}

.feature-card:hover{

    transform:
    scale(1.03)
    translateY(-6px);
}

.feature-card h3{

    color:#38bdf8;

    margin-bottom:15px;
}

/* =======================================
FOOTER
======================================= */

.footer{

    text-align:center;

    margin-top:50px;

    color:#64748b;

    font-size:14px;
}

/* =======================================
ANIMATION
======================================= */

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

</style>

</head>

<body>

<div class="background"></div>

<div class="thunder"></div>
<div class="thunder"></div>
<div class="thunder"></div>

<div class="container">

    <div class="header">

        <h1>
            ⚡ Smart Electricity Intelligence
        </h1>

        <p>
            AI Powered Electricity Analytics Dashboard
        </p>

        <div class="live-box">

            <div class="live-dot"></div>

            Live AI Monitoring Active

        </div>

    </div>

    <div class="upload-box">

        <div class="upload-icon">
            ⚡
        </div>

        <h2>
            Upload Electricity Dataset
        </h2>

        <p>
            Analyze electricity consumption with AI
        </p>

        <input
            type="file"
            id="fileInput"
            accept=".csv"
        >

        <br>

        <input
            type="text"
            id="consumerId"
            placeholder="Enter Bill Number / Consumer ID"
        >

        <br>

        <button onclick="analyzeDataset()">
            Analyze Dataset
        </button>

        <div class="loader" id="loader"></div>

    </div>

    <div class="dashboard" id="resultBox">

        Waiting for dataset upload...

    </div>

    <div class="chart-box">

        <canvas id="usageChart"></canvas>

    </div>

    <div class="feature-grid">

        <div class="feature-card">

            <h3>
                Smart AI Detection
            </h3>

            <p>
                Automatically detects unusual electricity patterns.
            </p>

        </div>

        <div class="feature-card">

            <h3>
                Carbon Footprint Tracking
            </h3>

            <p>
                Calculates environmental impact from electricity usage.
            </p>

        </div>

        <div class="feature-card">

            <h3>
                Real Time Monitoring
            </h3>

            <p>
                Dynamic dashboard with live analytics visualization.
            </p>

        </div>

    </div>

    <div class="footer">

        Smart Electricity Intelligence Platform © 2026

    </div>

</div>

</body>

</html>

"""
@app.route("/")
def home():

    return render_template_string(HTML_PAGE)

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        if "file" not in request.files:

            return jsonify({

                "success": False,
                "error": "No file uploaded"

            })

        file = request.files["file"]

        consumer = request.form.get(
            "consumer_id",
            "N/A"
        )

        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(include="number")

        if numeric_columns.empty:

            return jsonify({

                "success": False,
                "error": "Dataset has no numeric columns"

            })

        usage_column = numeric_columns.columns[-1]

        usage_data = numeric_columns[usage_column]

        average = round(float(usage_data.mean()), 2)

        maximum = round(float(usage_data.max()), 2)

        minimum = round(float(usage_data.min()), 2)

        total = round(float(usage_data.sum()), 2)

        bill = round(total * 8.5, 2)

        if average > 500:

            recommendation = (
                "High electricity usage detected. "
                "Reduce heavy appliance usage during peak hours."
            )

            insight = (
                "AI detected unusually high power consumption patterns."
            )

            score = 45

        elif average > 250:

            recommendation = (
                "Moderate electricity usage detected. "
                "Energy optimization is recommended."
            )

            insight = (
                "Usage is stable but can be optimized further."
            )

            score = 72

        else:

            recommendation = (
                "Electricity usage is optimized and efficient."
            )

            insight = (
                "Consumption patterns are balanced and eco-friendly."
            )

            score = 92

        return jsonify({

            "success": True,

            "consumer": consumer,

            "average": average,

            "maximum": maximum,

            "minimum": minimum,

            "total": total,

            "bill": bill,

            "score": score,

            "recommendation": recommendation,

            "insight": insight

        })

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        })

@app.route("/health")
def health():

    return jsonify({

        "status": "running"

    })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
