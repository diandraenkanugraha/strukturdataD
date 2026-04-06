import streamlit as st
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import re

st.title("Visualisasi Word Count Komentar Sosial Media")

# Input teks
text = st.text_area("Masukkan komentar sosial media:")

if text:
    # Preprocessing sederhana
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)

    # Hitung frekuensi kata
    word_count = Counter(words)

    # Ubah ke DataFrame
    df = pd.DataFrame(word_count.items(), columns=["Kata", "Frekuensi"])
    df = df.sort_values(by="Frekuensi", ascending=False)

    st.subheader("Tabel Word Count")
    st.write(df)

    # Visualisasi bar chart
    st.subheader("Bar Chart Frekuensi Kata")
    top_n = st.slider("Jumlah kata teratas", 5, 20, 10)

    df_top = df.head(top_n)

    fig, ax = plt.subplots()
    ax.bar(df_top["Kata"], df_top["Frekuensi"])
    plt.xticks(rotation=45)
    st.pyplot(fig)