import streamlit as st
import pandas as pd

# Judul Aplikasi
st.set_page_config(page_title="Visualisasi Circular Queue", layout="wide")
st.title("🔄 Visualisasi Antrean Circular Queue")
st.markdown("---")

# Inisialisasi State agar data tidak hilang saat refresh/tombol diklik
if 'size' not in st.session_state:
    st.session_state.size = 8
if 'queue' not in st.session_state:
    st.session_state.queue = [None] * st.session_state.size
if 'front' not in st.session_state:
    st.session_state.front = -1
if 'rear' not in st.session_state:
    st.session_state.rear = -1

# Sidebar untuk Kontrol
with st.sidebar:
    st.header("Kontrol Antrean")
    input_val = st.text_input("Masukkan Data (Elemen):")
    
    col1, col2 = st.columns(2)
    
    # Tombol Enqueue
    if col1.button("Enqueue (Tambah)"):
        if ((st.session_state.rear + 1) % st.session_state.size == st.session_state.front):
            st.error("Antrean Penuh! (Overflow)")
        elif input_val == "":
            st.warning("Isi data terlebih dahulu.")
        else:
            if st.session_state.front == -1:
                st.session_state.front = 0
            st.session_state.rear = (st.session_state.rear + 1) % st.session_state.size
            st.session_state.queue[st.session_state.rear] = input_val
            st.success(f"'{input_val}' ditambahkan.")

    # Tombol Dequeue
    if col2.button("Dequeue (Hapus)"):
        if st.session_state.front == -1:
            st.error("Antrean Kosong! (Underflow)")
        else:
            removed = st.session_state.queue[st.session_state.front]
            st.session_state.queue[st.session_state.front] = None
            if st.session_state.front == st.session_state.rear:
                st.session_state.front = -1
                st.session_state.rear = -1
            else:
                st.session_state.front = (st.session_state.front + 1) % st.session_state.size
            st.info(f"'{removed}' dihapus.")

    if st.button("Reset Queue"):
        st.session_state.queue = [None] * st.session_state.size
        st.session_state.front = -1
        st.session_state.rear = -1
        st.rerun()

# Tampilan Visual Utama
st.subheader("Representasi Memori (Array)")
cols = st.columns(st.session_state.size)

for i in range(st.session_state.size):
    with cols[i]:
        val = st.session_state.queue[i]
        label = f"Index {i}"
        
        # Penanda Front dan Rear
        status = ""
        if i == st.session_state.front and i == st.session_state.rear:
            status = "🎯 F & R"
        elif i == st.session_state.front:
            status = "➡️ Front"
        elif i == st.session_state.rear:
            status = "⬅️ Rear"
            
        color = "background-color: #2e7bcf; color: white;" if val is not None else "background-color: #f0f2f6;"
        st.markdown(
            f"""
            <div style="border: 1px solid #ccc; padding: 10px; text-align: center; border-radius: 5px; {color}">
                <strong>{val if val is not None else '-'}</strong>
            </div>
            <div style="text-align: center; font-size: 0.8em; margin-top: 5px;">
                {label}<br><span style="color:red;">{status}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

st.markdown("---")

# Ringkasan Status
st.subheader("Status Indeks")
data_status = {
    "Properti": ["Front Index", "Rear Index", "Kapasitas", "Status"],
    "Nilai": [
        st.session_state.front, 
        st.session_state.rear, 
        st.session_state.size,
        "Penuh" if ((st.session_state.rear + 1) % st.session_state.size == st.session_state.front) else ("Kosong" if st.session_state.front == -1 else "Tersedia")
    ]
}
st.table(pd.DataFrame(data_status))