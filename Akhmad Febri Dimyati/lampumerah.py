import streamlit as st
import time

# 1. Struktur Data Circular Linked List (CLL)
class Node:
    def __init__(self, warna, durasi, index):
        self.warna = warna
        self.durasi = durasi
        self.index = index # Posisi lampu (0: Merah, 1: Kuning, 2: Hijau)
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi, index):
        new_node = Node(warna, durasi, index)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

# 2. Setup Tampilan Streamlit
st.set_page_config(page_title="Lampu Merah", page_icon="🚦")
st.title("🚦 Visualisasi Lampu Merah (Realistis)")
st.markdown("---")

# 3. Inisialisasi Logika CLL (Sekali saja)
if 'traffic_cll' not in st.session_state:
    tlm = CircularLinkedList()
    # Menyesuaikan durasi tugas: Merah 40s, Hijau 20s, Kuning 5s
    # Urutan logis lalu lintas: Merah -> Hijau -> Kuning -> Merah
    tlm.tambah_lampu("MERAH", 40, 0)
    tlm.tambah_lampu("HIJAU", 20, 2)
    tlm.tambah_lampu("KUNING", 5, 1)
    st.session_state.traffic_cll = tlm
    st.session_state.current_node = tlm.head # Mulai dari Merah

# Ambil status lampu saat ini
current = st.session_state.current_node

# 4. Sidebar Kontrol.
with st.sidebar:
    st.header("Kontrol Simulasi")
    st.info(f"Lampu Aktif: **{current.warna}**")
    st.write(f"Durasi: {current.durasi} Detik")
    start_btn = st.button("▶️ Mulai/Lanjut Simulasi")
    reset_btn = st.button("🔁 Reset ke Merah")

if reset_btn:
    st.session_state.current_node = st.session_state.traffic_cll.head
    st.rerun()

# 5. Fungsi Visualisasi Tiang Lampu (CSS Kompleks)
def render_traffic_light(active_index):
    # Warna lampu saat MATI (redup)
    colors_off = ["#440000", "#444400", "#004400"]
    # Warna lampu saat HIDUP (terang + shadow)
    colors_on = ["#FF0000", "#FFFF00", "#00FF00"]
    shadows = ["0 0 50px #FF0000", "0 0 50px #FFFF00", "0 0 50px #00FF00"]

    # Tentukan warna mana yang menyala
    light_colors = [colors_off[0], colors_off[1], colors_off[2]]
    light_shadows = ["none", "none", "none"]
    
    light_colors[active_index] = colors_on[active_index]
    light_shadows[active_index] = shadows[active_index]

    # HTML & CSS untuk Tiang Lampu
    html_code = f"""
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; background-color: #f0f2f6; padding: 20px; border-radius: 20px;">
        <div style="background-color: #222; width: 150px; padding: 20px; border-radius: 30px; border: 10px solid #444; box-shadow: 10px 10px 20px rgba(0,0,0,0.5);">
            <div style="width: 100px; height: 100px; background-color: {light_colors[0]}; border-radius: 50%; margin: 10px auto; border: 5px solid #111; box-shadow: {light_shadows[0]}; transition: background 0.3s;"></div>
            <div style="width: 100px; height: 100px; background-color: {light_colors[1]}; border-radius: 50%; margin: 10px auto; border: 5px solid #111; box-shadow: {light_shadows[1]}; transition: background 0.3s;"></div>
            <div style="width: 100px; height: 100px; background-color: {light_colors[2]}; border-radius: 50%; margin: 10px auto; border: 5px solid #111; box-shadow: {light_shadows[2]}; transition: background 0.3s;"></div>
        </div>
        <div style="background-color: #333; width: 30px; height: 200px; margin-top: -10px; border-radius: 0 0 10px 10px;"></div>
        <div style="background-color: #555; width: 100px; height: 20px; border-radius: 10px;"></div>
    </div>
    """
    return html_code

# 6. Jalankan Simulasi (Looping)
placeholder = st.empty() # Wadah kosong untuk update visual

if start_btn:
    while True: # Loop selamanya (Circular)
        current = st.session_state.current_node
        
        # Countdown Detik
        for detik in range(current.durasi, 0, -1):
            with placeholder.container():
                # Col 1: Visual Lampu, Col 2: Info Detik
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(render_traffic_light(current.index), unsafe_allow_html=True)
                with c2:
                    st.metric(label=f"Lampu {current.warna}", value=f"{detik}s", delta="-1s")
                    st.write("---")
                    st.caption("Konsep: Circular Linked List bergerak ke `Node.next` setelah durasi habis.")
            
            time.sleep(1) # Delay 1 detik asli

        # Logika CLL: Pindah ke lampu berikutnya setelah waktu habis
        st.session_state.current_node = current.next
        # update variable current untuk loop selanjutnya
        current = st.session_state.current_node 

else:
    # Tampilan diam saat belum dimulai
    with placeholder.container():
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(render_traffic_light(current.index), unsafe_allow_html=True)
        with c2:
            st.warning("Klik 'Mulai' di sidebar untuk menjalankan simulasi otomatis.")
            st.write(f"Posisi sekarang: Lampu **{current.warna}** ({current.durasi} detik).")