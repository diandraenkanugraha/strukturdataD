import streamlit as st
import pandas as pd
import re

# Header dengan emoji
st.title("📊 Social Media Word Count")
st.markdown("Analisis frekuensi kata dari komentar netizen secara instan! ✨")

# Input komentar
user_comments = st.text_area("💬 Masukkan komentar di sini:", 
    "Wah keren banget aplikasinya! Keren dan simpel banget.")

# Tombol dengan emoji
if st.button("🚀 Hitung Kata Sekarang"):
    if user_comments.strip() == "":
        st.warning("Isi dulu komentarnya ya! ⚠️")
    else:
        # Preprocessing: hapus tanda baca & kecilkan huruf
        clean_text = re.sub(r'[^\w\s]', '', user_comments.lower())
        words = clean_text.split()
        
        # Hitung frekuensi (Key: kata, Value: frekuensi)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Konversi ke DataFrame untuk visualisasi
        df = pd.DataFrame(list(word_freq.items()), columns=['Kata', 'Frekuensi'])
        df = df.sort_values(by='Frekuensi', ascending=False)

        # Layout kolom untuk hasil
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Tabel Frekuensi")
            st.dataframe(df, use_container_width=True)

        with col2:
            st.subheader("📈 Visualisasi")
            st.bar_chart(df.set_index('Kata'))
            
        st.success("Analisis selesai! 🏁")