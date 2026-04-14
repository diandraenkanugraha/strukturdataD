import streamlit as st
import time

# ============================================
# IMPLEMENTASI CIRCULAR LINKED LIST
# ============================================

class Node:
    """Node untuk Circular Linked List"""
    def __init__(self, warna: str, durasi: int, kode_warna: str):
        self.warna = warna
        self.durasi = durasi
        self.kode_warna = kode_warna
        self.next = None


class CircularLinkedList:
    """Circular Linked List untuk lampu lalu lintas"""
    def __init__(self):
        self.head = None
        self.current = None
    
    def append(self, warna: str, durasi: int, kode_warna: str):
        """Menambahkan node baru ke linked list"""
        new_node = Node(warna, durasi, kode_warna)
        
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            self.current = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
    
    def get_current(self) -> Node:
        """Mendapatkan node saat ini"""
        return self.current
    
    def move_next(self):
        """Pindah ke node berikutnya"""
        if self.current:
            self.current = self.current.next
    
    def get_all_lights(self) -> list:
        """Mendapatkan semua lampu dalam list"""
        lights = []
        if not self.head:
            return lights
        
        temp = self.head
        while True:
            lights.append({
                'warna': temp.warna,
                'durasi': temp.durasi,
                'kode_warna': temp.kode_warna
            })
            temp = temp.next
            if temp == self.head:
                break
        return lights


# ============================================
# INISIALISASI LAMPU LALU LINTAS
# ============================================

def init_traffic_light() -> CircularLinkedList:
    """Inisialisasi lampu lalu lintas dengan durasi yang ditentukan"""
    traffic_light = CircularLinkedList()
    
    # Urutan: Merah -> Hijau -> Kuning -> (kembali ke Merah)
    traffic_light.append("MERAH", 40, "#FF0000")
    traffic_light.append("HIJAU", 20, "#00FF00")
    traffic_light.append("KUNING", 5, "#FFFF00")
    
    return traffic_light


# ============================================
# STREAMLIT UI
# ============================================

st.set_page_config(
    page_title="Lampu Lalu Lintas",
    page_icon="🚦",
    layout="centered"
)

st.title("🚦 Simulasi Lampu Lalu Lintas")
st.markdown("### Menggunakan Circular Linked List")

st.divider()

# Inisialisasi session state
if 'traffic_light' not in st.session_state:
    st.session_state.traffic_light = init_traffic_light()
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'countdown' not in st.session_state:
    st.session_state.countdown = st.session_state.traffic_light.get_current().durasi

# Info Circular Linked List
with st.expander("📚 Tentang Circular Linked List", expanded=False):
    st.markdown("""
    **Circular Linked List** adalah struktur data linked list dimana node terakhir 
    menunjuk kembali ke node pertama, membentuk sebuah lingkaran.
    
    Pada simulasi ini:
    - **Node 1**: Lampu Merah (40 detik) → menunjuk ke Node 2
    - **Node 2**: Lampu Hijau (20 detik) → menunjuk ke Node 3
    - **Node 3**: Lampu Kuning (5 detik) → menunjuk kembali ke Node 1
    
    Total 1 siklus = 65 detik
    """)
    
    st.markdown("**Diagram Circular Linked List:**")
    st.code("""
    ┌─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
 [MERAH]  ──────►  [HIJAU]  ──────►  [KUNING] ────┘
 40 detik          20 detik          5 detik
    """)

st.divider()

# Tampilkan info durasi
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🔴 **Merah**: 40 detik")
with col2:
    st.markdown("🟢 **Hijau**: 20 detik")
with col3:
    st.markdown("🟡 **Kuning**: 5 detik")

st.divider()

# Kontrol
col_start, col_stop, col_reset = st.columns(3)

with col_start:
    if st.button("▶️ Mulai", use_container_width=True, type="primary"):
        st.session_state.is_running = True

with col_stop:
    if st.button("⏸️ Berhenti", use_container_width=True):
        st.session_state.is_running = False

with col_reset:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.is_running = False
        st.session_state.traffic_light = init_traffic_light()
        st.session_state.countdown = st.session_state.traffic_light.get_current().durasi
        st.rerun()

st.divider()

# Placeholder untuk lampu
light_placeholder = st.empty()
countdown_placeholder = st.empty()
status_placeholder = st.empty()

def render_traffic_light(current_node: Node, countdown: int):
    """Render tampilan lampu lalu lintas"""
    
    # Tentukan warna untuk setiap lampu
    merah = current_node.kode_warna if current_node.warna == "MERAH" else "#4a0000"
    hijau = current_node.kode_warna if current_node.warna == "HIJAU" else "#004a00"
    kuning = current_node.kode_warna if current_node.warna == "KUNING" else "#4a4a00"
    
    # CSS untuk lampu
    light_html = f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <div style="
            background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
            border-radius: 20px;
            padding: 30px 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 3px solid #444;
        ">
            <!-- Lampu Merah -->
            <div style="
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, {merah}, #1a0000);
                margin: 15px auto;
                box-shadow: {'0 0 40px ' + merah + ', 0 0 60px ' + merah if current_node.warna == 'MERAH' else 'inset 0 0 20px rgba(0,0,0,0.5)'};
                border: 3px solid #333;
            "></div>
            
            <!-- Lampu Kuning -->
            <div style="
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, {kuning}, #1a1a00);
                margin: 15px auto;
                box-shadow: {'0 0 40px ' + kuning + ', 0 0 60px ' + kuning if current_node.warna == 'KUNING' else 'inset 0 0 20px rgba(0,0,0,0.5)'};
                border: 3px solid #333;
            "></div>
            
            <!-- Lampu Hijau -->
            <div style="
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, {hijau}, #001a00);
                margin: 15px auto;
                box-shadow: {'0 0 40px ' + hijau + ', 0 0 60px ' + hijau if current_node.warna == 'HIJAU' else 'inset 0 0 20px rgba(0,0,0,0.5)'};
                border: 3px solid #333;
            "></div>
        </div>
    </div>
    """
    
    light_placeholder.markdown(light_html, unsafe_allow_html=True)
    
    # Countdown
    countdown_placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 72px; color: {current_node.kode_warna};'>{countdown}</h1>",
        unsafe_allow_html=True
    )
    
    # Status
    status_placeholder.markdown(
        f"<h3 style='text-align: center;'>Lampu: <span style='color: {current_node.kode_warna};'>{current_node.warna}</span></h3>",
        unsafe_allow_html=True
    )


# Loop utama
current = st.session_state.traffic_light.get_current()
render_traffic_light(current, st.session_state.countdown)

if st.session_state.is_running:
    time.sleep(1)
    
    st.session_state.countdown -= 1
    
    if st.session_state.countdown <= 0:
        st.session_state.traffic_light.move_next()
        st.session_state.countdown = st.session_state.traffic_light.get_current().durasi
    
    st.rerun()

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray;'>Dibuat dengan Streamlit & Circular Linked List</p>",
    unsafe_allow_html=True
)
