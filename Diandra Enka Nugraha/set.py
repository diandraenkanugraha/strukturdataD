import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Set Operations Visualizer",
    page_icon="⊕",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0d0d14;
    color: #e8e8f0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}

/* Header */
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0;
}
.main-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #6b6b8a;
    margin-top: 4px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Operation buttons */
.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    border: 1px solid #2a2a40 !important;
    background: #13131f !important;
    color: #9090b0 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    padding: 10px !important;
}
.stButton > button:hover {
    background: #1e1e30 !important;
    border-color: #5c5cff !important;
    color: #ffffff !important;
}

/* Result box */
.result-box {
    background: #13131f;
    border: 1px solid #2a2a40;
    border-left: 3px solid #5c5cff;
    border-radius: 6px;
    padding: 16px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #c0c0e0;
    margin-top: 12px;
}
.result-label {
    font-size: 0.7rem;
    color: #5c5cff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.result-value {
    font-size: 1.1rem;
    color: #ffffff;
    font-weight: 700;
}

/* Info cards */
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
}

/* Divider */
hr {
    border-color: #2a2a40 !important;
    margin: 20px 0 !important;
}

/* Input labels */
label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #6b6b8a !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* Text area & input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #13131f !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 4px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a12 !important;
    border-right: 1px solid #1e1e30 !important;
}

/* Badge */
.badge {
    display: inline-block;
    background: #1e1e30;
    border: 1px solid #2a2a40;
    color: #9090b0;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def parse_set(text: str) -> set:
    """Parse comma-separated input into a set of strings."""
    if not text.strip():
        return set()
    return {x.strip() for x in text.split(",") if x.strip()}


def draw_venn(A: set, B: set, highlight: set, op_name: str, col_A="#5c5cff", col_B="#ff5c8a"):
    """Draw a Venn diagram highlighting the result region."""
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#0d0d14")

    cx_a, cx_b, cy, r = 1.35, 2.65, 2.0, 1.3

    A_only  = A - B
    B_only  = B - A
    AB      = A & B
    neither = set()  # outside both

    # Determine which regions are highlighted
    hl_a  = bool(A_only  & highlight) or (op_name in ("Union",) and bool(A_only))
    hl_ab = bool(AB       & highlight) or (op_name in ("Union",) and bool(AB))
    hl_b  = bool(B_only  & highlight) or (op_name in ("Union",) and bool(B_only))

    # For pure region checks (when sets might be empty, rely on logic)
    result = highlight

    # Recompute based on operation so empty-set edge cases still colour right
    if op_name == "Union":
        hl_a  = bool(A_only)
        hl_ab = bool(AB)
        hl_b  = bool(B_only)
    elif op_name == "Intersection":
        hl_a  = False
        hl_ab = bool(AB)
        hl_b  = False
    elif op_name == "Difference (A − B)":
        hl_a  = bool(A_only)
        hl_ab = False
        hl_b  = False
    elif op_name == "Symmetric Difference":
        hl_a  = bool(A_only)
        hl_ab = False
        hl_b  = bool(B_only)

    alpha_on  = 0.55
    alpha_off = 0.08

    # Draw circles (base)
    circ_a = Circle((cx_a, cy), r, color=col_A, alpha=alpha_off, zorder=2)
    circ_b = Circle((cx_b, cy), r, color=col_B, alpha=alpha_off, zorder=2)
    ax.add_patch(circ_a)
    ax.add_patch(circ_b)

    # Highlighted fills
    if hl_a:
        ax.add_patch(Circle((cx_a, cy), r, color=col_A, alpha=alpha_on, zorder=3))
    if hl_b:
        ax.add_patch(Circle((cx_b, cy), r, color=col_B, alpha=alpha_on, zorder=3))

    # Intersection overlay (clip trick via low-level fill)
    if hl_ab:
        theta = np.linspace(0, 2 * np.pi, 300)
        # Points inside both circles
        pts = []
        for t in theta:
            x = cx_a + r * np.cos(t)
            y = cy  + r * np.sin(t)
            if (x - cx_b)**2 + (y - cy)**2 <= r**2:
                pts.append((x, y))
        if pts:
            xs, ys = zip(*pts)
            ax.fill(xs, ys, color="#c45cff", alpha=0.7, zorder=4)

    # Circle borders
    for cx, col in [(cx_a, col_A), (cx_b, col_B)]:
        circ_border = Circle((cx, cy), r, fill=False,
                              edgecolor=col, linewidth=2, zorder=5)
        ax.add_patch(circ_border)

    # Labels for A / B circles
    ax.text(cx_a - 0.55, cy + 1.45, "A", fontsize=22, fontweight="bold",
            color=col_A, ha="center", va="center", fontfamily="monospace", zorder=6)
    ax.text(cx_b + 0.55, cy + 1.45, "B", fontsize=22, fontweight="bold",
            color=col_B, ha="center", va="center", fontfamily="monospace", zorder=6)

    # Element labels inside regions
    def label_elements(items, x, y, color="#ffffff"):
        text = ", ".join(sorted(str(i) for i in items)) if items else "∅"
        ax.text(x, y, text, fontsize=9, color=color, ha="center", va="center",
                fontfamily="monospace", zorder=7,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d0d14",
                          edgecolor="none", alpha=0.6))

    label_elements(A_only,  cx_a - 0.65, cy)
    label_elements(AB,      (cx_a + cx_b) / 2, cy)
    label_elements(B_only,  cx_b + 0.65, cy)

    ax.set_xlim(0, 4)
    ax.set_ylim(0.3, 3.7)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title
    ax.set_title(op_name, fontsize=14, color="#ffffff",
                 fontfamily="monospace", fontweight="bold", pad=12)

    plt.tight_layout()
    return fig


