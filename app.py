from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import random
import os
from datetime import datetime

app = Flask(__name__)

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Smart Electricity Intelligence System</title>

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
}

.background{
    position:fixed;
    width:100%;
    height:100%;
    background:
    radial-gradient(circle at top left,#1d4ed8,transparent 30%),
    radial-gradient(circle at bottom right,#06b6d4,transparent 30%),
    #020617;
    z-index:-1;
}

.container{
    width:95%;
    max-width:1400px;
    margin:auto;
    padding:40px 20px;
}

.header{
    text-align:center;
    animation:fadeIn 1s ease;
}

.header h1{
    font-size:56px;
    font-weight:700;
    background:linear-gradient(90deg,#60a5fa,#06b6d4,#34d399);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.header p{
    margin-top:10px;
    color:#94a3b8;
    font-size:18px;
}

.live-status{
    margin-top:20px;
    display:inline-flex;
    align-items:center;
    gap:10px;
    background:#0f172a;
    padding:10px 20px;
    border-radius:40px;
    border:1px solid #1e293b;
}

.dot{
    width:12px;
    height:12px;
    border-radius:50%;
    background:#22c55e;
    animation:pulse 1s infinite;
}

@keyframes pulse{
    0%{opacity:1;}
    50%{opacity:0.3;}
    100%{opacity:1;}
}

.upload-box{
    margin-top:40px;
    background:rgba(15,23,42,0.85);
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:30px;
    padding:50px;
    text-align:center;
    transition:0.4s;
    box-shadow:0 10px 50px rgba(0,0,0,0.4);
}

.upload-box:hover{
    transform:translateY(-5px);
    border-color:#3b82f6;
}

.upload-icon{
    font-size:70px;
    animation:float 3s ease infinite;
}

@keyframes float{
    0%{transform:translateY(0px);}
    50%{transform:translateY(-12px);}
    100%{transform:translateY(0px);}
}

input[type=file]{
    margin-top:25px;
    color:white;
}

.bill-search{
    margin-top:30px;
}

.bill-search input{
    width:320px;
    padding:15px;
    border:none;
    border-radius:50px;
    background:#1e293b;
    color:white;
    outline:none;
    font-size:16px;
}

button{
    margin-top:25px;
    padding:15px 45px;
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

.dashboard{
    margin-top:40px;
    animation:fadeIn 1s ease;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
    gap:25px;
}

.card{
    background:rgba(15,23,42,0.9);
    border-radius:25px;
    padding:30px;
    position:relative;
    overflow:hidden;
    transition:0.4s;
    border:1px solid rgba(255,255,255,0.06);
}

.card:hover{
    transform:translateY(-8px);
    box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

.card::before{
    content:"";
    position:absolute;
    width:150%;
    height:150%;
    background:linear-gradient(
        45deg,
        transparent,
        rgba(255,255,255,0.08),
        transparent
    );
    top:-100%;
    left:-100%;
    transition:0.8s;
}

.card:hover::before{
    top:100%;
    left:100%;
}

.card h3{
    color:#93c5fd;
    margin-bottom:15px;
    font-size:16px;
}

.card p{
    font-size:34px;
    font-weight:700;
}

.charts{
    margin-top:40px;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(450px,1fr));
    gap:30px;
}

.chart-box{
    background:#111827;
    border-radius:25px;
    padding:25px;
}

.info-box{
    margin-top:30px;
    background:#111827;
    padding:30px;
    border-radius:25px;
    line-height:1.8;
}

.footer{
    text-align:center;
    margin-top:50px;
    color:#64748b;
    font-size:14px;
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

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <div class="header">

        <h1>⚡ Smart Electricity Intelligence</h1>

        <p>
            AI Powered Energy Consumption Analytics Dashboard
        </p>

        <div class="live-status">

            <div class="dot"></div>

            Live Monitoring Active

        </div>

    </div>

    <div class="upload-box">

        <div class="upload-icon">
            ⚡
        </div>

        <h2>Upload Electricity Dataset</h2>

        <p style="margin-top:10px;color:#94a3b8;">
            Analyze Electricity Usage with AI Intelligence
        </p>

        <input
            type="file"
            id="fileInput"
            accept=".csv"
        >

        <div class="bill-search">

            <input
                type="text"
                id="billNumber"
                placeholder="Enter Bill Number / Consumer ID"
            >

        </div>

        <br>

        <button onclick="analyzeDataset()">
            Analyze Electricity Data
        </button>

        <div class="loader" id="loader"></div>

    </div>

    <div class="dashboard" id="resultBox">

        Waiting for dataset upload...

    </div>

    <div class="charts">

        <div class="chart-box">

            <canvas id="barChart"></canvas>

        </div>

        <div class="chart-box">

            <canvas id="donutChart"></canvas>

        </div>

    </div>

    <div class="footer">

        Smart Electricity Intelligence Platform © 2026

    </div>

</div>

<script>

let barChart;
let donutChart;

function animateValue(id,start,end,duration){

    let range = end - start;

    let current = start;

    let increment = end > start ? 1 : -1;

    let stepTime =
        Math.abs(Math.floor(duration / range));

    let obj = document.getElementById(id);

    let timer = setInterval(function(){

        current += increment;

        obj.innerHTML = current;

        if(current == end){

            clearInterval(timer);
        }

    },stepTime);
}

async function analyzeDataset(){

    const fileInput =
        document.getElementById("fileInput");

    const resultBox =
        document.getElementById("resultBox");

    const loader =
        document.getElementById("loader");

    const billNumber =
        document.getElementById("billNumber").value;

    if(fileInput.files.length === 0){

        resultBox.innerHTML =
            "Please upload CSV dataset.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML =
        "AI analyzing electricity usage...";

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    formData.append(
        "bill_number",
        billNumber
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
                        <h3>Peak Usage</h3>
                        <p>${data.maximum}</p>
                    </div>

                    <div class="card">
                        <h3>Efficiency Score</h3>
                        <p>${data.score}%</p>
                    </div>

                    <div class="card">
                        <h3>Estimated Bill</h3>
                        <p>₹${data.bill}</p>
                    </div>

                </div>

                <div class="info-box">

                    <h2>
                        AI Recommendation
                    </h2>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        ${data.recommendation}
                    </p>

                </div>

                <div class="info-box">

                    <h2>
                        Smart AI Insights
                    </h2>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        ${data.insight}
                    </p>

                </div>

                <div class="info-box">

                    <h2>
                        Carbon Footprint
                    </h2>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        Estimated CO₂ Emission:
                        ${data.carbon} kg
                    </p>

                </div>

            `;

            createBarChart(
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

    }

    catch(error){

        loader.style.display = "none";

        resultBox.innerHTML =
            "Server Error";
    }
}

function createBarChart(avg,max,min){

    const ctx =
        document.getElementById("barChart");

    if(barChart){
        barChart.destroy();
    }

    barChart = new Chart(ctx,{

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

                borderRadius:15

            }]
        },

        options:{

            responsive:true,

            animation:{
                duration:2500
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
                duration:2500
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

        consumer =
            request.form.get(
                "bill_number",
                "N/A"
            )

        df = pd.read_csv(file)

        numeric_columns =
            df.select_dtypes(include="number")

        usage_column =
            numeric_columns.columns[-1]

        usage_data =
            numeric_columns[usage_column]

        average =
            round(float(usage_data.mean()),2)

        maximum =
            round(float(usage_data.max()),2)

        minimum =
            round(float(usage_data.min()),2)

        total =
            round(float(usage_data.sum()),2)

        bill =
            round(total * 8.5,2)

        carbon =
            round(total * 0.42,2)

        if average > 500:

            recommendation = (
                "High electricity usage detected. "
                "Reduce appliance usage during peak hours."
            )

            insight = (
                "Peak electricity spikes observed "
                "during high-demand periods."
            )

            score = 45

        elif average > 250:

            recommendation = (
                "Moderate usage detected. "
                "Using efficient appliances can reduce bills."
            )

            insight = (
                "Energy usage is stable but optimization "
                "can improve efficiency."
            )

            score = 72

        else:

            recommendation = (
                "Electricity usage is optimized."
            )

            insight = (
                "Power consumption is balanced and efficient."
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

            "carbon": carbon,

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

    port =
        int(os.environ.get("PORT",5000))

    app.run(

        host="0.0.0.0",

        port=port

    )
