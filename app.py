from flask import Flask, request, jsonify, render_template_string
from PIL import Image
import os
import re
from datetime import datetime

app = Flask(__name__)

HTML_PAGE = """

<!DOCTYPE html>
<html>

<head>

<title>Electricity Bill Analyzer</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
    background:#0f172a;
    color:white;
    font-family:Arial;
    margin:0;
    padding:20px;
}

.container{
    max-width:900px;
    margin:auto;
}

.box{
    background:#1e293b;
    padding:30px;
    border-radius:15px;
    margin-top:20px;
}

button{
    padding:12px 25px;
    border:none;
    border-radius:10px;
    background:#2563eb;
    color:white;
    cursor:pointer;
    margin-top:15px;
}

.card{
    background:#334155;
    padding:20px;
    border-radius:15px;
    margin-top:15px;
}

</style>

</head>

<body>

<div class="container">

    <h1>Electricity Bill Analyzer</h1>

    <div class="box">

        <input type="file" id="imageInput">

        <br>

        <button onclick="uploadImage()">
            Analyze Bill
        </button>

    </div>

    <div class="box" id="result">

        Waiting for upload...

    </div>

</div>

<script>

async function uploadImage(){

    const fileInput =
        document.getElementById("imageInput");

    const result =
        document.getElementById("result");

    if(fileInput.files.length === 0){

        result.innerHTML =
            "Please upload image";

        return;
    }

    result.innerHTML =
        "Analyzing...";

    const formData = new FormData();

    formData.append(
        "image",
        fileInput.files[0]
    );

    try{

        const response =
            await fetch("/analyze",{

            method:"POST",

            body:formData

        });

        const data = await response.json();

        if(data.success){

            result.innerHTML = `

                <div class="card">

                    <h2>Analysis Completed</h2>

                    <p><b>Units:</b>
                    ${data.units} kWh</p>

                    <p><b>Amount:</b>
                    ₹${data.amount}</p>

                    <p><b>Status:</b>
                    ${data.status}</p>

                    <p><b>Recommendation:</b>
                    ${data.recommendation}</p>

                    <p><b>Date:</b>
                    ${data.date}</p>

                </div>

            `;
        }

        else{

            result.innerHTML =
                data.error;
        }

    }

    catch(error){

        result.innerHTML =
            "Server Error";
    }
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

        if "image" not in request.files:

            return jsonify({

                "success": False,
                "error": "No image uploaded"

            })

        file = request.files["image"]

        image = Image.open(file)

        width, height = image.size

        # ============================================
        # LIGHTWEIGHT ANALYSIS
        # ============================================

        estimated_units = int((width + height) / 10)

        estimated_amount = estimated_units * 8

        # ============================================
        # USAGE STATUS
        # ============================================

        if estimated_units > 400:

            status = "High Usage"

            recommendation = (
                "Reduce AC and heavy appliance usage."
            )

        elif estimated_units > 200:

            status = "Moderate Usage"

            recommendation = (
                "Switch to LED bulbs and save power."
            )

        else:

            status = "Low Usage"

            recommendation = (
                "Electricity usage is optimized."
            )

        return jsonify({

            "success": True,

            "units": estimated_units,

            "amount": estimated_amount,

            "status": status,

            "recommendation": recommendation,

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
