from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

# Cek apakah data.csv tersedia
DATA_FILE = 'data.csv'
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    print("Cek apakah data.csv ada: True")
else:
    print("Cek apakah data.csv ada: False")
    df = pd.DataFrame()

@app.route('/')
def home():
    return "<h1>Aplikasi Flask Berjalan di Railway!</h1><p>Gunakan endpoint /data untuk melihat isi CSV</p>"

@app.route('/data', methods=['GET'])
def show_data():
    if df.empty:
        return jsonify({"error": "data.csv tidak ditemukan atau kosong"}), 404
    return df.to_json(orient='records')

# Tambahkan endpoint lain sesuai kebutuhan
# Misalnya untuk prediksi, upload file, dsb.

# Ini penting agar Flask bisa jalan saat di Railway
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
