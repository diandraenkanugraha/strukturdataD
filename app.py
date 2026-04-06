import streamlit as st

st.title("Operasi Set")

# Input Set A dan B
a_input = st.text_input("Set A (pisah dengan koma):", "11, 12, 13, 14, 15")
b_input = st.text_input("Set B (pisah dengan koma):", "24, 25, 26, 27, 28")

# Inisiasi set 
set_a = set(x.strip() for x in a_input.split(",") if x.strip())
set_b = set(x.strip() for x in b_input.split(",") if x.strip())

st.write(f"Set A: {set_a}")
st.write(f"Set B: {set_b}")

st.subheader("Hasil Operasi:")

# Union - menggunakan tanda |
union = set_a | set_b
st.write(f"Union (A | B): {union}")

# Intersection - menggunakan tanda &
intersection = set_a & set_b
st.write(f"Intersection (A & B): {intersection}")

# Difference - menggunakan tanda -
difference_ab = set_a - set_b
st.write(f"Difference (A - B): {difference_ab}")

difference_ba = set_b - set_a
st.write(f"Difference (B - A): {difference_ba}")

# Symmetric Difference - menggunakan tanda ^
sym_diff = set_a ^ set_b
st.write(f"Symmetric Difference (A ^ B): {sym_diff}")

# Tabel keanggotaan
st.subheader("Tabel Keanggotaan:")
semua = sorted(union)
if semua:
    tabel = "| Elemen | A | B | A∪B | A∩B | A-B | B-A | A△B |\n|---|---|---|---|---|---|---|---|\n"
    for e in semua:
        tabel += f"| {e} | {'✓' if e in set_a else '✕'} | {'✓' if e in set_b else '✕'} | {'✓' if e in union else '✕'} | {'✓' if e in intersection else '✕'} | {'✓' if e in difference_ab else '✕'} | {'✓' if e in difference_ba else '✕'} | {'✓' if e in sym_diff else '✕'} |\n"
    st.markdown(tabel)