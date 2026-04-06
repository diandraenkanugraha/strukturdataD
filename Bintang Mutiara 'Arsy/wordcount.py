import streamlit as st

st.title("Word Count Komentar Sosial Media")
st.write("Key = kata | Value = frekuensi")

# Input komentar
komentar = st.text_area("Masukkan komentar sosial media:", 
"""Produk ini bagus sangat memuaskan,
pelayanan ramah dan cepat, produk bagus,,
kualitas bagus, pengiriman cepat,
harga murah, sangat recommended.
Saya puas dengan produk ini sellernya ramah""")

if st.button("Hitung Word Count"):

    # Proses teks menjadi list kata
    kata_list = komentar.lower().split()

    # Inisiasi dictionary - Key: kata, Value: frekuensi
    word_count = {}

    # Hitung frekuensi tiap kata
    for kata in kata_list:
        if kata in word_count:
            word_count[kata] = word_count[kata] + 1
        else:
            word_count[kata] = 1

    # Urutkan dari terbanyak
    word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))

    # Tampilkan dictionary
    st.subheader("Dictionary Word Count:")
    st.write(word_count)

    # Tampilkan tabel
    st.subheader("Tabel:")
    tabel = "| Kata (Key) | Frekuensi (Value) |\n|---|---|\n"
    for kata, frekuensi in word_count.items():
        tabel += f"| {kata} | {frekuensi} |\n"
    st.markdown(tabel)

    # Bar chart bawaan streamlit
    st.subheader("Bar Chart:")
    st.bar_chart(word_count)