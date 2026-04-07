import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from collections import Counter
import re
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Word Count · Komentar Sosmed",
    page_icon="💬",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Fira+Code:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #e0e0e0;
}

.judul {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f72585;
    margin-bottom: 4px;
    text-shadow: 0 0 20px rgba(247,37,133,0.4);
}
.subjudul {
    text-align: center;
    font-family: 'Fira Code', monospace;
    font-size: 0.78rem;
    color: #a0a0c0;
    letter-spacing: 2px;
    margin-bottom: 20px;
}

hr { border-color: #f7258530 !important; }

label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.75rem !important;
    color: #a0a0c0 !important;
}

.stTextArea > div > div > textarea {
    background: #0d1b2a !important;
    border: 1px solid #f7258540 !important;
    color: #e0e0e0 !important;
    font-family: 'Fira Code', monospace !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}

.stButton > button {
    font-family: 'Fira Code', monospace !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    width: 100% !important;
    background: linear-gradient(90deg, #f72585, #7209b7) !important;
    border: none !important;
    color: white !important;
    padding: 12px !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.kartu {
    background: rgba(13, 27, 42, 0.85);
    border: 1px solid #f7258530;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}
.kartu-judul {
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    color: #f72585;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* Word chips */
.chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
    font-family: 'Fira Code', monospace;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid;
    display: inline-block;
}

/* Dict table */
.dict-tbl { width: 100%; border-collapse: collapse; font-family: 'Fira Code', monospace; font-size: 0.8rem; }
.dict-tbl th { background: #0d1b2a; color: #f72585; padding: 8px 14px; text-align: left; font-size: 0.68rem; letter-spacing: 1px; border-bottom: 1px solid #f7258530; }
.dict-tbl td { padding: 7px 14px; color: #c0c0e0; border-bottom: 1px solid #ffffff08; }
.dict-tbl tr:hover td { background: #ffffff05; }

.bar-freq {
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(90deg, #f72585, #7209b7);
    display: inline-block;
    vertical-align: middle;
    margin-left: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Stop words ────────────────────────────────────────────────────────────────
STOP_WORDS = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk",
    "pada", "adalah", "atau", "juga", "karena", "ada", "tidak", "ya",
    "aja", "sih", "deh", "loh", "kak", "bang", "bro", "sis", "nya",
    "the", "is", "a", "an", "and", "or", "in", "of", "to", "for",
    "i", "you", "me", "my", "we", "it", "be", "was", "are", "but",
    "so", "this", "that", "have", "not", "with", "can", "do", "se",
}

def hitung_kata(text, hapus_sw):
    text  = text.lower()
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    if hapus_sw:
        words = [w for w in words if w not in STOP_WORDS]
    return dict(Counter(words).most_common())


def draw_pie(wf, top_n):
    items  = list(wf.items())[:top_n]
    labels = [k for k, _ in items]
    values = [v for _, v in items]

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    colors = cm.plasma(np.linspace(0.1, 0.9, len(labels)))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%",
        colors=colors, startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(edgecolor="#1a1a2e", linewidth=2),
    )
    for t in texts:
        t.set_color("#c0c0e0")
        t.set_fontsize(9)
        t.set_fontfamily("monospace")
    for at in autotexts:
        at.set_color("#ffffff")
        at.set_fontsize(8)
        at.set_fontweight("bold")
        at.set_fontfamily("monospace")

    ax.set_title(f"Top {top_n} Kata", color="#f72585",
                 fontsize=13, fontweight="bold", fontfamily="monospace", pad=16)
    plt.tight_layout()
    return fig


def draw_bubble(wf, top_n):
    items  = list(wf.items())[:top_n]
    labels = [k for k, _ in items]
    values = [v for _, v in items]

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    np.random.seed(42)
    x = np.random.uniform(0.1, 0.9, len(labels))
    y = np.random.uniform(0.1, 0.9, len(labels))
    sizes  = [v * 300 for v in values]
    colors = cm.plasma(np.linspace(0.1, 0.9, len(labels)))

    ax.scatter(x, y, s=sizes, c=colors, alpha=0.75, edgecolors="#1a1a2e", linewidth=2)

    for i, (xi, yi, lbl, val) in enumerate(zip(x, y, labels, values)):
        ax.text(xi, yi, lbl, ha="center", va="center",
                fontsize=max(7, min(12, val + 5)),
                fontweight="bold", color="#ffffff",
                fontfamily="monospace")
        ax.text(xi, yi - 0.07, str(val), ha="center", va="center",
                fontsize=7, color="#f72585", fontfamily="monospace")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Bubble Chart Frekuensi Kata", color="#f72585",
                 fontsize=13, fontweight="bold", fontfamily="monospace", pad=14)
    plt.tight_layout()
    return fig


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="judul">💬 Word Count</div>', unsafe_allow_html=True)
st.markdown('<div class="subjudul">ANALISIS FREKUENSI KATA · KOMENTAR MEDIA SOSIAL</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
default = """Produk ini bagus banget! Kualitasnya bagus dan harganya murah.
Saya suka banget sama produk ini, recommended banget deh!
Pengirimannya cepat, produk bagus, packing rapi. Bagus!
Mantap jiwa, produk kualitas terbaik dengan harga murah meriah.
Seller ramah, produk sesuai deskripsi, recommended seller ini!
Bagus banget produknya, udah order berkali-kali. Murah dan bagus!
Kualitas oke, harga murah, pengiriman cepat. Suka banget!"""

komentar  = st.text_area("✍️ Paste Komentar Media Sosial", value=default, height=180)
hapus_sw  = st.checkbox("Filter stop words (kata umum)", value=True)
top_n     = st.slider("Tampilkan top N kata", 5, 20, 10)
mode_viz  = st.radio("Pilih Visualisasi", ["🥧 Pie Chart", "🫧 Bubble Chart"], horizontal=True)
analisis  = st.button("🔍 Analisis Sekarang")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Hasil ─────────────────────────────────────────────────────────────────────
if analisis or komentar:
    wf = hitung_kata(komentar, hapus_sw)

    if not wf:
        st.warning("Tidak ada kata yang ditemukan.")
    else:
        # Statistik
        s1, s2, s3 = st.columns(3)
        s1.metric("Kata Unik",        len(wf))
        s2.metric("Kata Teratas",     list(wf.keys())[0])
        s3.metric("Frekuensi Maks",   list(wf.values())[0])

        st.markdown("<br>", unsafe_allow_html=True)

        # Visualisasi
        if mode_viz == "🥧 Pie Chart":
            fig = draw_pie(wf, top_n)
        else:
            fig = draw_bubble(wf, top_n)

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Dictionary {Key: Value}
        st.markdown("""
        <div class="kartu">
            <div class="kartu-judul">📖 Dictionary · { Key: Kata → Value: Frekuensi }</div>
        """, unsafe_allow_html=True)

        top_items = list(wf.items())[:top_n]
        max_val   = top_items[0][1] if top_items else 1
        rows = ""
        for i, (k, v) in enumerate(top_items):
            bar_w = int((v / max_val) * 80)
            rows += f"""
            <tr>
                <td style="color:#606080;">#{i+1}</td>
                <td><b style="color:#f72585;">"{k}"</b></td>
                <td>{v} <span class="bar-freq" style="width:{bar_w}px;"></span></td>
            </tr>"""

        st.markdown(f"""
            <table class="dict-tbl">
                <thead><tr><th>#</th><th>KEY (Kata)</th><th>VALUE (Frekuensi)</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Word chips
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="kartu"><div class="kartu-judul">🏷️ Word Cloud Chip</div><div class="chip-wrap">', unsafe_allow_html=True)
        colors_chip = ["#f72585", "#7209b7", "#3a0ca3", "#4361ee", "#4cc9f0"]
        chips = ""
        for i, (k, v) in enumerate(top_items):
            c = colors_chip[i % len(colors_chip)]
            chips += f'<span class="chip" style="color:{c};border-color:{c}40;background:{c}15;">#{k} ({v})</span> '
        st.markdown(chips + "</div></div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;font-family:\'Fira Code\',monospace;font-size:0.65rem;color:#3a3a55;">WORD COUNT VISUALIZER · STREAMLIT · FADHILA ITMAMUL F</p>', unsafe_allow_html=True)