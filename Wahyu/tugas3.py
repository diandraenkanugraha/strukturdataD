import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Circular Queue - Wahyu",
    page_icon="⭕",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
.stApp {
    background-color: #050510;
    background-image: radial-gradient(ellipse at 20% 50%, #0a0a2e 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 20%, #001a0a 0%, transparent 50%);
    color: #e0ffe0;
}

.judul {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: #00ff88;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(0,255,136,0.5), 0 0 60px rgba(0,255,136,0.2);
    margin-bottom: 2px;
}
.subjudul {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    color: #006633;
    letter-spacing: 4px;
    margin-bottom: 20px;
}

hr { border-color: #00ff8820 !important; }

label {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    color: #00ff8880 !important;
    letter-spacing: 2px !important;
}

.stTextInput > div > div > input {
    background: #050510 !important;
    border: 1px solid #00ff8840 !important;
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    border-radius: 4px !important;
    font-size: 0.8rem !important;
}
.stTextInput > div > div > input::placeholder { color: #006633 !important; }

.stButton > button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
    width: 100% !important;
    padding: 10px !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0,255,136,0.3) !important;
}

.panel {
    background: rgba(0, 255, 136, 0.03);
    border: 1px solid #00ff8820;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.6rem;
    color: #00ff88;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
    border-bottom: 1px solid #00ff8820;
    padding-bottom: 6px;
}

.log-item {
    font-family: 'Orbitron', monospace;
    font-size: 0.62rem;
    padding: 5px 10px;
    border-radius: 3px;
    margin-bottom: 4px;
    background: #050510;
    letter-spacing: 1px;
}
.log-ok   { border-left: 2px solid #00ff88; color: #00ff88; }
.log-err  { border-left: 2px solid #ff3366; color: #ff3366; }
.log-warn { border-left: 2px solid #ffcc00; color: #ffcc00; }

.elemen-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
}
.elemen-box {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 4px;
    border: 1px solid;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ── Circular Queue Class ──────────────────────────────────────────────────────
class CircularQueue:
    def __init__(self, cap):
        self.cap   = cap
        self.data  = [None] * cap
        self.front = -1
        self.rear  = -1
        self.size  = 0

    def is_empty(self): return self.size == 0
    def is_full(self):  return self.size == self.cap

    def enqueue(self, val):
        if self.is_full():
            return False, f"OVERFLOW — Queue penuh ({self.cap}/{self.cap})"
        if self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.cap
        self.data[self.rear] = val
        self.size += 1
        return True, f"ENQUEUE '{val}' → slot [{self.rear}]"

    def dequeue(self):
        if self.is_empty():
            return False, "UNDERFLOW — Queue kosong", None
        val = self.data[self.front]
        self.data[self.front] = None
        if self.size == 1:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.cap
        self.size -= 1
        return True, f"DEQUEUE '{val}' dari slot [{(self.front - 1) % self.cap}]", val


# ── Draw hexagonal-style circular queue ──────────────────────────────────────
def draw_cq(cq: CircularQueue):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#050510")
    ax.set_facecolor("#050510")

    n = cq.cap
    R_OUT, R_IN = 1.0, 0.48
    angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]

    for i in range(n):
        a0 = angles[i] - np.pi / n + 0.06
        a1 = angles[i] + np.pi / n - 0.06
        theta = np.linspace(a0, a1, 50)

        xo = R_OUT * np.cos(theta)
        yo = R_OUT * np.sin(theta)
        xi = R_IN  * np.cos(theta[::-1])
        yi = R_IN  * np.sin(theta[::-1])

        # Color logic
        if cq.data[i] is not None:
            if i == cq.front and i == cq.rear:
                fill_c, glow_c = "#ffcc00", "#ffcc0060"
            elif i == cq.front:
                fill_c, glow_c = "#00ff88", "#00ff8860"
            elif i == cq.rear:
                fill_c, glow_c = "#ff3366", "#ff336660"
            else:
                fill_c, glow_c = "#004422", "#00ff8820"
        else:
            fill_c, glow_c = "#0a0a1a", "#00000000"

        ax.fill(np.concatenate([xo, xi]),
                np.concatenate([yo, yi]),
                color=fill_c, alpha=0.8, zorder=2)

        # Glow border
        border_c = fill_c if cq.data[i] is not None else "#00ff8815"
        ax.plot(np.concatenate([xo, xi[::-1], [xo[0]]]),
                np.concatenate([yo, yi[::-1], [yo[0]]]),
                color=border_c, lw=1.5, zorder=3)

        mid = angles[i]

        # Slot index
        ax.text(1.2 * np.cos(mid), 1.2 * np.sin(mid), str(i),
                ha="center", va="center", fontsize=8,
                color="#00ff8850", fontfamily="monospace",
                fontweight="bold", zorder=4)

        # Value
        vx, vy = 0.73 * np.cos(mid), 0.73 * np.sin(mid)
        val = cq.data[i]
        txt_c = "#050510" if i in (cq.front, cq.rear) and val else "#00ff88" if val else "#00ff8820"
        ax.text(vx, vy,
                str(val) if val is not None else "∅",
                ha="center", va="center", fontsize=9, fontweight="bold",
                color=txt_c, fontfamily="monospace", zorder=4)

        # F/R badge
        lbl = ""
        if i == cq.front and i == cq.rear: lbl = "F/R"
        elif i == cq.front:                lbl = "FRONT"
        elif i == cq.rear:                 lbl = "REAR"
        if lbl:
            ax.text(1.38 * np.cos(mid), 1.38 * np.sin(mid), lbl,
                    ha="center", va="center", fontsize=6, fontweight="bold",
                    color="#ffcc00", fontfamily="monospace", zorder=5)

    # Inner circle
    inner = plt.Circle((0, 0), R_IN - 0.03, color="#050510", zorder=1)
    ax.add_patch(inner)

    # Grid lines inside
    for angle in angles:
        ax.plot([R_IN * np.cos(angle), 0], [R_IN * np.sin(angle), 0],
                color="#00ff8808", lw=0.5, zorder=1)

    # Center info
    pct = int(cq.size / cq.cap * 100) if cq.cap > 0 else 0
    ax.text(0, 0.12, f"{cq.size}/{cq.cap}",
            ha="center", va="center", fontsize=16, fontweight="bold",
            color="#00ff88", fontfamily="monospace", zorder=4)
    ax.text(0, -0.08, f"{pct}% PENUH",
            ha="center", va="center", fontsize=7,
            color="#006633", fontfamily="monospace", zorder=4)

    # Wrap-around indicator
    wrap_theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(1.55 * np.cos(wrap_theta), 1.55 * np.sin(wrap_theta),
            color="#00ff8815", lw=1, linestyle=":", zorder=1)

    # Arrow
    ax.annotate("", xy=(1.55 * np.cos(-0.15), 1.55 * np.sin(-0.15)),
                xytext=(1.55 * np.cos(0.15), 1.55 * np.sin(0.15)),
                arrowprops=dict(arrowstyle="->", color="#00ff8840", lw=1.5))
    ax.text(0, -1.65, "↺  WRAP-AROUND",
            ha="center", va="center", fontsize=7,
            color="#00ff8840", fontfamily="monospace")

    # Legend
    legend = [
        mpatches.Patch(color="#00ff88", label="Front"),
        mpatches.Patch(color="#ff3366", label="Rear"),
        mpatches.Patch(color="#ffcc00", label="Front & Rear"),
        mpatches.Patch(color="#004422", label="Terisi"),
        mpatches.Patch(color="#0a0a1a", label="Kosong"),
    ]
    ax.legend(handles=legend, loc="lower center",
              bbox_to_anchor=(0.5, -0.14), ncol=5,
              frameon=False, fontsize=7, labelcolor="#00ff8880")

    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.85, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    return fig


# ── Session ───────────────────────────────────────────────────────────────────
if "cq"  not in st.session_state: st.session_state.cq  = CircularQueue(8)
if "log" not in st.session_state: st.session_state.log = []
cq = st.session_state.cq

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="judul">⭕ CIRCULAR QUEUE</div>', unsafe_allow_html=True)
st.markdown('<div class="subjudul">WRAP-AROUND · ELEMEN TERAKHIR TERHUBUNG KE AWAL</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col_viz, col_ctrl = st.columns([1.6, 1], gap="large")

with col_viz:
    st.markdown("#### ⭕ Visualisasi")
    fig = draw_cq(cq)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Isi queue
    st.markdown('<div class="panel"><div class="panel-title">Urutan Elemen (Front → Rear)</div>', unsafe_allow_html=True)
    if not cq.is_empty():
        items_html = '<div class="elemen-row">'
        for i in range(cq.size):
            idx = (cq.front + i) % cq.cap
            if i == 0:
                c, bc = "#00ff88", "#00ff88"
            elif i == cq.size - 1:
                c, bc = "#ff3366", "#ff3366"
            else:
                c, bc = "#e0ffe0", "#00ff8840"
            items_html += f'<span class="elemen-box" style="color:{c};border-color:{bc};background:{bc}20;">[{idx}] {cq.data[idx]}</span>'
            if i < cq.size - 1:
                items_html += '<span style="color:#00ff8840;font-family:monospace;">→</span>'
        items_html += '<span style="color:#00ff8830;font-family:\'Orbitron\',monospace;font-size:0.6rem;"> ↺ wrap</span></div>'
        st.markdown(items_html + "</div>", unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-family:\'Orbitron\',monospace;font-size:0.7rem;color:#00ff8830;">— QUEUE KOSONG —</span></div>', unsafe_allow_html=True)

with col_ctrl:
    st.markdown("#### 🎛️ Kontrol")

    # Kapasitas
    cap_baru = st.slider("Kapasitas Slot", 4, 12, cq.cap)
    if cap_baru != cq.cap:
        st.session_state.cq  = CircularQueue(cap_baru)
        st.session_state.log = []
        st.rerun()

    val = st.text_input("Nilai", placeholder="Masukkan nilai...")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("➕ ENQUEUE"):
            if val.strip():
                ok, msg = cq.enqueue(val.strip())
                st.session_state.log.append(("ok" if ok else "err", msg))
                st.rerun()
            else:
                st.session_state.log.append(("warn", "INPUT KOSONG!"))
                st.rerun()
    with b2:
        if st.button("➖ DEQUEUE"):
            ok, msg, _ = cq.dequeue()
            st.session_state.log.append(("ok" if ok else "err", msg))
            st.rerun()

    if st.button("🔄 RESET"):
        st.session_state.cq  = CircularQueue(cap_baru)
        st.session_state.log = []
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Status
    st.markdown('<div class="panel"><div class="panel-title">Status Queue</div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    s1.metric("SIZE",  f"{cq.size}/{cq.cap}")
    s2.metric("FRONT", cq.front if cq.front != -1 else "—")
    s3, s4 = st.columns(2)
    s3.metric("REAR",  cq.rear  if cq.rear  != -1 else "—")
    s4.metric("STATUS", "FULL" if cq.is_full() else ("EMPTY" if cq.is_empty() else "ACTIVE"))
    st.markdown("</div>", unsafe_allow_html=True)

    # Log
    if st.session_state.log:
        st.markdown('<div class="panel"><div class="panel-title">Log Operasi</div>', unsafe_allow_html=True)
        for status, msg in reversed(st.session_state.log[-6:]):
            cls = f"log-{status}"
            st.markdown(f'<div class="log-item {cls}">› {msg}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;font-family:\'Orbitron\',monospace;font-size:0.55rem;color:#00ff8820;letter-spacing:3px;">CIRCULAR QUEUE VISUALIZER · STREAMLIT · WAHYU</p>', unsafe_allow_html=True)