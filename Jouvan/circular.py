import streamlit as st
import time

# --- 1. Definisi Struktur Data Circular Linked List ---

class Node:
    """Kelas untuk merepresentasikan satu lampu dalam list."""
    def __init__(self, warna, durasi, warna_kode):
        self.warna = warna              # Nama warna (Teks)
        self.durasi = durasi            # Durasi dalam detik
        self.warna_kode = warna_kode    # Kode Hex/Nama warna untuk CSS
        self.next = None                # Pointer ke node berikutnya

class CircularLinkedList:
    """Kelas untuk mengelola linked list yang melingkar."""
    def __init__(self):
        self.head = None

    def tambah_lampu(self, warna, durasi, warna_kode):
        """Menambahkan lampu baru ke dalam list."""
        new_node = Node(warna, durasi, warna_kode)
        if not self.head:
            self.head = new_node
            new_node.next = self.head  # Menunjuk ke diri sendiri (circular)
        else:
            temp = self.head
            # Mencari node terakhir (yang menunjuk ke head)
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node       # Node terakhir lama menunjuk ke node baru
            new_node.next = self.head  # Node baru menunjuk ke head (circular)

    def get_list_data(self):
        """Mengambil data list untuk visualisasi diagram."""
        nodes_data = []
        if not self.head:
            return nodes_data
        
        current = self.head
        while True:
            nodes_data.append({
                "warna": current.warna,
                "durasi": current.durasi,
                "kode": current.warna_kode
            })
            current = current.next
            if current == self.head:
                break
        return nodes_data

# --- 2. Inisialisasi Data (Sesuai Ketentuan) ---

@st.cache_resource # Agar list hanya dibuat sekali
def inisialisasi_sistem_lampu():
    sistem = CircularLinkedList()
    # Menambahkan sesuai urutan logika lalu lintas: Hijau -> Kuning -> Merah -> (kembali ke Hijau)
    # Catatan: Urutan input menentukan urutan nyala.
    sistem.tambah_lampu("HIJAU", 20, "#00DD00") # Hijau terang
    sistem.tambah_lampu("KUNING", 5, "#FFD700")  # Gold/Kuning
    sistem.tambah_lampu("MERAH", 40, "#FF0000")  # Merah terang
    return sistem

# --- 3. Fungsi Komponen UI Streamlit ---

def draw_traffic_light(active_color, timer_value):
    """Menggambar visualisasi fisik lampu lalu lintas."""
    
    # Warna dasar lampu saat mati
    off_color = "#333333"
    
    # Menentukan warna mana yang 'menyala'
    red_style = active_color if active_color == "#FF0000" else off_color
    yellow_style = active_color if active_color == "#FFD700" else off_color
    green_style = active_color if active_color == "#00DD00" else off_color

    # CSS untuk styling lampu
    st.markdown(f"""
    <style>
        .traffic-light-housing {{
            background-color: #222;
            width: 120px;
            height: 320px;
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-around;
            margin: auto;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        }}
        .light {{
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 3px solid #111;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }}
        .timer-display {{
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 30px;
            font-weight: bold;
            background-color: black;
            padding: 5px 15px;
            border-radius: 10px;
            margin-top: 10px;
            text-align: center;
            width: 80px;
        }}
    </style>
    
    <div class="traffic-light-housing">
        <div class="light" style="background-color: {red_style}; box-shadow: { '0 0 20px ' + red_style if active_color == '#FF0000' else 'none' };"></div>
        <div class="light" style="background-color: {yellow_style}; box-shadow: { '0 0 20px ' + yellow_style if active_color == '#FFD700' else 'none' };"></div>
        <div class="light" style="background-color: {green_style}; box-shadow: { '0 0 20px ' + green_style if active_color == '#00DD00' else 'none' };"></div>
        <div class="timer-display">{timer_value:02d}</div>
    </div>
    """, unsafe_allow_html=True)

def draw_cll_diagram(current_warna, list_data):
    """Menggambar diagram konsep Circular Linked List."""
    st.caption("Konsep Struktur Data: Circular Linked List")
    
    cols = st.columns(len(list_data) * 2 - 1) # Kolom untuk node dan panah
    
    for i, data in enumerate(list_data):
        # Gambar Node
        is_active = (data['warna'] == current_warna)
        border_css = f"4px solid {data['kode']}" if is_active else "2px solid #555"
        bg_css = data['kode'] + "33" if is_active else "#222" # Transparan jika aktif
        text_color = "white" if is_active else "#aaa"
        
        with cols[i*2]:
            st.markdown(f"""
                <div style="
                    border: {border_css};
                    border-radius: 10px;
                    padding: 10px;
                    text-align: center;
                    background-color: {bg_css};
                    color: {text_color};
                    font-weight: {'bold' if is_active else 'normal'};
                    min-width: 80px;
                ">
                    {data['warna']}<br>
                    {data['durasi']}s<br>
                    <small>Node {i+1}</small>
                </div>
            """, unsafe_allow_html=True)
            
        # Gambar Panah "Next"
        if i < len(list_data) - 1:
            with cols[i*2 + 1]:
                st.markdown("<div style='text-align:center; padding-top:25px; color:#555;'>==></div>", unsafe_allow_html=True)

    # Panah kembali dari terakhir ke awal (Visualisasi Circular)
    st.markdown("""
        <div style="text-align: center; margin-top: -10px; color: #555; font-size: 20px;">
            <span style="border-left: 2px solid #555; border-bottom: 2px solid #555; border-right: 2px solid #555; padding: 0 45% 5px 45%; border-radius: 0 0 10px 10px;">
                ^ (Kembali ke Node 1 / head.next) ^
            </span>
        </div>
        <br>
    """, unsafe_allow_html=True)

