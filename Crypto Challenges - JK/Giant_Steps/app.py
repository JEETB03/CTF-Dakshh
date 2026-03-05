from flask import Flask, render_template, send_file
import subprocess
import os

app = Flask(__name__)

# Run generator on startup to create output.txt if it doesn't exist
try:
    subprocess.run(["python", "gen_challenge.py"], check=True)
except Exception as e:
    print(f"Error running gen_challenge.py: {e}")

@app.route("/")
def index():
    params = {}
    try:
        with open("output.txt", "r") as f:
            for line in f:
                if " = " in line:
                    key, val = line.strip().split(" = ")
                    params[key] = val
    except FileNotFoundError:
        params = {"Error": "output.txt not found. Did gen_challenge.py run?"}
    
    return render_template("index.html", params=params)

@app.route("/download")
def download():
    return send_file("challenge.py", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
