import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

st.set_page_config(layout="wide", page_title="Ulasan Google PDAM")

# === Load data ===
df = pd.read_csv("data.csv")

# === Parse tanggal ===
def parse_relative_date(date_str):
    if "minggu" in date_str:
        weeks = int(re.findall(r"\d+", date_str)[0])
        return pd.Timestamp.now() - pd.Timedelta(weeks=weeks)
    elif "bulan" in date_str:
        months = int(re.findall(r"\d+", date_str)[0])
        return pd.Timestamp.now() - pd.DateOffset(months=months)
    elif "tahun" in date_str:
        years = int(re.findall(r"\d+", date_str)[0])
        return pd.Timestamp.now() - pd.DateOffset(years=years)
    else:
        return pd.NaT

df["parsed_date"] = df["date"].apply(parse_relative_date)
df["bulan_tahun"] = df["parsed_date"].dt.to_period("M")

# === Grafik ===
st.title("📊 Visualisasi Ulasan Google Maps PDAM")
st.markdown("Grafik ini menunjukkan jumlah ulasan setiap bulannya.")

monthly_count = df.groupby("bulan_tahun").size().reset_index(name="jumlah_ulasan")
monthly_count = monthly_count.sort_values("bulan_tahun")

fig, ax = plt.subplots()
ax.plot(monthly_count["bulan_tahun"].astype(str), monthly_count["jumlah_ulasan"], marker="o")
plt.xticks(rotation=45)
plt.xlabel("Bulan-Tahun")
plt.ylabel("Jumlah Ulasan")
plt.grid(True)
st.pyplot(fig)

# === Tabel Ulasan ===
st.subheader("🗣️ Daftar Ulasan Lengkap")
for _, row in df.sort_values("parsed_date", ascending=False).iterrows():
    st.markdown(f"""
    **👤 {row['name']}**  
    ⭐ Rating: {row['rating']}  
    📅 Tanggal: {row['date']}  
    🔗 [Lihat Profil Reviewer]({row['link']})  
    📝 *{row['snippet']}*
    ---
    """)
