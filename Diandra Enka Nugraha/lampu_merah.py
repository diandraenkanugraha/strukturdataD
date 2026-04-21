import streamlit as st
import time
import math

st.set_page_config(
    page_title="Traffic Light - Circular Linked List",
    layout="wide",
    page_icon="🚦"
)

# =====================================================
# CIRCULAR LINKED LIST IMPLEMENTATION
# =====================================================
class Node:
    """Node untuk Circular Linked List"""
    def __init__(self, color, color_hex, duration, label):
        self.color = color
        self.color_hex = color_hex
        self.duration = duration
        self.label = label
        self.next = None

class CircularLinkedList:
    """Circular Linked List untuk menyimpan urutan lampu lalu lintas"""
    def __init__(self):
        self.head = None
        self.current = None

    def append(self, color, color_hex, duration, label):
        new_node = Node(color, color_hex, duration, label)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            self.current = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def move_next(self):
        if self.current:
            self.current = self.current.next

    def get_current(self):
        return self.current

    def get_all_nodes(self):
        nodes = []
        if self.head:
            temp = self.head
            while True:
                nodes.append(temp)
                temp = temp.next
                if temp == self.head:
                    break
        return nodes

    def get_current_index(self):
        nodes = self.get_all_nodes()
        for i, node in enumerate(nodes):
            if node is self.current:
                return i
        return 0

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================
if 'cll' not in st.session_state:
    cll = CircularLinkedList()
    cll.append("Merah",  "#EF4444", 40, "Lampu Merah")
    cll.append("Kuning", "#EAB308",  5, "Lampu Kuning")
    cll.append("Hijau",  "#22C55E", 20, "Lampu Hijau")
    st.session_state.cll = cll
    st.session_state.remaining = 40.0
    st.session_state.running = False
    st.session_state.last_update = None
    st.session_state.transition_count = 0
    st.session_state.speed = 1.0           # NEW: kecepatan simulasi
    st.session_state.log = []              # NEW: riwayat transisi
    st.session_state.stats = {             # NEW: statistik per lampu
        "Merah":  {"count": 0, "total_time": 0.0},
        "Kuning": {"count": 0, "total_time": 0.0},
        "Hijau":  {"count": 0, "total_time": 0.0},
    }
    st.session_state.elapsed_current = 0.0  # detik yang sudah lewat di fase ini

