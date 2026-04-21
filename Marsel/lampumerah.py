import streamlit as st
import time

# 1. Definisi Struktur Node
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

# 2. Definisi Circular Linked List
class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi):
        new_node = Node(warna, durasi)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

# --- Inisialisasi Data ---
cll = CircularLinkedList()
cll.tambah_lampu("Merah", 40)
cll.tambah_lampu("Hijau", 20)
cll.tambah_lampu("Kuning", 5)

# --- UI Streamlit ---
st.title("🚦 Visualisasi Lampu Merah (Circular Linked List)")

if st.button('Mulai Simulasi'):
    current = cll.head
    placeholder = st.empty() # Wadah buat update tampilan secara realtime
    
    while True: # Loop terus menerus
        with placeholder.container():
            # Tentukan warna hex buat visualisasi
            color_hex = {"Merah": "#FF0000", "Hijau": "#00FF00", "Kuning": "#FFFF00"}[current.warna]
            
            st.subheader(f"Lampu Sekarang: {current.warna}")
            
            # Bikin lingkaran warna
            st.markdown(
                f"""
                <div style="width: 150px; height: 150px; background-color: {color_hex}; 
                border-radius: 50%; margin: 20px auto; border: 5px solid white;"></div>
                """, 
                unsafe_allow_html=True
            )
            
            # Countdown timer sederhana
            for i in range(current.durasi, 0, -1):
                st.write(f"Sisa waktu: {i} detik")
                time.sleep(1)
                st.rerun if i == 1 else None # Trick buat refresh UI
        
        current = current.next