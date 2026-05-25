from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import os

app = Flask(__name__)

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Smart Electricity Intelligence</title>

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
}

.header h1{
    font-size:55px;
    background:linear-gradient(90deg,#60a5fa,#06b6d4,#34d399);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.header p{
    margin-top:10px;
    color:#94a3b8;
}

.upload-box{
    margin-top:40px;
    background:#0f172a;
    border-radius:25px;
    padding:40px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
    transition:0.4s;
}

.upload-box:hover{
    transform:translateY(-5px);
}

input[type=file]{
    margin-top:20px;
    color:white;
}

input[type=text]{
    width:320px;
    margin-top:20px;
    padding:15px;
    border:none;
    border-radius:50px;
    background:#1e293b;
    color:white;
    outline:none;
}

button{
    margin-top:25px;
    padding:15px 40px;
    border:none;
    border-radius:50px;
    background:linear-gradient(135deg,#2563eb,#06b6d4);
    color:white;
    font-size:16px;
    cursor:pointer;
    font-weight:600;
    transition:0.4s;
}

button:hover{
    transform:scale(1.05);
}

.loader{
    width:60px;
    height:60px;
    border:6px solid rgba(255,255,255,0.1);
    border-top:6px solid #38bdf8;
    border-radius:50%;
    animation:spin 1s linear infinite;
    margin:25px auto;
    display:none;
}

@keyframes spin{
    100%{
        transform:rotate(360deg);
    }
}

.dashboard{
    margin-top:40px;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
    gap:25px;
}

.card{
    background:#111827;
    padding:30px;
    border-radius:25px;
    transition:0.4s;
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

.chart-box{
    margin-top:40px;
    background:#111827;
    border-radius:25px;
    padding:30px;
}

.info-box{
    margin-top:30px;
    background:#111827;
    border-radius:25px;
    padding:30px;
    line-height:1.8;
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#64748b;
}

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <div class="header">

        <h1>Smart Electricity Intelligence</h1>

        <p>
            AI Powered Electricity Consumption Analytics Dashboard
        </p>

    </div>

    <div class="upload-box">

        <h2>Upload Electricity Dataset</h2>

        <input type="file" id="fileInput" accept=".csv">

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

    <div class="footer">

        Smart Electricity Monitoring Platform © 2026

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
            "Please upload CSV dataset.";

        return;
    }

    loader.style.display = "block";

    resultBox.innerHTML =
        "Analyzing electricity usage...";

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

                <div class="info-box">

                    <h2>AI Recommendation</h2>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        ${data.recommendation}
                    </p>

                </div>

                <div class="info-box">

                    <h2>Smart Insights</h2>

                    <p style="margin-top:15px;color:#cbd5e1;">
                        ${data.insight}
                    </p>

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
                data.error;
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
