from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>UniEvent System</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, #667eea, #764ba2);
            text-align: center;
            color: white;
        }
        .card {
            background: white;
            color: black;
            margin: 20px;
            padding: 20px;
            border-radius: 15px;
            display: inline-block;
            width: 250px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <h1>🎓 UniEvent Dashboard</h1>
    <div class="card">
        <h2>Hackathon</h2>
        <p>Date: April 10</p>
    </div>
    <div class="card">
        <h2>AI Workshop</h2>
        <p>Date: April 15</p>
    </div>
    <div class="card">
        <h2>Tech Talk</h2>
        <p>Date: April 20</p>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)