# --- 4. Main Application ---

def main():
    st.set_page_config(page_title="Simulasi CLL Lampu Merah", layout="centered")
    
    st.title("🚦 Simulasi Lampu Lalu Lintas")
    st.subheader("Implementasi Struktur Data *Circular Linked List*")
    
    st.markdown(f"""
    **Ketentuan Durasi:**
    -🔴 Merah: 40 Detik | -🟡 Kuning: 5 Detik | -🟢 Hijau: 20 Detik
    """)

    # Setup data
    sistem_lampu = inisialisasi_sistem_lampu()
    list_data = sistem_lampu.get_list_data()

    st.divider()

    # Placeholder untuk elemen yang dinamis
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Fisik Lampu")
        light_placeholder = st.empty()
        status_placeholder = st.empty()
        
    with col2:
        st.write("### Logika & Diagram")
        diagram_placeholder = st.empty()
        info_placeholder = st.empty()

    # Tombol Kontrol
    if 'jalankan_simulasi' not in st.session_state:
        st.session_state['jalankan_simulasi'] = False

    def toggle_simulation():
        st.session_state['jalankan_simulasi'] = not st.session_state['jalankan_simulasi']

    st.sidebar.title("Kontrol")
    button_label = "Stop Simulasi" if st.session_state['jalankan_simulasi'] else "Mulai Simulasi"
    st.sidebar.button(button_label, on_click=toggle_simulation)
    
    speed = st.sidebar.slider("Kecepatan Simulasi (1x = Realtime)", 1, 10, 1)

    # --- Loop Simulasi Utama ---
    if st.session_state['jalankan_simulasi']:
        # Mulai dari Head (Hijau dalam setup ini)
        current_node = sistem_lampu.head
        
        # Penanganan error jika user stop di tengah jalan (menghindari infinite loop tak terkontrol di Streamlit)
        run_limit = 0 
        
        while st.session_state['jalankan_simulasi'] and run_limit < 10: # Batasi 10 siklus penuh untuk keamanan browser
            
            warna_aktif = current_node.warna
            durasi_aktif = current_node.durasi
            kode_aktif = current_node.warna_kode

            # Update Diagram (Node aktif berubah)
            with diagram_placeholder.container():
                draw_cll_diagram(warna_aktif, list_data)

            # Hitung Mundur
            for detik_tersisa in range(durasi_aktif, -1, -1):
                # Cek apakah user menekan stop di tengah hitungan mundur
                if not st.session_state['jalankan_simulasi']:
                    break
                
                # Update Visualisasi Lampu dan Angka
                with light_placeholder.container():
                    draw_traffic_light(kode_aktif, detik_tersisa)
                
                with status_placeholder:
                    st.info(f"Status Saat Ini: **{warna_aktif}**")
                    
                with info_placeholder:
                    st.write(f"**Logika Circular Linked List:**")
                    st.code(f"""
Current Node: {warna_aktif} (Durasi: {durasi_aktif}s)
Pointer Next   : {current_node.next.warna}
                    """)

                # Jeda waktu (disesuaikan dengan slider kecepatan)
                time.sleep(1 / speed)

            # Pindah ke node berikutnya (Logika inti CLL: current = current.next)
            current_node = current_node.next
            
            # Jika kembali ke head, hitung siklus
            if current_node == sistem_lampu.head:
                run_limit += 1

        if run_limit >= 10:
            st.warning("Simulasi dihentikan otomatis setelah 10 siklus untuk menghemat resource.")
            st.session_state['jalankan_simulasi'] = False
            st.experimental_rerun()

    else:
        # Tampilan saat idle (mati)
        with light_placeholder.container():
            draw_traffic_light("#333333", 0)
        with diagram_placeholder.container():
            draw_cll_diagram(None, list_data)
        status_placeholder.warning("Simulasi Berhenti. Klik 'Mulai' di sidebar.")

if __name__ == "__main__":
    main()