import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# Circular Linked List 
class Node:
    def __init__(self, color, duration):
        self.color    = color
        self.duration = duration
        self.next     = None

class CircularLinkedList:
    def __init__(self):
        self.head    = None
        self.current = None

    def append(self, color, duration):
        new_node = Node(color, duration)
        if not self.head:
            self.head         = new_node
            new_node.next     = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next     = new_node
            new_node.next = self.head
        if not self.current:
            self.current = self.head

    def move_next(self):
        self.current = self.current.next

    def get_all_nodes(self):
        nodes, temp = [], self.head
        while True:
            nodes.append(temp)
            temp = temp.next
            if temp == self.head:
                break
        return nodes

# Build CLL 
@st.cache_resource
def build_cll():
    cll = CircularLinkedList()
    cll.append("Merah",  40)
    cll.append("Hijau",  20)
    cll.append("Kuning",  5)
    return cll

cll = build_cll()

# Session state 
if "remaining"  not in st.session_state:
    st.session_state.remaining  = cll.current.duration
if "running"    not in st.session_state:
    st.session_state.running    = False
if "last_tick"  not in st.session_state:
    st.session_state.last_tick  = None

# ── Config 

COLORS = {
    "Merah":  {"hex": "#FF2200", "dim": "#3a0000", "emoji": "🔴", "label_color": "#FF4422"},
    "Hijau":  {"hex": "#00CC44", "dim": "#002a00", "emoji": "🟢", "label_color": "#00BB44"},
    "Kuning": {"hex": "#FFCC00", "dim": "#2a2000", "emoji": "🟡", "label_color": "#DDAA00"},
}

st.set_page_config(page_title="Lampu Lalu Lintas", page_icon="🚦", layout="centered")

# ── CSS 

st.markdown("""
<style>
  .main { max-width: 700px; margin: auto; }
  .bulb-row { display: flex; justify-content: center; gap: 1rem; margin: 1rem 0; }
  .bulb {
    width: 90px; height: 90px; border-radius: 50%;
    border: 4px solid #444; transition: background .3s, box-shadow .3s;
  }
  .timer-box {
    text-align: center; font-size: 72px; font-weight: 600;
    font-variant-numeric: tabular-nums; line-height: 1.1;
  }
  .state-label { text-align: center; font-size: 28px; font-weight: 500; margin-bottom: .5rem; }
  .housing {
    background: #1a1a1a; border-radius: 18px; padding: 24px 32px;
    display: flex; flex-direction: column; gap: 18px; align-items: center;
    width: fit-content; margin: auto; border: 4px solid #333;
  }
  .cll-row { display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap; }
  .cll-node {
    border: 2px solid #555; border-radius: 10px; padding: 10px 14px;
    text-align: center; font-size: 13px; min-width: 90px; transition: border-color .3s, background .3s;
  }
  .cll-node.active { font-weight: 600; }
  .cll-arrow { font-size: 22px; color: #888; }
  .back-arrow { text-align: center; color: #888; font-size: 13px; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header 

st.title("🚦 Lampu Lalu Lintas")
st.caption("Simulasi lampu lalu lintas menggunakan **Circular Linked List**")

# ── Tick logic

if st.session_state.running:
    now = time.time()
    if st.session_state.last_tick is not None:
        elapsed = now - st.session_state.last_tick
        st.session_state.remaining -= elapsed
        if st.session_state.remaining <= 0:
            cll.move_next()
            st.session_state.remaining = cll.current.duration
    st.session_state.last_tick = now

current_node = cll.current
color_cfg    = COLORS[current_node.color]
remaining    = max(0, int(st.session_state.remaining))

# ── Traffic light visual 
def bulb_style(color_name):
    cfg = COLORS[color_name]
    if current_node.color == color_name:
        return f"background:{cfg['hex']}; box-shadow: 0 0 30px 10px {cfg['hex']}88;"
    return f"background:{cfg['dim']};"

st.markdown(f"""
<div class="housing">
  <div class="bulb" style="{bulb_style('Merah')}"></div>
  <div class="bulb" style="{bulb_style('Kuning')}"></div>
  <div class="bulb" style="{bulb_style('Hijau')}"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="timer-box" style="color:{color_cfg['label_color']}">{remaining}</div>
<div class="state-label" style="color:{color_cfg['label_color']}">{color_cfg['emoji']} {current_node.color}</div>
""", unsafe_allow_html=True)

# ── Circular Linked List diagram 

st.markdown("---")
st.subheader("Struktur Circular Linked List")

nodes = cll.get_all_nodes()
parts = []
for i, node in enumerate(nodes):
    cfg     = COLORS[node.color]
    is_curr = (node == current_node)
    border  = f"border-color:{cfg['hex']};" if is_curr else ""
    bg      = f"background:{cfg['hex']}22;" if is_curr else ""
    active  = "active" if is_curr else ""
    parts.append(
        f'<div class="cll-node {active}" style="{border}{bg}">'
        f'{cfg["emoji"]} {node.color}<br>'
        f'<small style="color:#888">{node.duration} detik</small><br>'
        f'<small style="color:#555">next →</small>'
        f'</div>'
    )
    if i < len(nodes) - 1:
        parts.append('<div class="cll-arrow">→</div>')

st.markdown(
    f'<div class="cll-row">{"".join(parts)}</div>'
    '<div class="back-arrow">↩ Kuning.next menunjuk kembali ke Merah (circular)</div>',
    unsafe_allow_html=True,
)

# ── Info cards 
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Node saat ini", f"{color_cfg['emoji']} {current_node.color}")
col2.metric("Durasi",        f"{current_node.duration} detik")
col3.metric("Node berikutnya", f"{COLORS[current_node.next.color]['emoji']} {current_node.next.color}")

# ── Controls

st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    label = "⏸ Pause" if st.session_state.running else "▶ Mulai"
    if st.button(label, use_container_width=True):
        st.session_state.running   = not st.session_state.running
        st.session_state.last_tick = None

with c2:
    if st.button("⏭ Skip", use_container_width=True):
        cll.move_next()
        st.session_state.remaining  = cll.current.duration
        st.session_state.last_tick  = None

with c3:
    if st.button("🔄 Reset", use_container_width=True):
        cll.current                 = cll.head
        st.session_state.remaining  = cll.head.duration
        st.session_state.running    = False
        st.session_state.last_tick  = None

# ── Auto-refresh

if st.session_state.running:
    time.sleep(0.05)
    st.rerun()