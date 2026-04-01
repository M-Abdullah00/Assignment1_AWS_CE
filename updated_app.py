from flask import Flask, render_template_string, request, redirect, url_for
import boto3
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "giki_20223329_secret" # Using your reg ID as a secret key seed

# --- AWS CONFIGURATION ---
BUCKET_NAME = "unievent-images-12345"
# Explicitly pinning to us-east-1 for stability
s3 = boto3.client('s3', region_name='us-east-1')

# --- GIKI THEMED STYLING (Blue, Gold, and Neon) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIKI UniEvent | Cloud Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --giki-blue: #003366;
            --giki-gold: #FFD700;
            --neon-blue: #00f2ff;
        }
        body { 
            background: #0f172a; /* Dark sleek background */
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
        }
        .navbar {
            background-color: var(--giki-blue) !important;
            border-bottom: 3px solid var(--giki-gold);
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        }
        .hero-banner {
            background: linear-gradient(135deg, #003366 0%, #001a33 100%);
            padding: 60px 0;
            border-bottom-right-radius: 80px;
            text-align: center;
            border-bottom: 2px solid var(--neon-blue);
        }
        .giki-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 15px;
            transition: 0.3s;
        }
        .giki-card:hover {
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
            transform: translateY(-5px);
        }
        .btn-giki {
            background-color: var(--giki-gold);
            color: var(--giki-blue);
            font-weight: bold;
            border-radius: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn-giki:hover {
            background-color: #fff;
            color: #000;
            box-shadow: 0 0 10px var(--giki-gold);
        }
        .upload-section {
            background: rgba(255, 255, 255, 0.05);
            border: 2px dashed var(--giki-gold);
            padding: 25px;
            border-radius: 20px;
        }
        .badge-society {
            background: var(--neon-blue);
            color: #000;
            font-weight: bold;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-dark">
    <div class="container">
        <a class="navbar-brand fw-bold" href="#">
            <span style="color: var(--giki-gold);">GIKI</span> UniEvent System
        </a>
    </div>
</nav>

<div class="hero-banner mb-5">
    <div class="container">
        <h1 class="display-4 fw-bold">GIKI Engineering Portal</h1>
        <p class="lead text-info">Managing Softcom '26 & Digital Signal Processing Assets</p>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col-lg-4 mb-4">
            <div class="upload-section shadow-sm">
                <h4 class="mb-3" style="color: var(--giki-gold);">S3 Data Gateway</h4>
                <p class="small text-muted">Upload CSV data or event posters.</p>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <input type="file" name="file" class="form-control bg-dark text-white border-secondary" required>
                    </div>
                    <button type="submit" class="btn btn-giki w-100 py-2">Upload</button>
                </form>
            </div>
        </div>

        <div class="col-lg-8">
            <h3 class="mb-4" style="border-left: 5px solid var(--giki-gold); padding-left: 15px;">Upcoming GIKI Events</h3>
            
            {% for event in events %}
            <div class="card giki-card mb-4 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title text-info fw-bold">{{ event.title }}</h5>
                        <span class="badge badge-society">{{ event.society }}</span>
                    </div>
                    <p class="card-text mt-3 text-light opacity-75">{{ event.description }}</p>
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <small class="text-warning">📍 {{ event.location }}</small>
                        <small class="text-muted">{{ event.date }}</small>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<footer class="text-center py-5 mt-5 border-top border-secondary">
    <p class="text-muted small">© 2026 M Abdullah Zafar | GIKI Registration: 20223329</p>
    <p class="text-muted" style="font-size: 10px;">AWS Region: us-east-1 | S3 Bucket: unievent-images-12345</p>
</footer>

</body>
</html>
"""

@app.route('/')
def home():
    # Tailored GIKI event data based on your specific projects
    giki_events = [
        {
            "title": "Softcom '26 Flagship", 
            "society": "ACM/SOFTCOM", 
            "description": "The premier national software competition. Join us for 48 hours of coding, logic, and innovation.",
            "location": "AIA Auditorium",
            "date": "Dec 19 - 21"
        },
        {
            "title": "Radar Signal Processing Workshop", 
            "society": "DSP Lab", 
            "description": "Analysis of FIR vs IIR filter performance in high-noise environments. Bring your MATLAB scripts.",
            "location": "FES Lab 2",
            "date": "Ongoing"
        },
        {
            "title": "ACM Induction Interviews", 
            "society": "ACM", 
            "description": "Final round of interviews for the Executive Council and Sub-Council positions.",
            "location": "Society Office",
            "date": "Immediate"
        },
        {
            "title": "Netcom VLSI Design Series", 
            "society": "NETCOM", 
            "description": "Deep dive into SystemVerilog and FSM logic for high-speed RISC-V control units.",
            "location": "Seminar Hall",
            "date": "April 15"
        }
    ]

    # Optional: Log the view to S3 as a JSON audit file
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key='logs/portal_view.json',
            Body=json.dumps({"user": "Abdullah", "event_count": len(giki_events)})
        )
    except:
        pass # Silent fail if S3 is busy

    return render_template_string(HTML_TEMPLATE, events=giki_events)

@app.route('/upload', methods=['POST'])
def upload():
    # --- Fix for ParamValidationError ---
    # We check if 'file' exists in request and if the filename isn't empty
    if 'file' not in request.files:
        return "<h3>Error: No file part in the request.</h3>", 400
    
    file = request.files['file']
    if file.filename == '':
        return "<h3>Error: No file selected. Please choose a file first!</h3><a href='/'>Go Back</a>", 400

    if file:
        filename = secure_filename(file.filename)
        
        try:
            # --- Fix for 502/Timeout ---
            # We perform the upload, then return a "Success" page rather than a fast redirect
            s3.upload_fileobj(file, BUCKET_NAME, filename)
            
            return f"""
            <div style="background:#0f172a; color:white; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; font-family:sans-serif;">
                <h1 style="color:#FFD700;">✔ GIKI Cloud Success!</h1>
                <p>File <b>{filename}</b> has been successfully stored in <b>us-east-1</b>.</p>
                <br>
                <a href="/" style="text-decoration:none; color:#003366; background:#FFD700; padding:12px 25px; border-radius:8px; font-weight:bold;">Return to Portal</a>
            </div>
            """
        except Exception as e:
            return f"<div style='color:red;'><h3>S3 Upload Failed:</h3><p>{str(e)}</p></div>", 500

if __name__ == '__main__':
    # Running on Port 80 for public EC2 access
    app.run(host='0.0.0.0', port=80)
