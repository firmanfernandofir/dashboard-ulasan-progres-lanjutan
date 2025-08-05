from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Fungsi konversi tanggal relatif
def relative_date_to_absolute(text):
    today = datetime.today()
    try:
        if "hari" in text:
            num = int(re.findall(r'\d+', text)[0])
            return today - timedelta(days=num)
        elif "minggu" in text:
            num = int(re.findall(r'\d+', text)[0])
            return today - timedelta(weeks=num)
        elif "bulan" in text:
            num = int(re.findall(r'\d+', text)[0])
            return today - timedelta(weeks=4*num)
        elif "tahun" in text:
            num = int(re.findall(r'\d+', text)[0])
            return today - timedelta(weeks=52*num)
    except:
        return today
    return today

@app.route('/')
def index():
    try:
        # Load data
        df = pd.read_csv("data.csv")

        if 'date' not in df.columns or 'snippet' not in df.columns or 'link' not in df.columns:
            return "<h3>Kolom 'date', 'snippet', atau 'link' tidak ditemukan dalam data.csv</h3>"

        # Konversi tanggal
        df['Tanggal'] = df['date'].apply(relative_date_to_absolute)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        df['Week'] = df['Tanggal'].dt.to_period("W").dt.start_time

        # Siapkan teks hover
        df['hover'] = (
            "Tanggal: " + df['Tanggal'].dt.strftime('%d-%m-%Y') +
            "<br>Ulasan: " + df['snippet'].astype(str).str.slice(0, 100) + "..." +
            "<br><a href='" + df['link'].astype(str) + "' target='_blank'>Klik untuk sumber</a>"
        )

        # Agregasi jumlah ulasan per minggu
        df_grouped = df.groupby('Week').agg({
            'snippet': 'count',
            'hover': lambda x: '<br><br>'.join(x)
        }).reset_index().rename(columns={'snippet': 'JumlahUlasan'})

        # Plotly chart
        fig = px.bar(df_grouped, x='Week', y='JumlahUlasan', hover_data={'hover': True, 'JumlahUlasan': False})
        fig.update_traces(hovertemplate='%{customdata[0]}<extra></extra>')
        fig.update_layout(
            title="Jumlah Ulasan Per Minggu",
            xaxis_title="Minggu",
            yaxis_title="Jumlah Ulasan",
            hoverlabel=dict(align="left")
        )

        chart_html = fig.to_html(full_html=False)

        return render_template_string("""
        <html>
        <head><title>Visualisasi Ulasan PDAM</title></head>
        <body>
            <h2>Grafik Interaktif Jumlah Ulasan</h2>
            {{ plot | safe }}
        </body>
        </html>
        """, plot=chart_html)

    except Exception as e:
        return f"<h3>Terjadi error: {e}</h3>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
