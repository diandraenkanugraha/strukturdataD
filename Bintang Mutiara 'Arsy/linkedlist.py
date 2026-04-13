import streamlit as st
import time

# Definisi Node untuk Linked List
class Node:
    def __init__(self, warna, durasi, color_code):
        self.warna = warna
        self.durasi = durasi
        self.color_code = color_code
        self.next = None

# Setup Circular Linked List
merah = Node("Merah", 40, "#FF0000")
hijau = Node("Hijau", 20, "#00FF00")
kuning = Node("Kuning", 5, "#FFFF00")

merah.next = hijau
hijau.next = kuning
kuning.next = merah

st.title("Visualisasi Lampu Merah")
display_area = st.empty()

# Loop simulasi
current = merah
while True:
    durasi_sekarang = current.durasi
    while durasi_sekarang > 0:
        with display_area.container():
            st.markdown(
                f"""
                <div style="background-color: {current.color_code}; padding: 50px; border-radius: 50%; 
                width: 150px; height: 150px; margin: auto; text-align: center; display: flex; 
                align-items: center; justify-content: center; border: 5px solid black;">
                    <h1 style="color: black; margin: 0;">{durasi_sekarang}</h1>
                </div>
                <h2 style="text-align: center;">Lampu {current.warna}</h2>
                """,
                unsafe_allow_html=True
            )
        time.sleep(1)
        durasi_sekarang -= 1
    
    # Pindah ke node berikutnya dalam circular list
    current = current.next