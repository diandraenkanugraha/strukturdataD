import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Circular Queue Visualizer",
    page_icon="🔄",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background-color: #0d0d14; color: #e8e8f0; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0;
}
.main-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #6b6b8a;
    margin-top: 4px;
    letter-spacing: 2px;
    text-transform: uppercase;
}
hr { border-color: #2a2a40 !important; margin: 20px 0 !important; }

label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #6b6b8a !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.stTextInput > div > div > input {
    background: #13131f !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 6px !important;
}

.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    border: 1px solid #2a2a40 !important;
    background: #13131f !important;
    color: #9090b0 !important;
    width: 100% !important;
    padding: 10px !important;
}
.stButton > button:hover {
    border-color: #5c5cff !important;
    color: #ffffff !important;
    background: #1e1e30 !important;
}

.info-card {
    background: #13131f;
    border: 1px solid #2a2a40;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.info-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #5c5cff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.info-card-body {
    font-size: 0.95rem;
    color: #c0c0e0;
    font-family: 'Space Mono', monospace;
}

.status-box {
    background: #13131f;
    border: 1px solid #2a2a40;
    border-left: 3px solid #5c5cff;
    border-radius: 6px;
    padding: 12px 18px;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #c0c0e0;
    margin-bottom: 10px;
}
.status-ok   { border-left-color: #5cff8a !important; }
.status-warn { border-left-color: #ffb85c !important; }
.status-err  { border-left-color: #ff5c5c !important; }
</style>
""", unsafe_allow_html=True)


# ── Circular Queue Class ──────────────────────────────────────────────────────
class CircularQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, value):
        if self.is_full():
            return False, "❌ Queue penuh! Tidak bisa enqueue."
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity  # wrap-around
        self.queue[self.rear] = value
        self.size += 1
        return True, f"✅ Enqueue '{value}' ke indeks {self.rear}"

    def dequeue(self):
        if self.is_empty():
            return False, "❌ Queue kosong! Tidak bisa dequeue.", None
        value = self.queue[self.front]
        self.queue[self.front] = None
        if self.size == 1:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity  # wrap-around
        self.size -= 1
        return True, f"✅ Dequeue '{value}' dari indeks {self.front if self.front != -1 else (self.front)}", value

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[self.front]


# ── Draw Circular Queue ───────────────────────────────────────────────────────
def draw_circular_queue(cq: CircularQueue):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#0d0d14")

    n = cq.capacity
    angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]
    r_outer, r_inner = 1.0, 0.55

    for i in range(n):
        a_start = angles[i] - np.pi / n
        a_end   = angles[i] + np.pi / n

        # Determine color
        if cq.queue[i] is not None:
            if i == cq.front and i == cq.rear:
                color = "#c45cff"   # front & rear sama
            elif i == cq.front:
                color = "#5c5cff"   # front
            elif i == cq.rear:
                color = "#ff5c8a"   # rear
            else:
                color = "#3a3a99"   # filled
        else:
            color = "#1a1a28"       # empty

        # Draw arc segment
        theta = np.linspace(a_start, a_end, 30)
        x_out = r_outer * np.cos(theta)
        y_out = r_outer * np.sin(theta)
        x_in  = r_inner * np.cos(theta[::-1])
        y_in  = r_inner * np.sin(theta[::-1])
        ax.fill(
            np.concatenate([x_out, x_in]),
            np.concatenate([y_out, y_in]),
            color=color, alpha=0.9, zorder=2
        )
        # Border
        ax.plot(
            np.concatenate([x_out, x_in[::-1], [x_out[0]]]),
            np.concatenate([y_out, y_in[::-1], [y_out[0]]]),
            color="#0d0d14", linewidth=1.5, zorder=3
        )

        # Index number (outer)
        mid_angle = angles[i]
        rx, ry = 1.18 * np.cos(mid_angle), 1.18 * np.sin(mid_angle)
        ax.text(rx, ry, str(i), ha="center", va="center",
                color="#6b6b8a", fontsize=9, fontfamily="monospace", zorder=4)

        # Value (inner arc)
        vx, vy = 0.77 * np.cos(mid_angle), 0.77 * np.sin(mid_angle)
        val = cq.queue[i]
        ax.text(vx, vy, str(val) if val is not None else "—",
                ha="center", va="center",
                color="#ffffff" if val is not None else "#3a3a55",
                fontsize=10, fontweight="bold", fontfamily="monospace", zorder=4)

        # Front / Rear label
        label = ""
        if i == cq.front and i == cq.rear:
            label = "F/R"
        elif i == cq.front:
            label = "F"
        elif i == cq.rear:
            label = "R"
        if label:
            lx = 1.38 * np.cos(mid_angle)
            ly = 1.38 * np.sin(mid_angle)
            ax.text(lx, ly, label, ha="center", va="center",
                    color="#ffdd57", fontsize=8, fontweight="bold",
                    fontfamily="monospace", zorder=5)

    # Center text
    ax.text(0, 0, f"{cq.size}/{cq.capacity}",
            ha="center", va="center", color="#ffffff",
            fontsize=14, fontweight="bold", fontfamily="monospace", zorder=4)
    ax.text(0, -0.18, "size/cap", ha="center", va="center",
            color="#6b6b8a", fontsize=7, fontfamily="monospace", zorder=4)

    # Legend
    legend_items = [
        mpatches.Patch(color="#5c5cff", label="Front (F)"),
        mpatches.Patch(color="#ff5c8a", label="Rear (R)"),
        mpatches.Patch(color="#3a3a99", label="Filled"),
        mpatches.Patch(color="#1a1a28", label="Empty"),
    ]
    ax.legend(handles=legend_items, loc="lower center",
              bbox_to_anchor=(0.5, -0.08), ncol=4,
              frameon=False, fontsize=8,
              labelcolor="#9090b0")

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Circular Queue", color="#ffffff",
                 fontsize=14, fontweight="bold", fontfamily="monospace", pad=14)

    plt.tight_layout()
    return fig


# ── Session state ─────────────────────────────────────────────────────────────
if "cq" not in st.session_state:
    st.session_state.cq = CircularQueue(8)
if "log" not in st.session_state:
    st.session_state.log = []

cq = st.session_state.cq

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Circular Queue</p>', unsafe_allow_html=True)
st.markdown('<p class="main-sub">Visualisasi Antrian Melingkar · Wrap-Around</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col_ctrl, col_viz = st.columns([1, 1.6], gap="large")

with col_ctrl:
    st.markdown("#### ✦ Pengaturan")

    cap = st.slider("Kapasitas Queue", min_value=4, max_value=12, value=cq.capacity)
    if cap != cq.capacity:
        st.session_state.cq = CircularQueue(cap)
        st.session_state.log = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✦ Operasi")

    val_input = st.text_input("Nilai untuk Enqueue", placeholder="contoh: A, 10, X ...")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Enqueue"):
            if val_input.strip():
                ok, msg = cq.enqueue(val_input.strip())
                st.session_state.log.append(("ok" if ok else "err", msg))
            else:
                st.session_state.log.append(("warn", "⚠️ Masukkan nilai terlebih dahulu!"))

    with c2:
        if st.button("➖ Dequeue"):
            ok, msg, _ = cq.dequeue()
            st.session_state.log.append(("ok" if ok else "err", msg))

    if st.button("🔄 Reset Queue"):
        st.session_state.cq = CircularQueue(cap)
        st.session_state.log = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✦ Status Queue")

    c3, c4 = st.columns(2)
    c3.metric("Size",     f"{cq.size} / {cq.capacity}")
    c4.metric("Front",    cq.front if cq.front != -1 else "-")
    c5, c6 = st.columns(2)
    c5.metric("Rear",     cq.rear  if cq.rear  != -1 else "-")
    c6.metric("Peek",     str(cq.peek()) if cq.peek() is not None else "-")

    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">Kondisi</div>
        <div class="info-card-body">
            {'🔴 Queue <b>PENUH</b>' if cq.is_full() else ('⚪ Queue <b>KOSONG</b>' if cq.is_empty() else '🟢 Queue <b>AKTIF</b>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Log
    if st.session_state.log:
        st.markdown("#### ✦ Log Operasi")
        for status, msg in reversed(st.session_state.log[-6:]):
            cls = "status-ok" if status == "ok" else ("status-warn" if status == "warn" else "status-err")
            st.markdown(f'<div class="status-box {cls}">{msg}</div>', unsafe_allow_html=True)


with col_viz:
    st.markdown("#### ✦ Visualisasi")
    fig = draw_circular_queue(cq)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Isi queue saat ini
    st.markdown("#### ✦ Isi Queue (berurutan dari Front)")
    if not cq.is_empty():
        items = []
        for i in range(cq.size):
            idx = (cq.front + i) % cq.capacity
            items.append(f"[{idx}] {cq.queue[idx]}")
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">Elemen</div>
            <div class="info-card-body">{'  →  '.join(items)}  →  (wrap)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">Elemen</div>
            <div class="info-card-body">Queue kosong</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a55;text-align:center;">
    CIRCULAR QUEUE VISUALIZER · BUILT WITH STREAMLIT + MATPLOTLIB
</p>
""", unsafe_allow_html=True)