# =====================================================
# CSS STYLES
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

    .stApp { background: #08080f; }
    blockquote, .stBlock { border: none !important; }

    .title-section { text-align: center; padding: 20px 0 4px 0; }
    .title-main {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #f1f5f9;
        margin: 0;
        letter-spacing: -1px;
    }
    .title-sub {
        font-family: 'Inter', sans-serif;
        color: #475569;
        font-size: 0.92rem;
        margin: 5px 0 0 0;
        font-weight: 500;
    }
    .title-sub span {
        color: #818cf8;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* ---- Traffic light ---- */
    .tl-housing {
        width: 126px; height: 360px;
        background: linear-gradient(160deg, #252538 0%, #161625 50%, #1a1a2e 100%);
        border-radius: 63px; padding: 20px 16px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: space-around;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 0 2px #2a2a42,
                    inset 0 1px 0 rgba(255,255,255,0.04);
        position: relative;
    }
    .tl-housing::before {
        content: ''; position: absolute; top: -26px; left: 50%;
        transform: translateX(-50%); width: 14px; height: 26px;
        background: linear-gradient(160deg, #252538, #161625);
        border-radius: 4px 4px 0 0; border: 2px solid #2a2a42; border-bottom: none;
    }
    .tl-pole {
        width: 12px; height: 55px;
        background: linear-gradient(160deg, #252538, #161625);
        border: 2px solid #2a2a42; border-top: none;
        border-radius: 0 0 4px 4px; margin-top: -2px;
    }
    .tl-base {
        width: 56px; height: 11px;
        background: linear-gradient(160deg, #252538, #161625);
        border: 2px solid #2a2a42; border-radius: 6px; margin-top: -1px;
    }

    /* ---- Pedestrian light ---- */
    .ped-housing {
        width: 62px; height: 160px;
        background: linear-gradient(160deg, #1c1c2e 0%, #10101a 100%);
        border-radius: 31px; padding: 12px 8px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: space-around;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 0 1.5px #1e1e32;
    }
    .ped-bulb {
        width: 38px; height: 38px; border-radius: 50%;
        transition: all 0.5s ease;
    }
    .ped-off   { background: radial-gradient(circle at 38% 38%, #1a1a2a, #0d0d18); box-shadow: inset 0 2px 5px rgba(0,0,0,0.5); }
    .ped-stop  { background: radial-gradient(circle at 35% 32%, #ff8a8a, #ef4444 50%, #b91c1c 90%);
                 box-shadow: 0 0 14px rgba(239,68,68,0.7), 0 0 35px rgba(239,68,68,0.35), inset 0 2px 4px rgba(255,255,255,0.12); }
    .ped-walk  { background: radial-gradient(circle at 35% 32%, #86efac, #22c55e 50%, #15803d 90%);
                 box-shadow: 0 0 14px rgba(34,197,94,0.7), 0 0 35px rgba(34,197,94,0.35), inset 0 2px 4px rgba(255,255,255,0.12); }

    /* ---- Bulbs ---- */
    .bulb { width: 82px; height: 82px; border-radius: 50%; transition: all 0.5s ease; }
    .bulb-off    { background: radial-gradient(circle at 38% 38%, #2a2a3a, #141420); box-shadow: inset 0 3px 6px rgba(0,0,0,0.4), 0 0 0 2px #1e1e30; }
    .bulb-red    { background: radial-gradient(circle at 35% 32%, #ff8a8a, #ef4444 50%, #b91c1c 90%);
                   box-shadow: 0 0 20px rgba(239,68,68,0.8), 0 0 50px rgba(239,68,68,0.5), 0 0 90px rgba(239,68,68,0.25),
                               inset 0 -4px 8px rgba(0,0,0,0.25), inset 0 2px 4px rgba(255,255,255,0.15); }
    .bulb-yellow { background: radial-gradient(circle at 35% 32%, #fde68a, #eab308 50%, #a16207 90%);
                   box-shadow: 0 0 20px rgba(234,179,8,0.8), 0 0 50px rgba(234,179,8,0.5), 0 0 90px rgba(234,179,8,0.25),
                               inset 0 -4px 8px rgba(0,0,0,0.25), inset 0 2px 4px rgba(255,255,255,0.15); }
    .bulb-green  { background: radial-gradient(circle at 35% 32%, #86efac, #22c55e 50%, #15803d 90%);
                   box-shadow: 0 0 20px rgba(34,197,94,0.8), 0 0 50px rgba(34,197,94,0.5), 0 0 90px rgba(34,197,94,0.25),
                               inset 0 -4px 8px rgba(0,0,0,0.25), inset 0 2px 4px rgba(255,255,255,0.15); }

    .tl-glow-merah  { box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 0 2px #2a2a42, 0 0 80px rgba(239,68,68,0.18) !important; }
    .tl-glow-kuning { box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 0 2px #2a2a42, 0 0 80px rgba(234,179,8,0.18) !important; }
    .tl-glow-hijau  { box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 0 2px #2a2a42, 0 0 80px rgba(34,197,94,0.18) !important; }

    /* ---- Timer ---- */
    .timer-num   { font-family:'JetBrains Mono',monospace; font-size:76px; font-weight:700; line-height:1; letter-spacing:-4px; }
    .timer-label { font-family:'Inter',sans-serif; color:#475569; font-size:12px; margin-top:5px; font-weight:500; }

    /* ---- Progress bar ---- */
    .prog-bg   { width:100%; height:5px; background:#151525; border-radius:3px; overflow:hidden; }
    .prog-fill { height:100%; border-radius:3px; transition:width 0.8s linear; }

    /* ---- Cards ---- */
    .card {
        background: linear-gradient(145deg, #111120 0%, #0d0d1a 100%);
        border: 1px solid #1e1e35; border-radius: 16px; padding: 22px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    .card-title {
        font-family:'Inter',sans-serif; font-weight:700; color:#cbd5e1;
        font-size:13px; margin-bottom:14px; text-transform:uppercase; letter-spacing:1px;
    }

    /* ---- Node rows ---- */
    .node-row {
        display:flex; align-items:center; gap:12px; padding:10px 14px;
        border-radius:10px; border:1px solid #1e1e35; transition:all 0.3s;
    }
    .node-row-active { border-color:var(--node-color); background:var(--node-bg); }
    .node-dot   { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
    .node-name  { font-family:'Inter',sans-serif; color:#e2e8f0; font-size:13px; font-weight:600; margin:0; }
    .node-meta  { font-family:'JetBrains Mono',monospace; color:#475569; font-size:10px; margin:2px 0 0 0; }
    .current-badge {
        font-family:'JetBrains Mono',monospace; font-size:9px; font-weight:700;
        padding:2px 7px; border-radius:5px; margin-left:auto; flex-shrink:0;
    }

    /* ---- Stats ---- */
    .stat-label { font-family:'Inter',sans-serif; color:#475569; font-size:10px; margin:0; text-transform:uppercase; letter-spacing:0.5px; }
    .stat-value { font-family:'Inter',sans-serif; color:#e2e8f0; font-size:14px; font-weight:600; margin:3px 0 0 0; }
    .stat-mono  { font-family:'JetBrains Mono',monospace; }

    /* ---- Stat bar (per-light usage) ---- */
    .stat-bar-wrap { margin-bottom:10px; }
    .stat-bar-label { display:flex; justify-content:space-between; margin-bottom:4px; }
    .stat-bar-bg  { background:#0e0e20; border-radius:4px; height:7px; overflow:hidden; }
    .stat-bar-fill{ height:100%; border-radius:4px; transition:width 0.8s ease; }

    /* ---- Log ---- */
    .log-row {
        display:flex; align-items:center; gap:10px; padding:7px 12px;
        border-radius:8px; border:1px solid #14142a; margin-bottom:5px;
        background:#0a0a17;
    }
    .log-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
    .log-text { font-family:'JetBrains Mono',monospace; font-size:10px; color:#475569; }
    .log-color{ font-weight:700; }

    /* ---- Speed badge ---- */
    .speed-badge {
        display:inline-block;
        font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700;
        padding:3px 10px; border-radius:6px;
        background:#1a1a30; border:1px solid #2a2a45; color:#818cf8;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown("""
<div class="title-section">
    <h1 class="title-main">Traffic Light Simulator</h1>
    <p class="title-sub">Visualisasi menggunakan <span>Circular Linked List</span></p>
</div>
""", unsafe_allow_html=True)
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)


# =====================================================
# SVG GENERATOR — CIRCULAR LINKED LIST DIAGRAM
# =====================================================
def generate_cll_svg(nodes, current_idx):
    cx, cy = 175, 178
    r = 108
    node_r = 38
    delta_deg = 26

    positions = []
    for i in range(3):
        angle = math.radians(-90 + i * 120)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        positions.append((x, y))

    parts = []
    parts.append('<svg width="350" height="356" viewBox="0 0 350 356" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs>')
    parts.append('<marker id="arr-def" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
                 '<path d="M0,1 L10,5 L0,9 L2.5,5Z" fill="#2a2a45"/></marker>')
    for nd in nodes:
        parts.append(f'<marker id="arr-{nd.color}" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
                     f'<path d="M0,1 L10,5 L0,9 L2.5,5Z" fill="{nd.color_hex}"/></marker>')
    parts.append('</defs>')

    # Arc arrows
    for i in range(3):
        start_deg = -90 + i * 120 + delta_deg
        end_deg   = -90 + ((i + 1) % 3) * 120 - delta_deg
        sx = cx + r * math.cos(math.radians(start_deg))
        sy = cy + r * math.sin(math.radians(start_deg))
        ex = cx + r * math.cos(math.radians(end_deg))
        ey = cy + r * math.sin(math.radians(end_deg))
        target = (i + 1) % 3
        is_active = target == current_idx
        if is_active:
            color  = nodes[target].color_hex
            marker = f'url(#arr-{nodes[target].color})'
            sw, dash, opacity = "2.5", "", "1"
        else:
            color, marker = "#1e1e38", "url(#arr-def)"
            sw, dash, opacity = "1.8", 'stroke-dasharray="6,4" ', "0.7"
        parts.append(f'<path d="M {sx:.1f} {sy:.1f} A {r} {r} 0 0 1 {ex:.1f} {ey:.1f}" '
                     f'fill="none" stroke="{color}" stroke-width="{sw}" {dash}opacity="{opacity}" marker-end="{marker}"/>')
        mid_deg = (start_deg + end_deg) / 2
        label_r = r + 22
        lx = cx + label_r * math.cos(math.radians(mid_deg))
        ly = cy + label_r * math.sin(math.radians(mid_deg))
        lc = nodes[target].color_hex if is_active else "#2a2a45"
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="middle" '
                     f'font-family="JetBrains Mono,monospace" font-size="9" font-weight="600" fill="{lc}" '
                     f'opacity="{"0.9" if is_active else "0.5"}">next</text>')

    # Nodes
    for i, (x, y) in enumerate(positions):
        nd = nodes[i]
        is_cur = (i == current_idx)
        if is_cur:
            parts.append(f'<circle cx="{x}" cy="{y}" r="{node_r+8}" fill="none" stroke="{nd.color_hex}" stroke-width="2" opacity="0.25">'
                         f'<animate attributeName="r" values="{node_r+5};{node_r+16};{node_r+5}" dur="2s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0.35;0.08;0.35" dur="2s" repeatCount="indefinite"/>'
                         f'</circle>')
            parts.append(f'<circle cx="{x}" cy="{y}" r="{node_r+3}" fill="{nd.color_hex}" opacity="0.08"/>')

        fill_c   = f"{nd.color_hex}18" if is_cur else "#111122"
        stroke_c = nd.color_hex if is_cur else "#252540"
        sw_c     = "2.8" if is_cur else "1.5"
        parts.append(f'<circle cx="{x}" cy="{y}" r="{node_r}" fill="{fill_c}" stroke="{stroke_c}" stroke-width="{sw_c}"/>')

        if is_cur:
            parts.append(f'<text x="{x}" y="{y - node_r - 14}" text-anchor="middle" '
                         f'font-family="JetBrains Mono,monospace" font-size="9" font-weight="700" fill="{nd.color_hex}">CURRENT</text>')
            parts.append(f'<line x1="{x}" y1="{y - node_r - 10}" x2="{x}" y2="{y - node_r - 3}" stroke="{nd.color_hex}" stroke-width="1" opacity="0.5"/>')

        txt_c = "#ffffff" if is_cur else "#4a5568"
        parts.append(f'<text x="{x}" y="{y - 7}" text-anchor="middle" dominant-baseline="middle" '
                     f'font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="{txt_c}">{nd.color}</text>')
        dur_c = nd.color_hex if is_cur else "#333350"
        parts.append(f'<text x="{x}" y="{y + 11}" text-anchor="middle" dominant-baseline="middle" '
                     f'font-family="JetBrains Mono,monospace" font-size="11" font-weight="600" fill="{dur_c}">{nd.duration}s</text>')
        parts.append(f'<text x="{x}" y="{y + 25}" text-anchor="middle" dominant-baseline="middle" '
                     f'font-family="JetBrains Mono,monospace" font-size="8" fill="#2a2a45">node[{i}]</text>')

    # HEAD pointer
    hx, hy = positions[0]
    parts.append(f'<text x="{hx}" y="{hy - node_r - 28}" text-anchor="middle" '
                 f'font-family="JetBrains Mono,monospace" font-size="10" font-weight="700" fill="#64748b">HEAD</text>')
    parts.append(f'<line x1="{hx}" y1="{hy - node_r - 25}" x2="{hx}" y2="{hy - node_r - 17}" stroke="#64748b" stroke-width="1.2"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =====================================================
# FRAGMENT — rerun setiap 1 detik
# =====================================================
@st.fragment(run_every=1.0)
def traffic_fragment():
    cll   = st.session_state.cll
    now   = time.time()
    speed = st.session_state.speed

    # ---- Timer logic ----
    if st.session_state.running:
        if st.session_state.last_update is not None:
            elapsed = (now - st.session_state.last_update) * speed
            st.session_state.remaining        -= elapsed
            st.session_state.elapsed_current  += elapsed

            # Catat statistik waktu aktif
            color_key = cll.get_current().color
            st.session_state.stats[color_key]["total_time"] += elapsed

            if st.session_state.remaining <= 0:
                # Catat log transisi
                prev_color = cll.get_current().color
                cll.move_next()
                next_color = cll.get_current().color
                st.session_state.remaining       = cll.get_current().duration + st.session_state.remaining
                st.session_state.transition_count += 1
                st.session_state.elapsed_current  = 0.0

                # Tambahkan ke log (simpan maks 8 entri)
                ts = time.strftime("%H:%M:%S")
                st.session_state.stats[next_color]["count"] += 1
                entry = {"from": prev_color, "to": next_color, "ts": ts,
                         "n": st.session_state.transition_count}
                st.session_state.log.insert(0, entry)
                if len(st.session_state.log) > 8:
                    st.session_state.log.pop()

        st.session_state.last_update = now

    remaining_int = max(0, math.ceil(st.session_state.remaining))
    current       = cll.get_current()
    nodes         = cll.get_all_nodes()
    current_idx   = cll.get_current_index()
    progress_pct  = max(0, min(100, (remaining_int / current.duration) * 100)) if current.duration > 0 else 0

    # Pejalan kaki: hijau saat merah, merah saat selain merah
    ped_stop_cls = "ped-off"
    ped_walk_cls = "ped-off"
    ped_label    = ""
    ped_color    = "#475569"
    if current.color == "Merah":
        ped_walk_cls = "ped-walk"
        ped_label    = "JALAN"
        ped_color    = "#22C55E"
    else:
        ped_stop_cls = "ped-stop"
        ped_label    = "BERHENTI"
        ped_color    = "#EF4444"

    # ================================================================
    # TOMBOL KONTROL
    # ================================================================
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        if st.button("▶️  Mulai", use_container_width=True, type="primary"):
            st.session_state.running    = True
            st.session_state.last_update = time.time()
    with col_b2:
        if st.button("⏸️  Berhenti", use_container_width=True):
            st.session_state.running = False
    with col_b3:
        if st.button("🔄  Reset", use_container_width=True):
            st.session_state.running          = False
            cll.current                        = cll.head
            st.session_state.remaining         = float(cll.get_current().duration)
            st.session_state.last_update       = None
            st.session_state.transition_count  = 0
            st.session_state.elapsed_current   = 0.0
            st.session_state.log               = []
            st.session_state.stats             = {
                "Merah":  {"count": 0, "total_time": 0.0},
                "Kuning": {"count": 0, "total_time": 0.0},
                "Hijau":  {"count": 0, "total_time": 0.0},
            }
    with col_b4:
        if st.button("⏭️  Skip", use_container_width=True):
            prev = cll.get_current().color
            cll.move_next()
            nxt = cll.get_current().color
            st.session_state.remaining        = float(cll.get_current().duration)
            st.session_state.transition_count += 1
            st.session_state.elapsed_current   = 0.0
            ts = time.strftime("%H:%M:%S")
            st.session_state.stats[nxt]["count"] += 1
            entry = {"from": prev, "to": nxt, "ts": ts,
                     "n": st.session_state.transition_count}
            st.session_state.log.insert(0, entry)
            if len(st.session_state.log) > 8:
                st.session_state.log.pop()
            if st.session_state.running:
                st.session_state.last_update = time.time()

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ================================================================
    # PENGATURAN KECEPATAN
    # ================================================================
    speed_labels = {"0.5×": 0.5, "1× (Normal)": 1.0, "2×": 2.0, "5×": 5.0}
    cur_speed_label = {v: k for k, v in speed_labels.items()}.get(speed, "1× (Normal)")
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
        <p style="font-family:'Inter',sans-serif; color:#475569; font-size:12px; margin:0; font-weight:600; text-transform:uppercase; letter-spacing:1px;">Kecepatan Simulasi:</p>
        <span class="speed-badge">{cur_speed_label}</span>
    </div>
    """, unsafe_allow_html=True)
    speed_col = st.columns(len(speed_labels))
    for idx, (lbl, val) in enumerate(speed_labels.items()):
        with speed_col[idx]:
            btn_type = "primary" if speed == val else "secondary"
            if st.button(lbl, use_container_width=True, type=btn_type, key=f"spd_{lbl}"):
                st.session_state.speed = val

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # ================================================================
    # LAYOUT UTAMA — 3 kolom
    # ================================================================
    col_left, col_mid, col_right = st.columns([0.85, 0.7, 1.45], gap="large")

    # ================================================================
    # KOLOM KIRI — Traffic Light + Pejalan Kaki + Status
    # ================================================================
    with col_left:
        glow_cls = f"tl-glow-{current.color.lower()}"
        red_cls  = "bulb-red"    if current.color == "Merah"  else "bulb-off"
        yel_cls  = "bulb-yellow" if current.color == "Kuning" else "bulb-off"
        grn_cls  = "bulb-green"  if current.color == "Hijau"  else "bulb-off"

        st.markdown(f"""
        <div class="card" style="display:flex; flex-direction:column; align-items:center; padding:32px 24px 24px 24px;">
            <p class="card-title" style="margin-bottom:18px;">Lampu Lalu Lintas</p>
            <div style="display:flex; align-items:flex-end; gap:18px; justify-content:center;">
                <!-- Main light -->
                <div style="display:flex; flex-direction:column; align-items:center;">
                    <div class="tl-housing {glow_cls}">
                        <div class="bulb {red_cls}"></div>
                        <div class="bulb {yel_cls}"></div>
                        <div class="bulb {grn_cls}"></div>
                    </div>
                    <div class="tl-pole"></div>
                    <div class="tl-base"></div>
                </div>
                <!-- Pedestrian light -->
                <div style="display:flex; flex-direction:column; align-items:center; margin-bottom:13px;">
                    <p style="font-family:'Inter',sans-serif; font-size:9px; color:#334155; margin:0 0 6px 0; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Pejalan<br>Kaki</p>
                    <div class="ped-housing">
                        <div class="ped-bulb {ped_stop_cls}"></div>
                        <div class="ped-bulb {ped_walk_cls}"></div>
                    </div>
                    <p style="font-family:'JetBrains Mono',monospace; font-size:9px; font-weight:700; color:{ped_color}; margin:6px 0 0 0;">{ped_label}</p>
                </div>
            </div>
            <div style="margin-top:24px; text-align:center;">
                <div class="timer-num" style="color:{current.color_hex};">{remaining_int:02d}</div>
                <p class="timer-label">detik tersisa</p>
            </div>
            <div style="width:100%; margin-top:18px;">
                <div class="prog-bg">
                    <div class="prog-fill" style="width:{progress_pct:.1f}%; background:linear-gradient(90deg, {current.color_hex}88, {current.color_hex});"></div>
                </div>
                <p style="font-family:'JetBrains Mono',monospace; color:#334155; font-size:10px; margin-top:4px; text-align:center;">{progress_pct:.0f}%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Status card
        status_text = "🟢 Berjalan" if st.session_state.running else "🔴 Berhenti"
        st.markdown(f"""
        <div class="card" style="margin-top:12px;">
            <p class="card-title">Informasi Status</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
                <div><p class="stat-label">Status</p><p class="stat-value">{status_text}</p></div>
                <div><p class="stat-label">Transisi</p><p class="stat-value stat-mono">{st.session_state.transition_count}x</p></div>
                <div><p class="stat-label">Lampu Aktif</p><p class="stat-value" style="color:{current.color_hex};">{current.label}</p></div>
                <div><p class="stat-label">Durasi Penuh</p><p class="stat-value stat-mono">{current.duration} detik</p></div>
                <div><p class="stat-label">Total Siklus</p><p class="stat-value stat-mono">{sum(n.duration for n in nodes)} detik</p></div>
                <div><p class="stat-label">Jumlah Node</p><p class="stat-value stat-mono">{len(nodes)} node</p></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ================================================================
    # KOLOM TENGAH — Statistik per lampu + Log transisi
    # ================================================================
    with col_mid:
        # Statistik penggunaan lampu
        total_time_all = sum(st.session_state.stats[k]["total_time"] for k in st.session_state.stats)
        color_map = {"Merah": "#EF4444", "Kuning": "#EAB308", "Hijau": "#22C55E"}

        stat_rows = ""
        for color_key, hex_c in color_map.items():
            s        = st.session_state.stats[color_key]
            pct      = (s["total_time"] / total_time_all * 100) if total_time_all > 0 else 0
            mins, secs = divmod(int(s["total_time"]), 60)
            time_str = f"{mins}m {secs}s" if mins else f"{secs}s"
            stat_rows += f"""
            <div class="stat-bar-wrap">
                <div class="stat-bar-label">
                    <span style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600; color:{hex_c};">{color_key}</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#475569;">{time_str} &nbsp;|&nbsp; {pct:.0f}%</span>
                </div>
                <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:{pct:.1f}%; background:{hex_c};"></div></div>
            </div>"""

        st.markdown(f"""
        <div class="card">
            <p class="card-title">Statistik Penggunaan</p>
            {stat_rows}
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #14142a; display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; text-align:center;">
                {"".join(
                    f'<div><p class="stat-label">{k}</p><p class="stat-value stat-mono" style="color:{color_map[k]}; font-size:16px;">{st.session_state.stats[k]["count"]}</p><p style="font-family:Inter,sans-serif; font-size:9px; color:#334155; margin:0;">kali aktif</p></div>'
                    for k in color_map
                )}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Log transisi
        if st.session_state.log:
            log_html = ""
            for entry in st.session_state.log:
                fc = color_map.get(entry["from"], "#475569")
                tc = color_map.get(entry["to"], "#475569")
                log_html += f"""
                <div class="log-row">
                    <div class="log-dot" style="background:{tc};"></div>
                    <div class="log-text">
                        <span style="color:{fc};" class="log-color">{entry["from"]}</span>
                        <span style="color:#2a2a45;"> → </span>
                        <span style="color:{tc};" class="log-color">{entry["to"]}</span>
                    </div>
                    <div style="margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:9px; color:#334155;">{entry["ts"]}</div>
                </div>"""

            st.markdown(f"""
            <div class="card" style="margin-top:12px;">
                <p class="card-title">Riwayat Transisi</p>
                {log_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="margin-top:12px;">
                <p class="card-title">Riwayat Transisi</p>
                <p style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#2a2a45; text-align:center; margin:12px 0;">Belum ada transisi...</p>
            </div>
            """, unsafe_allow_html=True)

    # ================================================================
    # KOLOM KANAN — CLL Diagram + Node Detail + Alur
    # ================================================================
    with col_right:
        cll_svg = generate_cll_svg(nodes, current_idx)
        st.markdown(f"""
        <div class="card" style="display:flex; flex-direction:column; align-items:center; padding:24px 16px 18px 16px;">
            <p class="card-title" style="margin-bottom:6px;">Circular Linked List</p>
            <div style="opacity:0.4; margin-bottom:6px;">
                <p style="font-family:'JetBrains Mono',monospace; font-size:9px; color:#64748b; margin:0;">
                    current → current.next → current.next.next → ... → current (loop)
                </p>
            </div>
            {cll_svg}
        </div>
        """, unsafe_allow_html=True)

        # Node Detail
        node_rows = []
        for i, nd in enumerate(nodes):
            is_cur    = (i == current_idx)
            border_c  = nd.color_hex if is_cur else "#1e1e35"
            bg        = f"{nd.color_hex}0d" if is_cur else "transparent"
            opacity   = "1" if is_cur else "0.4"
            badge     = (f'<span class="current-badge" style="background:{nd.color_hex}20; color:{nd.color_hex}; border:1px solid {nd.color_hex}40;">CURRENT</span>'
                         if is_cur else "")
            node_rows.append(f"""
            <div class="node-row {'node-row-active' if is_cur else ''}"
                 style="border-color:{border_c}; background:{bg}; opacity:{opacity}; --node-color:{nd.color_hex}; --node-bg:{nd.color_hex}0d;">
                <div class="node-dot" style="background:{nd.color_hex}; box-shadow:0 0 8px {nd.color_hex}50;"></div>
                <div style="flex:1; min-width:0;">
                    <p class="node-name" style="color:{'#fff' if is_cur else '#64748b'};">Node[{i}] — {nd.color}</p>
                    <p class="node-meta">next → Node[{(i+1)%3}] &nbsp;|&nbsp; duration = {nd.duration}s</p>
                </div>
                {badge}
            </div>""")

        st.markdown(f"""
        <div class="card" style="margin-top:12px;">
            <p class="card-title">Detail Node</p>
            <div style="display:flex; flex-direction:column; gap:7px;">{''.join(node_rows)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Sequence & pseudocode
        seq = []
        for i, nd in enumerate(nodes):
            is_cur = (i == current_idx)
            c  = nd.color_hex if is_cur else "#2a2a45"
            fw = "700" if is_cur else "400"
            bg = f"{nd.color_hex}15" if is_cur else "transparent"
            bd = nd.color_hex if is_cur else "#1e1e35"
            seq.append(f'<span style="font-family:Inter,sans-serif; font-size:12px; font-weight:{fw}; padding:5px 12px; border-radius:7px; border:1px solid {bd}; color:{c}; background:{bg};">{nd.color}</span>')
            if i < 2:
                seq.append('<span style="color:#2a2a42; font-size:14px;">→</span>')
        seq.append('<span style="color:#2a2a42; font-size:14px;">→</span>')
        seq.append('<span style="font-size:13px; padding:5px 8px;">🔁</span>')

        st.markdown(f"""
        <div class="card" style="margin-top:12px;">
            <p class="card-title">Alur Perpindahan Node</p>
            <div style="display:flex; align-items:center; justify-content:center; gap:7px; flex-wrap:wrap;">{''.join(seq)}</div>
            <div style="margin-top:12px; padding:12px; background:#0a0a18; border-radius:9px; border:1px solid #1a1a30;">
                <p style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#475569; margin:0; line-height:1.7;">
                    <span style="color:#6366f1;">def</span> <span style="color:#22c55e;">move_next</span>(self):<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;self.<span style="color:#eab308;">current</span> = self.current.<span style="color:#ef4444;">next</span>
                    <span style="color:#334155;"># circular → otomatis kembali ke head</span>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# JALANKAN FRAGMENT
# =====================================================
traffic_fragment()

# Footer
st.markdown("""
<div style="text-align:center; padding:24px 0 14px 0; border-top:1px solid #111125; margin-top:24px;">
    <p style="font-family:'Inter',sans-serif; color:#1e293b; font-size:11px; margin:0;">
        Circular Linked List — Setiap node memiliki pointer
        <code style="color:#334155; background:#0f0f1f; padding:1px 5px; border-radius:3px; font-family:'JetBrains Mono',monospace; font-size:10px;">next</code>
        yang membentuk siklus tanpa akhir
    </p>
</div>
""", unsafe_allow_html=True)