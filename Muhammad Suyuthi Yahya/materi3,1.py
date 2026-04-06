import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge
import math

st.set_page_config(page_title="Visualisasi Operasi Set", layout="wide")

def create_venn_diagram(set_a, set_b, operation="union"):
    """Membuat diagram Venn untuk operasi set"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Warna untuk set A dan B
    color_a = '#FF6B6B'
    color_b = '#4ECDC4'
    alpha = 0.4
    
    # Posisi pusat lingkaran
    center_a = (3, 5)
    center_b = (7, 5)
    radius = 2.5
    
    # Gambar lingkaran set A
    circle_a = Circle(center_a, radius, color=color_a, alpha=alpha, edgecolor='black', linewidth=2)
    ax.add_patch(circle_a)
    
    # Gambar lingkaran set B
    circle_b = Circle(center_b, radius, color=color_b, alpha=alpha, edgecolor='black', linewidth=2)
    ax.add_patch(circle_b)
    
    # Hitung hasil operasi
    if operation == "union":
        result = set_a | set_b
        title = "Union (A ∪ B)"
        # Highlight area union
        ax.add_patch(Wedge(center_a, radius, 0, 360, color=color_a, alpha=0.2))
        ax.add_patch(Wedge(center_b, radius, 0, 360, color=color_b, alpha=0.2))
        
    elif operation == "intersection":
        result = set_a & set_b
        title = "Intersection (A ∩ B)"
        # Highlight area intersection
        intersection_wedge = Wedge((5, 5), 1.8, 180, 360, color='yellow', alpha=0.7)
        ax.add_patch(intersection_wedge)
        
    elif operation == "difference":
        result = set_a - set_b
        title = "Difference (A - B)"
        # Highlight hanya area A yang tidak overlap
        diff_wedge = Wedge(center_a, radius, 270, 450, color=color_a, alpha=0.6)
        ax.add_patch(diff_wedge)
        
    elif operation == "symmetric_difference":
        result = (set_a - set_b) | (set_b - set_a)
        title = "Symmetric Difference (A Δ B)"
        # Highlight area symmetric difference
        sym_a = Wedge(center_a, radius, 270, 450, color=color_a, alpha=0.6)
        sym_b = Wedge(center_b, radius, 90, 270, color=color_b, alpha=0.6)
        ax.add_patch(sym_a)
        ax.add_patch(sym_b)
    
    # Label set A dan B
    ax.text(3, 8.5, f'A = {set_a}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(7, 8.5, f'B = {set_b}', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Label hasil
    ax.text(5, 1, f'{title} = {result}', ha='center', va='center', 
            fontsize=16, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    # Tambahkan elemen set di posisi yang tepat
    plot_set_elements(ax, set_a, center_a, radius, color_a, "A")
    plot_set_elements(ax, set_b, center_b, radius, color_b, "B")
    
    plt.title(f'Visualisasi Operasi Set: {title}', fontsize=18, fontweight='bold', pad=20)
    return fig

def plot_set_elements(ax, set_data, center, radius, color, label):
    """Menempatkan elemen set di posisi yang tepat dalam diagram Venn"""
    elements = list(set_data)
    n_elements = len(elements)
    
    if n_elements == 0:
        return
    
    # Posisi angular untuk elemen
    angles = np.linspace(0, 2*np.pi, min(n_elements, 8))
    
    for i, elem in enumerate(elements[:8]):  # Maksimal 8 elemen
        angle = angles[i]
        x = center[0] + (radius * 0.6) * np.cos(angle)
        y = center[1] + (radius * 0.6) * np.sin(angle)
        ax.text(x, y, str(elem), ha='center', va='center', 
                fontsize=12, fontweight='bold', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor=color, alpha=0.8))

def main():
    st.title("🧮 Visualisasi Operasi Set")
    st.markdown("---")
    
    # Sidebar untuk input
    st.sidebar.header("⚙️ Pengaturan Set")
    
    # Input Set A
    st.sidebar.subheader("Set A")
    a_input = st.sidebar.text_input("Elemen Set A (pisahkan dengan koma)", "1,3,5,7")
    try:
        set_a = set(map(int, [x.strip() for x in a_input.split(',') if x.strip().isdigit()]))
    except:
        set_a = set([1,3,5,7])
    
    # Input Set B
    st.sidebar.subheader("Set B")
    b_input = st.sidebar.text_input("Elemen Set B (pisahkan dengan koma)", "2,3,5,8")
    try:
        set_b = set(map(int, [x.strip() for x in b_input.split(',') if x.strip().isdigit()]))
    except:
        set_b = set([2,3,5,8])
    
    # Pilihan operasi
    operation = st.sidebar.selectbox(
        "Pilih Operasi Set:",
        ["union", "intersection", "difference", "symmetric_difference"],
        format_func=lambda x: {
            "union": "Union (A ∪ B)",
            "intersection": "Intersection (A ∩ B)", 
            "difference": "Difference (A - B)",
            "symmetric_difference": "Symmetric Difference (A Δ B)"
        }[x]
    )
    
    op_names = {
        "union": "Union (A ∪ B)",
        "intersection": "Intersection (A ∩ B)",
        "difference": "Difference (A - B)",
        "symmetric_difference": "Symmetric Difference (A Δ B)"
    }
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Visualisasi Diagram Venn")
        fig = create_venn_diagram(set_a, set_b, operation)
        st.pyplot(fig)
    
    with col2:
        st.subheader("📋 Tabel Hasil Operasi")
        
        # Hitung semua operasi
        union_result = set_a | set_b
        inter_result = set_a & set_b
        diff_result = set_a - set_b
        sym_diff_result = (set_a - set_b) | (set_b - set_a)
        
        results = {
            "Union (A ∪ B)": union_result,
            "Intersection (A ∩ B)": inter_result,
            "Difference (A - B)": diff_result,
            "Symmetric Diff (A Δ B)": sym_diff_result
        }
        
        # Highlight operasi yang dipilih
        for op_name, result in results.items():
            bg_color = "lightgreen" if op_name == op_names[operation] else "white"
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0;">
                <strong>{op_name}</strong>: {result}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info(f"**Set A**: {set_a}\n**Set B**: {set_b}")
    
    # Info tambahan
    st.markdown("---")
    st.markdown("""
    ## 📖 Penjelasan Operasi Set
    - **Union (A ∪ B)**: Menggabungkan semua elemen unik dari A dan B
    - **Intersection (A ∩ B)**: Elemen yang ada di kedua set A dan B
    - **Difference (A - B)**: Elemen yang ada di A tapi tidak di B
    - **Symmetric Difference (A Δ B)**: Elemen yang ada di A atau B, tapi tidak di keduanya
    """)

if __name__ == "__main__":
    main()