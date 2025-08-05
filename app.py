from flask import Flask, request, render_template_string
import pandas as pd
import os

# Cek apakah file tersedia
print("Cek apakah data.csv ada:", os.path.exists("data.csv"))

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data.csv")

# Home page
@app.route("/")
def index():
    return render_template_string("""
        <h2>Data Preview</h2>
        <table border="1">
        {{ table|safe }}
        </table>
    """, table=df.head().to_html())

# Predict example
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    # Misal: prediksi dummy
    return {"prediction": "Contoh prediksi"}

# WSGI app (tidak pakai app.run())
# Gunicorn akan menjalankan: app
