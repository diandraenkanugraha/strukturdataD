import streamlit as st

st.set_page_config(page_title="Circular Queue Visualization", layout="centered")

st.title("🔄 Visualisasi Circular Queue")

# Inisialisasi session state
if "queue" not in st.session_state:
    st.session_state.queue = []
if "front" not in st.session_state:
    st.session_state.front = -1
if "rear" not in st.session_state:
    st.session_state.rear = -1
if "size" not in st.session_state:
    st.session_state.size = 5  # kapasitas default

capacity = st.number_input("Masukkan Kapasitas Queue", min_value=3, max_value=10, value=st.session_state.size)

st.session_state.size = capacity

# Fungsi Enqueue
def enqueue(data):
    if (st.session_state.rear + 1) % st.session_state.size == st.session_state.front:
        st.error("Queue Penuh!")
    else:
        if st.session_state.front == -1:
            st.session_state.front = 0
        st.session_state.rear = (st.session_state.rear + 1) % st.session_state.size
        
        if len(st.session_state.queue) < st.session_state.size:
            st.session_state.queue.append(data)
        else:
            st.session_state.queue[st.session_state.rear] = data
        
        st.success(f"{data} berhasil ditambahkan!")

# Fungsi Dequeue
def dequeue():
    if st.session_state.front == -1:
        st.error("Queue Kosong!")
    else:
        removed = st.session_state.queue[st.session_state.front]
        
        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
            st.session_state.queue = []
        else:
            st.session_state.front = (st.session_state.front + 1) % st.session_state.size
        
        st.warning(f"{removed} dikeluarkan dari queue")

# Input
data_input = st.text_input("Masukkan Data")

col1, col2 = st.columns(2)

with col1:
    if st.button("Enqueue"):
        if data_input:
            enqueue(data_input)
        else:
            st.warning("Masukkan data terlebih dahulu")

with col2:
    if st.button("Dequeue"):
        dequeue()

st.subheader("📊 Visualisasi Queue")

# Visualisasi bentuk melingkar sederhana
if st.session_state.front == -1:
    st.info("Queue kosong")
else:
    display = []
    for i in range(st.session_state.size):
        if i < len(st.session_state.queue):
            value = st.session_state.queue[i]
        else:
            value = "-"
        
        if i == st.session_state.front and i == st.session_state.rear:
            display.append(f"[F/R:{value}]")
        elif i == st.session_state.front:
            display.append(f"[F:{value}]")
        elif i == st.session_state.rear:
            display.append(f"[R:{value}]")
        else:
            display.append(f"[{value}]")

    st.write(" ➡️ ".join(display))

st.write("---")
st.write(f"Front Index: {st.session_state.front}")
st.write(f"Rear Index: {st.session_state.rear}")