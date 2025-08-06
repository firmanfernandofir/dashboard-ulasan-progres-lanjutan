import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

st.set_page_config(layout="wide", page_title="Ulasan Google Maps PDAM")

# === Load Data ===
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# === Fungsi Parsing Tanggal Relatif ===
def parse_relative_date(date_str):
    if not isinstance(date_str, str):
        return pd.NaT

    if "minggu" in date_str:
        match = re.findall(r"\d+", date_str)
        if match:
            weeks = int(match[0])
            return pd.Timestamp.now() - pd.Timedelta(weeks=weeks)
    elif "bulan" in date_str:
        match = re.findall(r"\d+", date_str)
        if match:
            months = int(match[0])
            return pd.Timestamp.now() - pd.DateOffset(months=months)
    elif "tahun" in date_str:
        match = re.findall(r"\d+", date_str)
        if match:
            years = int(match[0])
            return pd.Timestamp.now() - pd.DateOffset(years=years)

    return pd.NaT

# === Parsing dan Persiapan Data ===
df["parsed_date"] = df["date"].apply(parse_relative_date)
df["bulan_tahun"] = df["parsed_date"].dt.to_period("M")

# === HEADER ===
st.title("📊 Visualisasi Ulasan Google Maps PDAM")
st.markdown("Data ini menampilkan ulasan dari pengguna Google Maps terkait layanan PDAM.")

# === Grafik Jumlah Ulasan per Bulan ===
monthly_count = df.groupby("bulan_tahun").size().reset_index(name="jumlah_ulasan")
monthly_count = monthly_count.sort_values("bulan_tahun")

st.subheader("📈 Jumlah Ulasan per Bulan")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly_count["bulan_tahun"].astype(str), monthly_count["jumlah_ulasan"], marker="o", linestyle='-')
plt.xticks(rotation=45)
plt.xlabel("Bulan-Tahun")
plt.ylabel("Jumlah Ulasan")
plt.grid(True)
st.pyplot(fig)

# === Filter Berdasarkan Rating (Opsional) ===
with st.expander("🔎 Filter Berdasarkan Rating"):
    selected_ratings = st.multiselect("Pilih Rating", sorted(df["rating"].dropna().unique()), default=sorted(df["rating"].dropna().unique()))
    df = df[df["rating"].isin(selected_ratings)]

# === Tampilkan Tabel Ulasan Lengkap ===
st.subheader("🗣️ Daftar Ulasan Lengkap")
for _, row in df.sort_values("parsed_date", ascending=False).iterrows():
    st.markdown(f"""
    <div style='border:1px solid #ccc;padding:10px;border-radius:10px;margin-bottom:10px'>
    <strong>👤 {row['name']}</strong><br>
    ⭐ <b>Rating:</b> {row['rating']}<br>
    📅 <b>Tanggal:</b> {row['date']}<br>
    🔗 <a href="{row['link']}" target="_blank">Lihat Profil Reviewer</a><br>
    📝 <i>{row['snippet']}</i>
    </div>
    """, unsafe_allow_html=True)
