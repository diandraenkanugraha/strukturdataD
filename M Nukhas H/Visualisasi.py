import streamlit as st

st.title("Visualisasi Operasi Set")
st.write("Masukkan elemen set (pisahkan dengan koma)")

# Input
set1_input = st.text_input("Set A", "1,2,3,4")
set2_input = st.text_input("Set B", "3,4,5,6")

# Konversi ke set
setA = set(map(int, set1_input.split(",")))
setB = set(map(int, set2_input.split(",")))

# Operasi
union = setA | setB
intersection = setA & setB
difference = setA - setB
sym_diff = setA ^ setB

# Output
st.subheader("Hasil Operasi")
st.write("Union:", union)
st.write("Intersection:", intersection)
st.write("Difference (A - B):", difference)
st.write("Symmetric Difference:", sym_diff)