OPERATIONS = {
    "Union":                   ("A ∪ B",  "Semua elemen yang ada di A, B, atau keduanya.",         lambda a, b: a | b),
    "Intersection":            ("A ∩ B",  "Elemen yang ada di kedua himpunan A dan B.",            lambda a, b: a & b),
    "Difference (A − B)":      ("A − B",  "Elemen yang ada di A tapi tidak ada di B.",             lambda a, b: a - b),
    "Symmetric Difference":    ("A △ B",  "Elemen yang ada di A atau B, tapi tidak di keduanya.", lambda a, b: a ^ b),
}


# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Set Operations</p>', unsafe_allow_html=True)
st.markdown('<p class="main-sub">Visualizer · Diagram Venn Interaktif</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col_input, col_viz = st.columns([1, 1.6], gap="large")

with col_input:
    st.markdown("#### ✦ Input Himpunan")

    raw_a = st.text_input(
        "Himpunan A",
        value="1, 2, 3, 4, 5",
        help="Pisahkan elemen dengan koma. Contoh: 1, 2, apel, buku",
    )
    raw_b = st.text_input(
        "Himpunan B",
        value="3, 4, 5, 6, 7",
        help="Pisahkan elemen dengan koma.",
    )

    A = parse_set(raw_a)
    B = parse_set(raw_b)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✦ Pilih Operasi")

    op_cols = st.columns(2)
    op_labels = list(OPERATIONS.keys())
    selected_op = st.session_state.get("selected_op", "Union")

    for i, label in enumerate(op_labels):
        c = op_cols[i % 2]
        sym = OPERATIONS[label][0]
        if c.button(f"{sym}\n{label}", key=label):
            selected_op = label
            st.session_state["selected_op"] = selected_op

    # ── Info card ──
    st.markdown("<br>", unsafe_allow_html=True)
    sym, desc, fn = OPERATIONS[selected_op]
    result = fn(A, B)

    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">Definisi</div>
        <div class="info-card-body">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    result_str = "{ " + ", ".join(sorted(str(x) for x in result)) + " }" if result else "∅  (himpunan kosong)"
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Hasil · {sym}</div>
        <div class="result-value">{result_str}</div>
    </div>
    """, unsafe_allow_html=True)

    card2, card3 = st.columns(2)
    card2.metric("| A |", len(A))
    card3.metric("| B |", len(B))

    st.metric(f"| {sym} |", len(result))


with col_viz:
    st.markdown("#### ✦ Diagram Venn")

    fig = draw_venn(A, B, result, selected_op)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ── Element breakdown table ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("#### ✦ Breakdown Elemen")

    t1, t2, t3 = st.columns(3)
    def fmt(s): return ", ".join(sorted(str(x) for x in s)) if s else "—"

    with t1:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title" style="color:#5c5cff;">A saja (A − B)</div>
            <div class="info-card-body">{fmt(A - B)}</div>
        </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title" style="color:#c45cff;">A ∩ B</div>
            <div class="info-card-body">{fmt(A & B)}</div>
        </div>""", unsafe_allow_html=True)

    with t3:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title" style="color:#ff5c8a;">B saja (B − A)</div>
            <div class="info-card-body">{fmt(B - A)}</div>
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a55;text-align:center;">
    SET OPERATIONS VISUALIZER · BUILT WITH STREAMLIT + MATPLOTLIB
</p>
""", unsafe_allow_html=True)