import streamlit as st
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

st.title("Diagram Venn & Operasi Set")
st.write("Masukkan elemen untuk Set A dan Set B.")

set_a_input = st.text_input("Masukkan Set A (pisahkan dengan koma):", "apel, jeruk, mangga, pisang")
set_b_input = st.text_input("Masukkan Set B (pisahkan dengan koma):", "mangga, pisang, anggur, melon")

set_a = set([x.strip().lower() for x in set_a_input.split(",") if x.strip()])
set_b = set([x.strip().lower() for x in set_b_input.split(",") if x.strip()])

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.write("**Union (A ∪ B):**")
    st.info(set_a | set_b)
    st.write("**Intersection (A ∩ B):**")
    st.success(set_a & set_b)

with col2:
    st.write("**Difference (A - B):**")
    st.warning(set_a - set_b)
    st.write("**Symmetric Difference (A △ B):**")
    st.error(set_a ^ set_b)

st.divider()

if set_a or set_b:
    fig, ax = plt.subplots(figsize=(6, 4))
    venn2([set_a, set_b], ('Set A', 'Set B'), ax=ax)
    st.pyplot(fig)