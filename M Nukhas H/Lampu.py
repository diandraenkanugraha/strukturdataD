import streamlit as st
import time

# ─────────────────────────────────────────────
#  Circular Linked List Implementation
# ─────────────────────────────────────────────

class Node:
    """A single node in the circular linked list."""
    def __init__(self, color: str, duration: int, emoji: str, hex_color: str):
        self.color     = color       # Light name
        self.duration  = duration    # Duration in seconds
        self.emoji     = emoji       # Display emoji
        self.hex_color = hex_color   # CSS color
        self.next: "Node | None" = None


class CircularLinkedList:
    """Circular linked list that cycles through traffic light states."""
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def append(self, color: str, duration: int, emoji: str, hex_color: str) -> None:
        new_node = Node(color, duration, emoji, hex_color)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node          # points to itself
        else:
            self.tail.next = new_node         # type: ignore[union-attr]
            new_node.next  = self.head        # close the circle
            self.tail      = new_node
        self.size += 1

    def traverse(self):
        """Yield every node once (one full cycle)."""
        if self.head is None:
            return
        current = self.head
        for _ in range(self.size):
            yield current
            current = current.next            # type: ignore[assignment]


# ─────────────────────────────────────────────
#  Build the traffic-light list
# ─────────────────────────────────────────────

def build_traffic_light() -> CircularLinkedList:
    cll = CircularLinkedList()
    cll.append("Merah",  40, "🔴", "#FF3B3B")
    cll.append("Hijau",  20, "🟢", "#2ECC71")
    cll.append("Kuning",  5, "🟡", "#F1C40F")
    return cll


# ─────────────────────────────────────────────
#  Streamlit UI
# ─────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Traffic Light – Circular Linked List",
                       page_icon="🚦", layout="centered")

    st.title("🚦 Simulasi Lampu Lalu Lintas")
    st.caption("Struktur Data – Circular Linked List")

    # ── Sidebar: show the list structure ────────────────────────────────────
    with st.sidebar:
        st.header("📋 Circular Linked List")
        cll = build_traffic_light()
        for i, node in enumerate(cll.traverse()):
            st.markdown(
                f"**Node {i+1}** &nbsp; {node.emoji} &nbsp; `{node.color}`  \n"
                f"Durasi: **{node.duration} detik**  \n"
                f"next → Node {(i % cll.size) + 2 if i < cll.size - 1 else 1}"
            )
            if i < cll.size - 1:
                st.markdown("↓")
        st.markdown("↑ *(kembali ke Node 1)*")

    # ── Main area: controls ──────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    speed = col1.slider("Kecepatan (×)", min_value=1, max_value=20,
                        value=1, help="Kalikan kecepatan simulasi")
    cycles = col2.number_input("Jumlah Siklus", min_value=1, max_value=20,
                               value=2, step=1)
    start  = col3.button("▶ Mulai Simulasi", use_container_width=True)

    # ── Placeholders ────────────────────────────────────────────────────────
    info_box   = st.empty()
    light_box  = st.empty()
    timer_box  = st.empty()
    progress   = st.progress(0)
    cycle_info = st.empty()

    info_box.info("Tekan **▶ Mulai Simulasi** untuk memulai.", icon="ℹ️")

    # ── Simulation loop ──────────────────────────────────────────────────────
    if start:
        info_box.empty()
        cll = build_traffic_light()

        for cycle in range(1, int(cycles) + 1):
            for node in cll.traverse():

                # ── draw the traffic-light box ──────────────────────────────
                bulb_red    = "🔴" if node.color == "Merah"  else "⚫"
                bulb_yellow = "🟡" if node.color == "Kuning" else "⚫"
                bulb_green  = "🟢" if node.color == "Hijau"  else "⚫"

                light_box.markdown(
                    f"""
<div style="
    background:#1a1a2e;
    border-radius:18px;
    padding:30px 0;
    width:160px;
    margin:auto;
    text-align:center;
    box-shadow: 0 0 30px {node.hex_color}88;
    border: 3px solid {node.hex_color};
">
<div style='font-size:60px;line-height:1.3'>{bulb_red}</div>
<div style='font-size:60px;line-height:1.3'>{bulb_yellow}</div>
<div style='font-size:60px;line-height:1.3'>{bulb_green}</div>
</div>
<h2 style='text-align:center;color:{node.hex_color};margin-top:12px'>
  Lampu {node.color}
</h2>
""",
                    unsafe_allow_html=True,
                )

                cycle_info.markdown(
                    f"🔄 **Siklus {cycle} / {cycles}** &nbsp;|&nbsp; "
                    f"⏱ Durasi: **{node.duration} detik**"
                )

                # ── countdown ───────────────────────────────────────────────
                total = node.duration
                for remaining in range(total, 0, -1):
                    elapsed  = total - remaining
                    pct      = elapsed / total
                    progress.progress(pct)
                    timer_box.markdown(
                        f"<h3 style='text-align:center;color:{node.hex_color}'>"
                        f"⏳ {remaining} detik tersisa</h3>",
                        unsafe_allow_html=True,
                    )
                    time.sleep(1 / speed)

                progress.progress(1.0)
                timer_box.markdown(
                    f"<h3 style='text-align:center;color:{node.hex_color}'>"
                    f"✅ Selesai!</h3>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.3 / speed)

        # ── done ─────────────────────────────────────────────────────────────
        light_box.empty()
        timer_box.empty()
        progress.empty()
        cycle_info.empty()
        st.success(f"🎉 Simulasi selesai! {cycles} siklus telah berjalan.", icon="✅")
        st.balloons()


if __name__ == "__main__":
    main()