from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import os

app = Flask(__name__)


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

/* =========================
BACKGROUND
========================= */

.background{
    position:fixed;
    width:100%;
    height:100%;
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

/* =========================
THUNDER EFFECT
========================= */

.thunder{
    position:fixed;
    width:4px;
    height:220px;
    background:white;
    top:-250px;
    opacity:0;

    box-shadow:
    0 0 20px white,
    0 0 40px #38bdf8,
    0 0 80px #60a5fa;

    z-index:-2;

    animation:lightning 6s linear infinite;
}

.thunder:nth-child(2){
    left:20%;
    animation-delay:1s;
}

.thunder:nth-child(3){
    left:50%;
    animation-delay:3s;
}

.thunder:nth-child(4){
    left:80%;
    animation-delay:5s;
}

@keyframes lightning{

    0%{
        opacity:0;
        top:-250px;
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

/* =========================
CONTAINER
========================= */

.container{
    width:95%;
    max-width:1450px;
    margin:auto;
    padding:40px 20px;
}

/* =========================
HEADER
========================= */

.header{
    text-align:center;
    animation:fadeIn 1s ease;
}

.header h1{

    font-size:60px;

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

    margin-top:10px;
    color:#94a3b8;
    font-size:18px;
}

.live-box{

    display:inline-flex;
    align-items:center;
    gap:10px;

    margin-top:25px;

    padding:12px 24px;

    border-radius:50px;

    background:rgba(15,23,42,0.8);

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

/* =========================
UPLOAD BOX
========================= */

.upload-box{

    margin-top:45px;

    background:
    rgba(15,23,42,0.88);

    border-radius:30px;

    padding:50px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.08);

    backdrop-filter:blur(18px);

    transition:0.5s;
}

.upload-box:hover{

    transform:translateY(-5px);

    box-shadow:
    0 15px 50px rgba(37,99,235,0.25);
}

.upload-icon{

    font-size:85px;

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

    margin-top:25px;

    padding:14px;

    border-radius:15px;

    background:#1e293b;

    color:white;
}

input[type=text]{

    width:340px;

    margin-top:25px;

    padding:15px;

    border:none;

    border-radius:50px;

    background:#1e293b;

    color:white;

    outline:none;
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

/* =========================
LOADER
========================= */

.loader{

    width:70px;
    height:70px;

    border-radius:50%;

    border:6px solid rgba(255,255,255,0.1);

    border-top:6px solid #38bdf8;

    margin:35px auto;

    display:none;

    animation:spin 1s linear infinite;
}

@keyframes spin{

    100%{
        transform:rotate(360deg);
    }
}

/* =========================
DASHBOARD
========================= */

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

    background:
    rgba(17,24,39,0.9);

    border-radius:28px;

    padding:30px;

    transition:0.4s;

    border:1px solid rgba(255,255,255,0.06);
}

.card:hover{

    transform:translateY(-8px);
}

.card h3{

    color:#93c5fd;

    margin-bottom:15px;
}

.card p{

    font-size:32px;

    font-weight:700;
}

/* =========================
CHART
========================= */

.chart-box{

    margin-top:40px;

    background:#111827;

    border-radius:28px;

    padding:30px;
}

/* =========================
FEATURES
========================= */

.feature-grid{

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(280px,1fr));

    gap:25px;

    margin-top:40px;
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
    translateY(-8px)
    scale(1.03);
}

.feature-card h3{

    color:#38bdf8;

    margin-bottom:15px;
}

/* =========================
FOOTER
========================= */

.footer{

    text-align:center;

    margin-top:50px;

    color:#64748b;
}

/* =========================
FADE
========================= */

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

            Live Monitoring Active

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
            Upload CSV dataset for smart AI analysis
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
                AI Detection
            </h3>

            <p>
                Detect abnormal electricity consumption automatically.
            </p>

        </div>

        <div class="feature-card">

            <h3>
                Carbon Tracking
            </h3>

            <p>
                Analyze environmental impact using energy usage.
            </p>

        </div>

        <div class="feature-card">

            <h3>
                Smart Insights
            </h3>

            <p>
                Get intelligent recommendations for saving electricity.
            </p>

        </div>

    </div>

    <div class="footer">

        Smart Electricity Intelligence Platform © 2026

    </div>

</div>

<script>

let chart;

async function analyzeDataset(){

    const fileInput =
        document.getElementById("fileInput");

    const resultBox =
        document.getElementById("resultBox");

    const loader =
        document.getElementById("loader");

    const consumerId =
        document.getElementById("consumerId").value;

    if(fileInput.files.length === 0){

        resultBox.innerHTML =
            "<h2>Please upload CSV dataset.</h2>";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML =
        "<h2>Analyzing electricity usage...</h2>";

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    formData.append(
        "consumer_id",
        consumerId
    );

    try{

        const response =
            await fetch("/analyze",{

            method:"POST",

            body:formData

        });

        const data =
            await response.json();

        loader.style.display = "none";

        if(data.success){

            resultBox.innerHTML = `

                <div class="grid">

                    <div class="card">
                        <h3>Consumer ID</h3>
                        <p>${data.consumer}</p>
                    </div>

                    <div class="card">
                        <h3>Total Units</h3>
                        <p>${data.total}</p>
                    </div>

                    <div class="card">
                        <h3>Average Usage</h3>
                        <p>${data.average}</p>
                    </div>

                    <div class="card">
                        <h3>Maximum Usage</h3>
                        <p>${data.maximum}</p>
                    </div>

                    <div class="card">
                        <h3>Estimated Bill</h3>
                        <p>₹${data.bill}</p>
                    </div>

                    <div class="card">
                        <h3>Efficiency Score</h3>
                        <p>${data.score}%</p>
                    </div>

                </div>

                <div class="feature-grid">

                    <div class="feature-card">

                        <h3>AI Recommendation</h3>

                        <p>${data.recommendation}</p>

                    </div>

                    <div class="feature-card">

                        <h3>Smart Insight</h3>

                        <p>${data.insight}</p>

                    </div>

                    <div class="feature-card">

                        <h3>Usage Status</h3>

                        <p>
                            ${
                                data.score > 80
                                ? "Efficient Usage"
                                : "Needs Optimization"
                            }
                        </p>

                    </div>

                </div>

            `;

            createChart(
                data.average,
                data.maximum,
                data.minimum
            );
        }

        else{

            resultBox.innerHTML =
                "<h2>" + data.error + "</h2>";
        }

    }

    catch(error){

        loader.style.display = "none";

        resultBox.innerHTML =
            "<h2>Server Error</h2>";
    }
}

function createChart(avg,max,min){

    const ctx =
        document.getElementById("usageChart");

    if(chart){
        chart.destroy();
    }

    chart = new Chart(ctx,{

        type:'bar',

        data:{

            labels:[
                'Average',
                'Maximum',
                'Minimum'
            ],

            datasets:[{

                label:'Electricity Usage',

                data:[
                    avg,
                    max,
                    min
                ],

                backgroundColor:[
                    '#2563eb',
                    '#06b6d4',
                    '#10b981'
                ],

                borderRadius:12
            }]
        },

        options:{

            responsive:true,

            plugins:{

                legend:{
                    labels:{
                        color:'white'
                    }
                }
            },

            scales:{

                y:{
                    ticks:{
                        color:'white'
                    }
                },

                x:{
                    ticks:{
                        color:'white'
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
