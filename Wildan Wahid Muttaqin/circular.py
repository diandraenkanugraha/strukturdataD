import streamlit as st
import time

class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, warna, durasi):
        newNode = Node(warna, durasi)

        if not self.head:
            self.head = newNode
            newNode.next = self.head
            return

        current = self.head
        while current.next != self.head:
            current = current.next

        current.next = newNode
        newNode.next = self.head

cll = CircularLinkedList()
cll.append("🔴", 40)
cll.append("🟢", 20)
cll.append("🟡", 5)

st.title("🚦 Simulasi Lampu Lalu Lintas (Circular Linked List)")

start = st.button("Mulai Simulasi")

placeholder = st.empty()

if start:
    current = cll.head

    while True:
        for sisa in range(current.durasi, 0, -1):
            if current.warna == "MERAH":
                color = "red"
            elif current.warna == "HIJAU":
                color = "green"
            else:
                color = "yellow"

            placeholder.markdown(
                f"""
                <div style="text-align:center;">
                    <h1 style="color:{color};">{current.warna}</h1>
                    <h2>{sisa} detik</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(1)

        current = current.next