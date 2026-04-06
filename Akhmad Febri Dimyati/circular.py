import streamlit as st

class CircularQueue:
    def __init__(self, k):
        self.k = k
        self.queue = [None] * k
        self.head = -1
        self.tail = -1

    def enqueue(self, value):
        if ((self.tail + 1) % self.k == self.head):
            return "Penuh"
        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = value
        else:
            self.tail = (self.tail + 1) % self.k
            self.queue[self.tail] = value
        return "Berhasil"

    def dequeue(self):
        if (self.head == -1):
            return "Kosong"
        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.queue[self.head] = None
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.queue[self.head] = None
            self.head = (self.head + 1) % self.k
            return temp

# Konfigurasi Streamlit
st.set_page_config(page_title="Circular Queue Visualizer")
st.title("🔄 Circular Queue Visualization")

if 'cq' not in st.session_state:
    st.session_state.cq = CircularQueue(5)

# Kontrol
col1, col2 = st.columns(2)
with col1:
    val = st.text_input("Input Data")
    if st.button("Enqueue (Tambah)"):
        res = st.session_state.cq.enqueue(val)
        if res == "Penuh": st.error("Antrian Penuh!")
with col2:
    st.write("Aksi")
    if st.button("Dequeue (Hapus)"):
        res = st.session_state.cq.dequeue()
        if res == "Kosong": st.error("Antrian Kosong!")

# Visualisasi
st.subheader("Status Antrian Saat Ini:")
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        label = ""
        if i == st.session_state.cq.head: label += "➡️ HEAD"
        if i == st.session_state.cq.tail: label += " ⬅️ TAIL"
        
        color = "blue" if st.session_state.cq.queue[i] else "gray"
        st.markdown(f"""
            <div style="border:2px solid black; height:100px; border-radius:10px; 
            text-align:center; background-color:{color}; color:white; line-height:100px;">
                {st.session_state.cq.queue[i] if st.session_state.cq.queue[i] else '-'}
            </div>
            <p style="text-align:center;">Index {i}<br><b>{label}</b></p>
        """, unsafe_allow_html=True)

st.info("Konsep Circular Queue: Elemen terakhir terhubung kembali ke awal (Wrap-around).")