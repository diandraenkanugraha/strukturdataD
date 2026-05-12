import streamlit as st
import time
import random

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Search Algorithm Visualizer",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* ── dark background ── */
.stApp {
    background: #0d0d14;
    color: #e8e8f0;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #13131f;
    border-right: 1px solid #2a2a40;
}

/* ── title strip ── */
.title-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 24px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #2a2a50;
    border-radius: 12px;
    margin-bottom: 28px;
}
.title-bar h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #7c83fd, #fd7cd0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.title-bar .icon { font-size: 2.4rem; }

/* ── array cell ── */
.array-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 24px;
    background: #13131f;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    min-height: 90px;
    margin-bottom: 20px;
}
.cell {
    width: 58px;
    height: 58px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.1rem;
    transition: all 0.25s ease;
    position: relative;
}
.cell .idx {
    font-size: 0.6rem;
    font-weight: 400;
    opacity: .55;
    position: absolute;
    top: 4px;
    left: 50%;
    transform: translateX(-50%);
}
/* states */
.cell-default  { background:#1e1e30; border:2px solid #2a2a45; color:#c8c8e0; }
.cell-visited  { background:#1e2a3a; border:2px solid #3a6080; color:#7ab8e8; }
.cell-current  { background:#2a1e3a; border:2px solid #9060c0; color:#d090ff;
                 box-shadow: 0 0 12px #9060c080; transform:scale(1.08); }
.cell-found    { background:#1a3020; border:2px solid #40c060; color:#60f090;
                 box-shadow: 0 0 16px #40c06080; transform:scale(1.12); }
.cell-range    { background:#1e2a1e; border:2px dashed #405040; color:#80a080; }
.cell-mid      { background:#2a2a10; border:2px solid #c0a020; color:#ffd040;
                 box-shadow: 0 0 12px #c0a02060; transform:scale(1.1); }
.cell-eliminated { background:#1a1014; border:2px solid #402030; color:#604050; opacity:.45; }

/* ── info cards ── */
.info-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}
.card {
    flex: 1;
    padding: 14px 18px;
    border-radius: 10px;
    background: #13131f;
    border: 1px solid #2a2a40;
}
.card .label { font-size: .7rem; letter-spacing:.08em; text-transform:uppercase; opacity:.55; }
.card .value { font-size: 1.6rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
.card-steps  .value { color: #7c83fd; }
.card-comps  .value { color: #fd7cd0; }
.card-status .value { font-size: 1.1rem; }

/* ── log box ── */
.log-box {
    background: #0a0a12;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .8rem;
    line-height: 1.7;
    max-height: 260px;
    overflow-y: auto;
}
.log-info    { color: #7ab8e8; }
.log-action  { color: #d090ff; }
.log-success { color: #60f090; }
.log-fail    { color: #f07070; }

/* ── legend ── */
.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 14px 18px;
    background: #13131f;
    border: 1px solid #2a2a40;
    border-radius: 10px;
    margin-bottom: 20px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: .78rem;
}
.dot {
    width: 14px; height: 14px;
    border-radius: 4px;
}
.dot-default    { background:#1e1e30; border:2px solid #2a2a45; }
.dot-visited    { background:#1e2a3a; border:2px solid #3a6080; }
.dot-current    { background:#2a1e3a; border:2px solid #9060c0; }
.dot-found      { background:#1a3020; border:2px solid #40c060; }
.dot-mid        { background:#2a2a10; border:2px solid #c0a020; }
.dot-eliminated { background:#1a1014; border:2px solid #402030; opacity:.5; }

/* ── buttons ── */
div.stButton > button {
    background: linear-gradient(135deg, #7c83fd, #fd7cd0);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: .95rem;
    padding: 10px 24px;
    cursor: pointer;
    width: 100%;
}
div.stButton > button:hover { opacity: .88; }

/* ── complexity badge ── */
.complexity {
    padding: 10px 16px;
    background: #13131f;
    border: 1px solid #2a2a40;
    border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .82rem;
    line-height: 1.8;
    margin-top: 10px;
}
.complexity span { color: #fd7cd0; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
defaults = {
    "array": [],
    "steps": [],
    "current_step": -1,
    "running": False,
    "result_index": -1,
    "log": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  Algorithm generators
# ─────────────────────────────────────────────
def linear_search_steps(arr, target):
    steps, log = [], []
    log.append(("info", f"Mulai Linear Search — target: <b>{target}</b>"))
    for i, val in enumerate(arr):
        state = ["current" if j == i else ("visited" if j < i else "default") for j in range(len(arr))]
        log.append(("action", f"[{i}] Periksa arr[{i}] = {val}"))
        steps.append({"states": state[:], "log": list(log), "comparisons": i + 1})
        if val == target:
            state[i] = "found"
            log.append(("success", f"✓ Ditemukan di indeks {i}!"))
            steps.append({"states": state[:], "log": list(log), "found": i, "comparisons": i + 1})
            return steps, i
    log.append(("fail", f"✗ {target} tidak ditemukan dalam array."))
    steps.append({"states": ["visited"] * len(arr), "log": list(log), "found": -1, "comparisons": len(arr)})
    return steps, -1


def binary_search_steps(arr, target):
    arr_s = sorted(arr)
    steps, log = [], []
    lo, hi = 0, len(arr_s) - 1
    comparisons = 0
    log.append(("info", f"Mulai Binary Search — target: <b>{target}</b> (array diurutkan)"))

    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        state = []
        for j in range(len(arr_s)):
            if j < lo or j > hi:
                state.append("eliminated")
            elif j == mid:
                state.append("mid")
            else:
                state.append("range")
        log.append(("action", f"lo={lo}, hi={hi}, mid={mid} → arr[{mid}]={arr_s[mid]}"))
        steps.append({"states": state[:], "log": list(log), "arr": arr_s, "comparisons": comparisons})
        if arr_s[mid] == target:
            state[mid] = "found"
            log.append(("success", f"✓ Ditemukan di indeks {mid}!"))
            steps.append({"states": state[:], "log": list(log), "arr": arr_s, "found": mid, "comparisons": comparisons})
            return steps, mid, arr_s
        elif arr_s[mid] < target:
            log.append(("action", f"arr[{mid}]={arr_s[mid]} < {target} → geser lo ke {mid+1}"))
            lo = mid + 1
        else:
            log.append(("action", f"arr[{mid}]={arr_s[mid]} > {target} → geser hi ke {mid-1}"))
            hi = mid - 1

    log.append(("fail", f"✗ {target} tidak ditemukan dalam array."))
    steps.append({"states": ["eliminated"] * len(arr_s), "log": list(log), "arr": arr_s, "found": -1, "comparisons": comparisons})
    return steps, -1, arr_s


def jump_search_steps(arr, target):
    import math
    arr_s = sorted(arr)
    n = len(arr_s)
    step = int(math.sqrt(n))
    steps, log = [], []
    comparisons = 0
    log.append(("info", f"Mulai Jump Search — target: <b>{target}</b>, step=√{n}≈{step}"))

    prev = 0
    curr = step
    while curr < n and arr_s[min(curr, n) - 1] < target:
        comparisons += 1
        state = ["eliminated" if j < prev else ("visited" if j <= min(curr, n) - 1 else "default") for j in range(n)]
        state[min(curr, n) - 1] = "current"
        log.append(("action", f"Lompat ke blok [{prev}..{min(curr,n)-1}], arr[{min(curr,n)-1}]={arr_s[min(curr,n)-1]}"))
        steps.append({"states": state[:], "log": list(log), "arr": arr_s, "comparisons": comparisons})
        prev = curr
        curr += step

    log.append(("action", f"Target mungkin di blok [{prev}..{min(curr,n)-1}] — Linear scan"))
    for i in range(prev, min(curr, n)):
        comparisons += 1
        state = ["eliminated" if j < prev else ("current" if j == i else ("visited" if j < i else "default")) for j in range(n)]
        log.append(("action", f"Periksa arr[{i}]={arr_s[i]}"))
        steps.append({"states": state[:], "log": list(log), "arr": arr_s, "comparisons": comparisons})
        if arr_s[i] == target:
            state[i] = "found"
            log.append(("success", f"✓ Ditemukan di indeks {i}!"))
            steps.append({"states": state[:], "log": list(log), "arr": arr_s, "found": i, "comparisons": comparisons})
            return steps, i, arr_s

    log.append(("fail", f"✗ {target} tidak ditemukan."))
    steps.append({"states": ["visited"] * n, "log": list(log), "arr": arr_s, "found": -1, "comparisons": comparisons})
    return steps, -1, arr_s


# ─────────────────────────────────────────────
#  Render helpers
# ─────────────────────────────────────────────
def render_array(arr, states):
    cells = ""
    for i, (val, s) in enumerate(zip(arr, states)):
        cells += f'<div class="cell cell-{s}"><span class="idx">{i}</span>{val}</div>'
    return f'<div class="array-wrapper">{cells}</div>'


def render_log(log_entries):
    lines = ""
    for cls, msg in log_entries[-20:]:
        lines += f'<div class="log-{cls}">{msg}</div>'
    return f'<div class="log-box">{lines}</div>'


def render_info(steps_n, comps, status_html):
    return f"""
<div class="info-row">
  <div class="card card-steps"><div class="label">Langkah</div><div class="value">{steps_n}</div></div>
  <div class="card card-comps"><div class="label">Perbandingan</div><div class="value">{comps}</div></div>
  <div class="card card-status"><div class="label">Status</div><div class="value">{status_html}</div></div>
</div>"""


# ─────────────────────────────────────────────
#  Sidebar controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Kontrol")

    algo = st.selectbox(
        "Algoritma",
        ["Linear Search", "Binary Search", "Jump Search"],
        index=0,
    )

    st.markdown("---")
    st.markdown("#### Array")
    gen_mode = st.radio("Mode input", ["Acak", "Manual"], horizontal=True)

    if gen_mode == "Acak":
        n_elem = st.slider("Jumlah elemen", 5, 20, 10)
        arr_range = st.slider("Rentang nilai", 1, 100, (1, 50))
        if st.button("🎲 Generate Array"):
            st.session_state.array = random.sample(range(arr_range[0], arr_range[1] + 1), min(n_elem, arr_range[1] - arr_range[0] + 1))
            st.session_state.steps = []
            st.session_state.current_step = -1
            st.session_state.log = []
    else:
        raw = st.text_input("Masukkan nilai (pisah koma)", "5,12,3,8,21,7,15,30,1,9")
        if st.button("✔ Gunakan Array Ini"):
            try:
                st.session_state.array = [int(x.strip()) for x in raw.split(",") if x.strip()]
                st.session_state.steps = []
                st.session_state.current_step = -1
                st.session_state.log = []
            except ValueError:
                st.error("Input tidak valid — masukkan angka dipisah koma.")

    st.markdown("---")
    st.markdown("#### Target")
    # suggest a value that exists in array most of the time
    default_target = st.session_state.array[0] if st.session_state.array else 7
    target = st.number_input("Nilai yang dicari", value=default_target, step=1)

    st.markdown("---")
    speed = st.select_slider("Kecepatan animasi", ["Lambat", "Normal", "Cepat"], value="Normal")
    delay_map = {"Lambat": 1.0, "Normal": 0.5, "Cepat": 0.15}
    delay = delay_map[speed]

    st.markdown("---")
    run_btn = st.button("▶ Jalankan")
    step_btn = st.button("⏭ Step Berikutnya")
    reset_btn = st.button("↺ Reset")

    # Complexity info
    complexity_info = {
        "Linear Search": ("O(n)", "O(1)", "O(n)", "O(1)", "Tidak perlu urutan"),
        "Binary Search": ("O(log n)", "O(1)", "O(log n)", "O(1)", "Harus terurut"),
        "Jump Search": ("O(√n)", "O(1)", "O(√n)", "O(1)", "Harus terurut"),
    }
    best, avg, worst, space, note = complexity_info[algo]
    st.markdown(
        f"""<div class="complexity">
<b>Kompleksitas Waktu</b><br>
Best: <span>{best}</span> | Avg: <span>{avg}</span> | Worst: <span>{worst}</span><br>
Space: <span>{space}</span><br>
📌 {note}
</div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  Main area
# ─────────────────────────────────────────────
st.markdown(
    '<div class="title-bar"><span class="icon">🔍</span>'
    "<h1>Search Algorithm Visualizer</h1></div>",
    unsafe_allow_html=True,
)

# Legend
st.markdown(
    """<div class="legend">
<div class="legend-item"><div class="dot dot-default"></div> Default</div>
<div class="legend-item"><div class="dot dot-visited"></div> Sudah diperiksa</div>
<div class="legend-item"><div class="dot dot-current"></div> Sedang diperiksa</div>
<div class="legend-item"><div class="dot dot-mid"></div> Titik tengah</div>
<div class="legend-item"><div class="dot dot-found"></div> Ditemukan ✓</div>
<div class="legend-item"><div class="dot dot-eliminated"></div> Dieliminasi</div>
</div>""",
    unsafe_allow_html=True,
)

# Auto-generate array if empty
if not st.session_state.array:
    st.session_state.array = random.sample(range(1, 51), 10)

# ── Reset ──
if reset_btn:
    st.session_state.steps = []
    st.session_state.current_step = -1
    st.session_state.log = []
    st.rerun()

# ── Run (full animation) ──
if run_btn and st.session_state.array:
    arr = st.session_state.array

    if algo == "Linear Search":
        steps, found = linear_search_steps(arr, int(target))
        display_arr = arr
    elif algo == "Binary Search":
        steps, found, display_arr = binary_search_steps(arr, int(target))
    else:
        steps, found, display_arr = jump_search_steps(arr, int(target))

    st.session_state.steps = steps
    st.session_state.result_index = found

    placeholder_arr = st.empty()
    placeholder_info = st.empty()
    placeholder_log = st.empty()

    for step_i, step in enumerate(steps):
        states = step["states"]
        comps = step.get("comparisons", step_i + 1)
        log_e = step.get("log", [])
        d_arr = step.get("arr", display_arr)

        found_flag = step.get("found", None)
        if found_flag is not None:
            status = "✅ Ditemukan!" if found_flag >= 0 else "❌ Tidak ditemukan"
        else:
            status = f"🔎 Mencari <b>{int(target)}</b>..."

        placeholder_arr.markdown(render_array(d_arr, states), unsafe_allow_html=True)
        placeholder_info.markdown(render_info(step_i + 1, comps, status), unsafe_allow_html=True)
        placeholder_log.markdown(render_log(log_e), unsafe_allow_html=True)

        time.sleep(delay)

    st.session_state.current_step = len(steps) - 1

# ── Step mode ──
elif step_btn and st.session_state.array:
    arr = st.session_state.array

    if not st.session_state.steps:
        if algo == "Linear Search":
            steps, found = linear_search_steps(arr, int(target))
            display_arr = arr
        elif algo == "Binary Search":
            steps, found, display_arr = binary_search_steps(arr, int(target))
        else:
            steps, found, display_arr = jump_search_steps(arr, int(target))
        st.session_state.steps = steps
        st.session_state.result_index = found

    nxt = st.session_state.current_step + 1
    if nxt < len(st.session_state.steps):
        st.session_state.current_step = nxt

# ── Display current step ──
if st.session_state.steps and st.session_state.current_step >= 0:
    idx = st.session_state.current_step
    step = st.session_state.steps[idx]
    states = step["states"]
    comps = step.get("comparisons", idx + 1)
    log_e = step.get("log", [])
    d_arr = step.get("arr", st.session_state.array)

    found_flag = step.get("found", None)
    if found_flag is not None:
        status = "✅ Ditemukan!" if found_flag >= 0 else "❌ Tidak ditemukan"
    else:
        status = f"🔎 Mencari <b>{int(target)}</b>..."

    st.markdown(render_array(d_arr, states), unsafe_allow_html=True)
    st.markdown(render_info(idx + 1, comps, status), unsafe_allow_html=True)
    st.markdown(render_log(log_e), unsafe_allow_html=True)

    st.caption(f"Langkah {idx+1} / {len(st.session_state.steps)}")

else:
    # Initial display — no steps yet
    arr = st.session_state.array
    states = ["default"] * len(arr)
    st.markdown(render_array(arr, states), unsafe_allow_html=True)
    st.markdown(render_info(0, 0, "⏸ Siap — tekan <b>▶ Jalankan</b>"), unsafe_allow_html=True)
    st.markdown('<div class="log-box"><div class="log-info">Log pencarian akan muncul di sini...</div></div>', unsafe_allow_html=True)