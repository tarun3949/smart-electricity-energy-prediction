from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Smart Electricity Analytics</title>

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
    color:white;
    overflow-x:hidden;
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
    max-width:1400px;
    margin:auto;
    padding:40px 20px;
}

.title{
    text-align:center;
    margin-bottom:40px;
    animation:fadeIn 1s ease;
}

.title h1{
    font-size:52px;
    font-weight:700;
    background:linear-gradient(90deg,#3b82f6,#06b6d4,#10b981);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.title p{
    color:#94a3b8;
    margin-top:10px;
    font-size:18px;
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

.upload-box{
    background:rgba(15,23,42,0.85);
    border:2px dashed #334155;
    border-radius:30px;
    padding:50px;
    text-align:center;
    transition:0.4s;
    backdrop-filter:blur(12px);
    box-shadow:0 10px 40px rgba(0,0,0,0.4);
}

.upload-box:hover{
    transform:translateY(-5px);
    border-color:#38bdf8;
}

.upload-icon{
    font-size:60px;
    margin-bottom:20px;
    animation:float 3s ease-in-out infinite;
}

@keyframes float{
    0%{transform:translateY(0px);}
    50%{transform:translateY(-10px);}
    100%{transform:translateY(0px);}
}

.file-input{
    margin-top:20px;
    color:white;
    font-size:16px;
}

button{
    margin-top:25px;
    padding:16px 50px;
    border:none;
    border-radius:50px;
    background:linear-gradient(135deg,#2563eb,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:600;
    cursor:pointer;
    transition:0.4s;
}

button:hover{
    transform:translateY(-5px) scale(1.03);
    box-shadow:0 10px 30px rgba(37,99,235,0.5);
}

.loader{
    width:70px;
    height:70px;
    border:6px solid rgba(255,255,255,0.1);
    border-top:6px solid #38bdf8;
    border-radius:50%;
    animation:spin 1s linear infinite;
    margin:30px auto;
    display:none;
}

@keyframes spin{
    100%{
        transform:rotate(360deg);
    }
}

.result-box{
    margin-top:40px;
    background:rgba(15,23,42,0.92);
    border-radius:30px;
    padding:40px;
    animation:fadeIn 1s ease;
    box-shadow:0 10px 50px rgba(0,0,0,0.4);
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
    gap:25px;
    margin-top:30px;
}

.card{
    background:#1e293b;
    padding:30px;
    border-radius:25px;
    transition:0.4s;
    position:relative;
    overflow:hidden;
}

.card::before{
    content:"";
    position:absolute;
    width:120%;
    height:120%;
    background:linear-gradient(45deg,transparent,#38bdf8,transparent);
    top:-100%;
    left:-100%;
    transition:0.8s;
}

.card:hover::before{
    top:100%;
    left:100%;
}

.card:hover{
    transform:translateY(-8px);
    background:#243041;
}

.card h3{
    color:#93c5fd;
    margin-bottom:15px;
    font-size:17px;
}

.card p{
    font-size:32px;
    font-weight:700;
}

.chart-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(450px,1fr));
    gap:30px;
    margin-top:40px;
}

.chart-container{
    background:#111827;
    border-radius:25px;
    padding:25px;
}

.progress-section{
    margin-top:30px;
}

.progress-bar{
    width:100%;
    height:20px;
    background:#1e293b;
    border-radius:20px;
    overflow:hidden;
    margin-top:10px;
}

.progress{
    height:100%;
    width:0%;
    background:linear-gradient(90deg,#2563eb,#06b6d4,#10b981);
    animation:load 2s forwards;
}

@keyframes load{
    from{
        width:0%;
    }
    to{
        width:100%;
    }
}

.info-box{
    margin-top:30px;
    background:#1e293b;
    padding:25px;
    border-radius:20px;
    line-height:1.8;
}

.footer{
    text-align:center;
    margin-top:50px;
    color:#64748b;
    font-size:14px;
}

.badge{
    display:inline-block;
    padding:8px 18px;
    background:#0f766e;
    border-radius:30px;
    margin-top:15px;
    font-size:14px;
}

.live-dot{
    width:12px;
    height:12px;
    background:#22c55e;
    border-radius:50%;
    display:inline-block;
    margin-right:8px;
    animation:pulse 1s infinite;
}

@keyframes pulse{
    0%{opacity:1;}
    50%{opacity:0.3;}
    100%{opacity:1;}
}

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <div class="title">

        <h1>⚡ Smart Electricity Analytics</h1>

        <p>
            AI Powered Electricity Monitoring & Consumption Intelligence
        </p>

        <div class="badge">
            <span class="live-dot"></span>
            Live AI Analytics Active
        </div>

    </div>

    <div class="upload-box">

        <div class="upload-icon">
            ⚡
        </div>

        <h2>Upload Electricity Dataset</h2>

        <p style="margin-top:10px;color:#94a3b8;">
            Upload CSV Dataset for Advanced AI Analysis
        </p>

        <input
            type="file"
            id="fileInput"
            class="file-input"
            accept=".csv"
        >

        <br>

        <button onclick="analyzeDataset()">
            Analyze Dataset
        </button>

        <div class="loader" id="loader"></div>

    </div>

    <div class="result-box" id="resultBox">

        Waiting for dataset upload...

    </div>

    <div class="chart-grid">

        <div class="chart-container">

            <canvas id="usageChart"></canvas>

        </div>

        <div class="chart-container">

            <canvas id="donutChart"></canvas>

        </div>

    </div>

    <div class="footer">

        Smart Electricity Intelligence Platform • AI Analytics Dashboard

    </div>

</div>

<script>

let usageChart;
let donutChart;

async function analyzeDataset(){

    const fileInput =
        document.getElementById("fileInput");

    const resultBox =
        document.getElementById("resultBox");

    const loader =
        document.getElementById("loader");

    if(fileInput.files.length === 0){

        resultBox.innerHTML =
            "Please upload CSV dataset.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML =
        "AI analyzing electricity dataset...";

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
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

                <h2>
                    Dataset Analysis Completed
                </h2>

                <div class="progress-section">

                    <h3>
                        AI Processing Completion
                    </h3>

                    <div class="progress-bar">

                        <div class="progress"></div>

                    </div>

                </div>

                <div class="grid">

                    <div class="card">
                        <h3>Total Rows</h3>
                        <p>${data.rows}</p>
                    </div>

                    <div class="card">
                        <h3>Total Columns</h3>
                        <p>${data.columns}</p>
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
                        <h3>Minimum Usage</h3>
                        <p>${data.minimum}</p>
                    </div>

                    <div class="card">
                        <h3>Total Consumption</h3>
                        <p>${data.total}</p>
                    </div>

                    <div class="card">
                        <h3>Efficiency Score</h3>
                        <p>${data.score}%</p>
                    </div>

                    <div class="card">
                        <h3>Usage Status</h3>
                        <p>${data.efficiency}</p>
                    </div>

                </div>

                <div class="info-box">

                    <h3>
                        AI Recommendation
                    </h3>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        ${data.recommendation}
                    </p>

                </div>

                <div class="info-box">

                    <h3>
                        Peak Consumption Alert
                    </h3>

                    <p style="margin-top:15px;color:#fca5a5;">
                        ${data.alert}
                    </p>

                </div>

                <div class="info-box">

                    <h3>
                        Carbon Footprint Analysis
                    </h3>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        Estimated CO₂ Emission:
                        ${data.carbon} kg
                    </p>

                </div>

            `;

            createUsageChart(
                data.average,
                data.maximum,
                data.minimum
            );

            createDonutChart(
                data.average,
                data.maximum,
                data.minimum
            );

        }

        else{

            resultBox.innerHTML =
                "Error: " + data.error;
        }

    }

    catch(error){

        loader.style.display = "none";

        resultBox.innerHTML =
            "Server Error";
    }
}

function createUsageChart(avg,max,min){

    const ctx =
        document.getElementById("usageChart");

    if(usageChart){
        usageChart.destroy();
    }

    usageChart = new Chart(ctx,{

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
                    '#3b82f6',
                    '#06b6d4',
                    '#10b981'
                ],

                borderRadius:12

            }]
        },

        options:{

            responsive:true,

            animation:{
                duration:2000
            },

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

function createDonutChart(avg,max,min){

    const ctx =
        document.getElementById("donutChart");

    if(donutChart){
        donutChart.destroy();
    }

    donutChart = new Chart(ctx,{

        type:'doughnut',

        data:{

            labels:[
                'Average',
                'Maximum',
                'Minimum'
            ],

            datasets:[{

                data:[
                    avg,
                    max,
                    min
                ],

                backgroundColor:[
                    '#2563eb',
                    '#06b6d4',
                    '#10b981'
                ]

            }]
        },

        options:{

            responsive:true,

            animation:{
                animateRotate:true,
                duration:2000
            },

            plugins:{

                legend:{
                    labels:{
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

        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(include="number")

        if numeric_columns.empty:

            return jsonify({

                "success": False,
                "error": "Dataset must contain numeric columns"

            })

        usage_column = numeric_columns.columns[-1]

        usage_data = numeric_columns[usage_column]

        average = round(float(usage_data.mean()), 2)

        maximum = round(float(usage_data.max()), 2)

        minimum = round(float(usage_data.min()), 2)

        total = round(float(usage_data.sum()), 2)

        carbon = round(total * 0.45, 2)

        if average > 500:

            recommendation = (
                "High electricity usage detected. "
                "Reduce appliance usage during peak hours."
            )

            efficiency = "Low Efficiency"

            alert = (
                "Critical peak consumption detected."
            )

            score = 45

        elif average > 250:

            recommendation = (
                "Moderate electricity usage detected. "
                "Switch to efficient appliances."
            )

            efficiency = "Moderate Efficiency"

            alert = (
                "Energy usage moderately high."
            )

            score = 72

        else:

            recommendation = (
                "Electricity usage is optimized."
            )

            efficiency = "High Efficiency"

            alert = (
                "No abnormal consumption detected."
            )

            score = 92

        return jsonify({

            "success": True,

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "average": average,

            "maximum": maximum,

            "minimum": minimum,

            "total": total,

            "carbon": carbon,

            "score": score,

            "recommendation": recommendation,

            "efficiency": efficiency,

            "alert": alert,

            "date": str(datetime.now().date())

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
