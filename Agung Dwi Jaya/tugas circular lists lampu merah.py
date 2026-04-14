import streamlit as st
import time

class Node:
    def __init__(self, color, duration):
        self.color = color
        self.duration = duration
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, color, duration):
        new_node = Node(color, duration)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

if 'cll' not in st.session_state:
    cll = CircularLinkedList()
    cll.append("RED", 40)
    cll.append("GREEN", 20)
    cll.append("YELLOW", 5)
    st.session_state.cll = cll
    st.session_state.current_node = cll.head

st.set_page_config(page_title="Tugas Struktur Data - Lampu Lalu Lintas", layout="centered")

st.title("🚦 Visualisasi Lampu Merah (Circular Linked List)")

speed = st.sidebar.slider("Kecepatan Mobil car", 1, 20, 10)

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.car_pos = -50

elapsed = time.time() - st.session_state.start_time
current = st.session_state.current_node

if elapsed >= current.duration:
    st.session_state.current_node = current.next 
    st.session_state.start_time = time.time()
    elapsed = 0

if current.color == "RED":
    if st.session_state.car_pos < 120 or st.session_state.car_pos > 250:
        st.session_state.car_pos += speed
else:
    st.session_state.car_pos += speed

if st.session_state.car_pos > 550:
    st.session_state.car_pos = -100

colors = {
    "RED": ("#FF0000", "gray", "gray"),
    "YELLOW": ("gray", "#FFFF00", "gray"),
    "GREEN": ("gray", "gray", "#00FF00")
}
c_red, c_yellow, c_green = colors[current.color]

remaining = int(current.duration - elapsed)
svg_code = f"""
<svg width="500" height="300" viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg">
    <rect width="500" height="300" fill="#0E1117" />
    
    <rect x="0" y="120" width="500" height="80" fill="#333" />
    <line x1="0" y1="160" x2="500" y2="160" stroke="white" stroke-dasharray="10" stroke-width="2" />
    
    <rect x="180" y="120" width="10" height="80" fill="white" />

    <rect x="140" y="40" width="30" height="80" fill="#222" rx="5" />
    <circle cx="155" cy="55" r="10" fill="{c_red}" />
    <circle cx="155" cy="80" r="10" fill="{c_yellow}" />
    <circle cx="155" cy="105" r="10" fill="{c_green}" />

    <g transform="translate({st.session_state.car_pos}, 155)">
        <rect width="60" height="25" fill="#007bff" rx="4" />
        <rect x="40" y="5" width="15" height="15" fill="#add8e6" />
        <circle cx="15" cy="25" r="6" fill="black" />
        <circle cx="45" cy="25" r="6" fill="black" />
    </g>
    
    <text x="10" y="30" fill="white" font-family="Arial" font-weight="bold">
        Lampu: {current.color} ({remaining}s)
    </text>
</svg>
"""

st.components.v1.html(svg_code, height=320)

time.sleep(0.03)
st.rerun()