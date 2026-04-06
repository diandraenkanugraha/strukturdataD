import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Word Count Visualizer",
    page_icon="💬",
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

.stTextArea > div > div > textarea {
    background: #13131f !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 6px !important;
    font-size: 0.85rem !important;
}

.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    border: 1px solid #5c5cff !important;
    background: #5c5cff !important;
    color: #ffffff !important;
    width: 100% !important;
    padding: 10px !important;
}
.stButton > button:hover {
    background: #4444dd !important;
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
}

.dict-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
}
.dict-table th {
    background: #1e1e30;
    color: #5c5cff;
    text-align: left;
    padding: 8px 14px;
    letter-spacing: 1px;
    font-size: 0.7rem;
    text-transform: uppercase;
    border-bottom: 1px solid #2a2a40;
}
.dict-table td {
    padding: 7px 14px;
    color: #c0c0e0;
    border-bottom: 1px solid #1a1a28;
}
.dict-table tr:hover td { background: #15151f; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Word Count Visualizer</p>', unsafe_allow_html=True)
st.markdown('<p class="main-sub">Analisis Frekuensi Kata · Komentar Media Sosial</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Stop words sederhana ──────────────────────────────────────────────────────
STOP_WORDS = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk",
    "pada", "adalah", "atau", "juga", "karena", "ada", "tidak", "ya",
    "aja", "sih", "deh", "loh", "kak", "bang", "bro", "sis", "nya",
    "the", "is", "a", "an", "and", "or", "in", "of", "to", "for",
    "i", "you", "me", "my", "we", "it", "be", "was", "are", "but",
    "so", "this", "that", "have", "not", "with", "can", "do",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def count_words(text: str, remove_stopwords: bool) -> dict:
    text = text.lower()
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    if remove_stopwords:
        words = [w for w in words if w not in STOP_WORDS]
    counter = Counter(words)
    return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))


def draw_bar(word_freq: dict, top_n: int):
    items = list(word_freq.items())[:top_n]
    if not items:
        return None
    words, freqs = zip(*items)

    fig, ax = plt.subplots(figsize=(9, max(4, len(words) * 0.45)))
    fig.patch.set_facecolor("#0d0d14")
    ax.set_facecolor("#0d0d14")

    colors = ["#5c5cff" if i == 0 else "#3a3a99" if i < 3 else "#252540"
              for i in range(len(words))]

    bars = ax.barh(list(reversed(words)), list(reversed(freqs)),
                   color=list(reversed(colors)), edgecolor="none", height=0.6)

    for bar, freq in zip(bars, reversed(freqs)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(freq), va="center", ha="left",
                color="#ffffff", fontsize=9, fontfamily="monospace", fontweight="bold")

    ax.set_xlabel("Frekuensi", color="#6b6b8a", fontsize=9, fontfamily="monospace")
    ax.set_title(f"Top {top_n} Kata Terbanyak", color="#ffffff",
                 fontsize=13, fontweight="bold", fontfamily="monospace", pad=14)
    ax.tick_params(colors="#9090b0", labelsize=9)
    ax.xaxis.label.set_color("#6b6b8a")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a40")
    ax.set_xlim(0, max(freqs) * 1.2)

    plt.tight_layout()
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_result = st.columns([1, 1.6], gap="large")

with col_input:
    st.markdown("#### ✦ Input Komentar")

    default_text = """Produk ini bagus banget! Kualitasnya bagus dan harganya murah.
Saya suka banget sama produk ini, recommended banget deh!
Pengirimannya cepat, produk bagus, packing rapi. Bagus!
Mantap jiwa, produk kualitas terbaik dengan harga murah meriah.
Seller ramah, produk sesuai deskripsi, recommended seller ini!
Bagus banget produknya, udah order berkali-kali. Murah dan bagus!
Kualitas oke, harga murah, pengiriman cepat. Suka banget!"""

    komentar = st.text_area(
        "Masukkan komentar media sosial",
        value=default_text,
        height=220,
        help="Paste komentar dari Instagram, TikTok, Twitter, dll."
    )

    remove_sw = st.checkbox("Hilangkan kata umum (stop words)", value=True)
    top_n = st.slider("Tampilkan top N kata", min_value=5, max_value=30, value=10)

    analyze = st.button("🔍 Analisis Sekarang")

# ── Result ────────────────────────────────────────────────────────────────────
with col_result:
    if analyze or komentar:
        word_freq = count_words(komentar, remove_sw)

        if not word_freq:
            st.warning("Tidak ada kata yang ditemukan.")
        else:
            st.markdown("#### ✦ Bar Chart Frekuensi")
            fig = draw_bar(word_freq, top_n)
            if fig:
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Stats
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Kata Unik", len(word_freq))
            c2.metric("Kata Teratas", list(word_freq.keys())[0] if word_freq else "-")
            c3.metric("Frekuensi Tertinggi", list(word_freq.values())[0] if word_freq else 0)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Dictionary table
            st.markdown("#### ✦ Dictionary {Key: Value}")
            st.markdown("""
            <div class="info-card">
                <div class="info-card-title">Format: kata → frekuensi</div>
            </div>
            """, unsafe_allow_html=True)

            top_items = list(word_freq.items())[:top_n]
            rows = "".join(
                f"<tr><td>#{i+1}</td><td><b>{k}</b></td><td>{v}</td></tr>"
                for i, (k, v) in enumerate(top_items)
            )
            st.markdown(f"""
            <table class="dict-table">
                <thead><tr><th>#</th><th>Key (Kata)</th><th>Value (Frekuensi)</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a55;text-align:center;">
    WORD COUNT VISUALIZER · BUILT WITH STREAMLIT + MATPLOTLIB
</p>
""", unsafe_allow_html=True)