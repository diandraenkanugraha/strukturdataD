import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

st.set_page_config(
    page_title="Word Count Komentar",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Visualisasi Word Count Komentar Sosial Media")

st.write("""
Program ini menghitung jumlah kemunculan setiap kata.
Key   = Kata  
Value = Frekuensi kemunculan kata
""")

# ======================
# CONTOH INPUT OTOMATIS
# ======================
contoh_teks = """Saya suka belajar data science
Belajar data itu menyenangkan
Saya suka coding dan data"""

teks = st.text_area("Masukkan komentar:", value=contoh_teks, height=200)

if st.button("Hitung Word Count"):

    if teks.strip() == "":
        st.warning("Masukkan teks terlebih dahulu.")
    else:
        # 1. Ubah ke huruf kecil
        teks = teks.lower()

        # 2. Hapus tanda baca
        teks = re.sub(r"[^\w\s]", "", teks)

        # 3. Pisahkan kata
        daftar_kata = teks.split()

        # 4. Hitung frekuensi
        frekuensi = Counter(daftar_kata)

        # 5. Buat DataFrame
        df = pd.DataFrame(
            frekuensi.items(),
            columns=["Kata (Key)", "Frekuensi (Value)"]
        )

        df = df.sort_values(by="Frekuensi (Value)", ascending=False)

        # ======================
        # TAMPILKAN HASIL
        # ======================
        st.subheader("📋 Tabel Word Count")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Grafik 10 Kata Teratas")

        top10 = df.head(10)

        fig, ax = plt.subplots()
        ax.bar(top10["Kata (Key)"], top10["Frekuensi (Value)"])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.success(f"Total kata unik: {len(df)}")