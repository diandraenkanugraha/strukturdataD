import streamlit as st
import time

# 1. Definisi Node untuk Linked List
class Node:
    def __init__(self, warna, durasi, hex_code):
        self.warna = warna
        self.durasi = durasi
        self.hex_code = hex_code
        self.next = None

# 2. Definisi Circular Linked List
class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi, hex_code):
        new_node = Node(warna, durasi, hex_code)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

# 3. Inisialisasi Data Sesuai Tugas
cll = CircularLinkedList()
cll.tambah_lampu("Merah", 40, "#FF0000")
cll.tambah_lampu("Hijau", 20, "#00FF00")
cll.tambah_lampu("Kuning", 5, "#FFFF00")

# --- UI Streamlit ---
st.set_page_config(page_title="Visualisasi Lampu Merah", page_icon="🚦")
st.title("🚦 Visualisasi Lampu Lalu Lintas")
st.write("Menggunakan Struktur Data **Circular Linked List**")

# Inisialisasi state untuk kontrol loop
if 'running' not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns(2)
with col1:
    if st.button("Mulai Simulasi"):
        st.session_state.running = True
with col2:
    if st.button("Berhenti"):
        st.session_state.running = False

placeholder = st.empty()

# 4. Logika Simulasi
if st.session_state.running:
    current = cll.head
    while st.session_state.running:
        for i in range(current.durasi, 0, -1):
            with placeholder.container():
                # Visualisasi Lampu
                st.markdown(
                    f"""
                    <div style="
                        display: flex; 
                        flex-direction: column; 
                        align-items: center; 
                        background-color: #333; 
                        padding: 20px; 
                        border-radius: 50px; 
                        width: 120px;
                        margin: auto;
                    ">
                        <div style="width: 80px; height: 80px; background-color: {current.hex_code if current.warna == 'Merah' else '#555'}; border-radius: 50%; margin: 10px;"></div>
                        <div style="width: 80px; height: 80px; background-color: {current.hex_code if current.warna == 'Kuning' else '#555'}; border-radius: 50%; margin: 10px;"></div>
                        <div style="width: 80px; height: 80px; background-color: {current.hex_code if current.warna == 'Hijau' else '#555'}; border-radius: 50%; margin: 10px;"></div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown(f"<h2 style='text-align: center;'>Lampu {current.warna}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align: center;'>{i}</h1>", unsafe_allow_html=True)
            
            time.sleep(1)
        
        # Pindah ke node berikutnya (Circular)
        current = current.next
else:
    st.info("Klik tombol 'Mulai Simulasi' untuk menjalankan program.")