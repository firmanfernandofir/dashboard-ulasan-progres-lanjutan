from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Load data dari CSV (pastikan file data.csv tersedia di root folder)
df = pd.read_csv("data.csv")

# Halaman utama
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visualisasi Data</title>
        </head>
        <body>
            <h1>Visualisasi Data CSV</h1>
            <form method="POST" action="/plot">
                <label for="x">Pilih Kolom X:</label>
                <select name="x">
                    {% for col in columns %}
                    <option value="{{ col }}">{{ col }}</option>
                    {% endfor %}
                </select>
                <label for="y">Pilih Kolom Y:</label>
                <select name="y">
                    {% for col in columns %}
                    <option value="{{ col }}">{{ col }}</option>
                    {% endfor %}
                </select>
                <button type="submit">Tampilkan Plot</button>
            </form>
        </body>
        </html>
    ''', columns=df.columns)

# Route untuk membuat grafik
@app.route('/plot', methods=['POST'])
def plot():
    x_col = request.form['x']
    y_col = request.form['y']

    fig = px.scatter(df, x=x_col, y=y_col, title=f'Scatter Plot: {x_col} vs {y_col}')
    plot_html = fig.to_html(full_html=False)

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hasil Plot</title>
        </head>
        <body>
            <h1>Hasil Visualisasi</h1>
            <div>{{ plot|safe }}</div>
            <a href="/">Kembali</a>
        </body>
        </html>
    ''', plot=plot_html)

# Tidak perlu app.run() karena akan dijalankan oleh Gunicorn
