import streamlit as st
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

st.set_page_config(page_title="Operasi Set", layout="centered")
st.title("🔢 Visualisasi Operasi Set")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    a_input = st.text_input("Set A (pisah koma)", "1, 2, 3, 4, 5")
with col2:
    b_input = st.text_input("Set B (pisah koma)", "4, 5, 6, 7, 8")

A = set(x.strip() for x in a_input.split(",") if x.strip())
B = set(x.strip() for x in b_input.split(",") if x.strip())

operasi = {
    "Union (A ∪ B)":                  A | B,
    "Intersection (A ∩ B)":           A & B,
    "Difference (A - B)":             A - B,
    "Difference (B - A)":             B - A,
    "Symmetric Difference (A △ B)":   A ^ B,
}

pilihan = st.selectbox("Pilih Operasi Set", list(operasi.keys()))
hasil = operasi[pilihan]

st.markdown("---")

fig, ax = plt.subplots(figsize=(6, 4))
v = venn2([A, B], set_labels=("Set A", "Set B"), ax=ax)
ax.set_title(pilihan, fontsize=13, fontweight="bold")
st.pyplot(fig)

st.success(f"**Hasil {pilihan}:** `{sorted(hasil)}`")
st.info(f"Jumlah elemen: **{len(hasil)}**")

st.markdown("---")
st.markdown("### 📋 Semua Hasil Operasi")
for nama, res in operasi.items():
    st.write(f"- **{nama}:** {sorted(res)}")