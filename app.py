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
    max-width:1200px;
    margin:auto;
    padding:40px 20px;
}

.title{
    text-align:center;
    margin-bottom:40px;
    animation:fadeIn 1s ease;
}

.title h1{
    font-size:48px;
    font-weight:700;
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
    background:rgba(15,23,42,0.9);
    border:2px dashed #334155;
    border-radius:25px;
    padding:50px;
    text-align:center;
    transition:0.4s;
    backdrop-filter:blur(10px);
}

.upload-box:hover{
    transform:scale(1.01);
    border-color:#3b82f6;
}

.file-input{
    margin-top:20px;
    color:white;
}

button{
    margin-top:25px;
    padding:15px 45px;
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
    transform:translateY(-5px);
    box-shadow:0 10px 25px rgba(37,99,235,0.4);
}

.loader{
    width:60px;
    height:60px;
    border:5px solid rgba(255,255,255,0.1);
    border-top:5px solid #38bdf8;
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
    background:rgba(15,23,42,0.95);
    border-radius:25px;
    padding:35px;
    animation:fadeIn 1s ease;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
    margin-top:30px;
}

.card{
    background:#1e293b;
    padding:25px;
    border-radius:20px;
    transition:0.4s;
}

.card:hover{
    transform:translateY(-6px);
    background:#243041;
}

.card h3{
    color:#93c5fd;
    margin-bottom:12px;
    font-size:17px;
}

.card p{
    font-size:30px;
    font-weight:700;
}

.chart-container{
    margin-top:40px;
    background:#111827;
    border-radius:25px;
    padding:25px;
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#64748b;
    font-size:14px;
}

.progress-bar{
    width:100%;
    background:#1e293b;
    border-radius:20px;
    overflow:hidden;
    margin-top:20px;
}

.progress{
    width:0%;
    height:18px;
    background:linear-gradient(90deg,#2563eb,#06b6d4);
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

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <div class="title">

        <h1>⚡ Smart Electricity Analytics</h1>

        <p>Upload Electricity Dataset and Analyze Energy Usage with AI</p>

    </div>

    <div class="upload-box">

        <h2>Upload CSV Dataset</h2>

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

    <div class="chart-container">

        <canvas id="usageChart"></canvas>

    </div>

    <div class="footer">

        AI Powered Electricity Monitoring Dashboard

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

    if(fileInput.files.length === 0){

        resultBox.innerHTML =
            "Please upload CSV dataset.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML =
        "Analyzing dataset using AI...";

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

                <h2>Dataset Analysis Completed</h2>

                <div class="progress-bar">
                    <div class="progress"></div>
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
                        <h3>Average Units</h3>
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
                        <h3>Total Usage</h3>
                        <p>${data.total}</p>
                    </div>

                </div>

                <br>

                <h3>AI Recommendation</h3>

                <p style="margin-top:15px;color:#cbd5e1;line-height:1.8;">
                    ${data.recommendation}
                </p>

                <br>

                <h3>Usage Efficiency</h3>

                <p style="margin-top:15px;color:#cbd5e1;">
                    ${data.efficiency}
                </p>

                <br>

                <h3>Peak Consumption Alert</h3>

                <p style="margin-top:15px;color:#fca5a5;">
                    ${data.alert}
                </p>

            `;

            createChart(
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
                    '#3b82f6',
                    '#06b6d4',
                    '#10b981'
                ],

                borderRadius:10

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

        if average > 500:

            recommendation = (
                "High electricity usage detected. "
                "Reduce heavy appliance usage during peak hours."
            )

            efficiency = "Low Efficiency"

            alert = "Peak energy consumption is very high."

        elif average > 250:

            recommendation = (
                "Moderate electricity usage detected. "
                "Using LED appliances can improve efficiency."
            )

            efficiency = "Moderate Efficiency"

            alert = "Energy consumption is moderately high."

        else:

            recommendation = (
                "Electricity usage is optimized and balanced."
            )

            efficiency = "High Efficiency"

            alert = "No abnormal electricity spike detected."

        return jsonify({

            "success": True,

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "average": average,

            "maximum": maximum,

            "minimum": minimum,

            "total": total,

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
