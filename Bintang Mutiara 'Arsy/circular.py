import streamlit as st

st.title("Circular Queue")
st.write("Elemen terakhir terhubung kembali ke awal (wrap-around)")

# Inisiasi circular queue
SIZE = 5

if "queue" not in st.session_state:
    st.session_state.queue = [None] * SIZE
    st.session_state.front = -1
    st.session_state.rear = -1

queue = st.session_state.queue
front = st.session_state.front
rear = st.session_state.rear

# Cek penuh dan kosong
def is_full():
    return (rear + 1) % SIZE == front

def is_empty():
    return front == -1

# Input nilai
nilai = st.text_input("Masukkan nilai:")

col1, col2, col3 = st.columns(3)

# Enqueue
with col1:
    if st.button("Enqueue"):
        if is_full():
            st.error("Queue penuh!")
        elif nilai == "":
            st.warning("Isi nilai dulu!")
        else:
            if is_empty():
                st.session_state.front = 0
            st.session_state.rear = (st.session_state.rear + 1) % SIZE
            st.session_state.queue[st.session_state.rear] = nilai
            st.success(f"Enqueue: {nilai}")

# Dequeue
with col2:
    if st.button("Dequeue"):
        if is_empty():
            st.error("Queue kosong!")
        else:
            removed = queue[st.session_state.front]
            st.session_state.queue[st.session_state.front] = None
            if st.session_state.front == st.session_state.rear:
                st.session_state.front = -1
                st.session_state.rear = -1
            else:
                st.session_state.front = (st.session_state.front + 1) % SIZE
            st.success(f"Dequeue: {removed}")

# Reset
with col3:
    if st.button("Reset"):
        st.session_state.queue = [None] * SIZE
        st.session_state.front = -1
        st.session_state.rear = -1
        st.info("Queue direset")

# Tampilkan isi queue
st.subheader("Isi Queue:")
cols = st.columns(SIZE)
for i in range(SIZE):
    with cols[i]:
        nilai_slot = queue[i] if queue[i] is not None else "-"
        label = f"[{i}]"
        if i == st.session_state.front and not is_empty():
            label += " F"
        if i == st.session_state.rear and not is_empty():
            label += " R"
        st.metric(label=label, value=nilai_slot)

st.write(f"Front: {st.session_state.front} | Rear: {st.session_state.rear}")
st.write(f"Status: {'PENUH' if is_full() else 'KOSONG' if is_empty() else 'Aktif'}")