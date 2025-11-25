import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Virtual Lab SPLDV Interaktif")

st.title("📐 Virtual Lab Sistem Persamaan Linear Dua Variabel (SPLDV)")
st.markdown("Ubah koefisien di sidebar untuk melihat efeknya pada grafik, jenis solusi, dan determinan matriks.")

# --- Sidebar untuk Input Koefisien (INTERAKTIF) ---
st.sidebar.title("⚙️ Input Persamaan")

# Persamaan 1: a1x + b1y = c1
st.sidebar.header("Persamaan 1: $a_1x + b_1y = c_1$")
a1 = st.sidebar.slider("Koefisien $a_1$", -5, 5, 2)
b1 = st.sidebar.slider("Koefisien $b_1$", -5, 5, 1)
c1 = st.sidebar.number_input("Konstanta $c_1$", value=4.0)

# Persamaan 2: a2x + b2y = c2
st.sidebar.header("Persamaan 2: $a_2x + b_2y = c_2$")
a2 = st.sidebar.slider("Koefisien $a_2$", -5, 5, 1)
b2 = st.sidebar.slider("Koefisien $b_2$", -5, 5, -1)
c2 = st.sidebar.number_input("Konstanta $c_2$", value=2.0)

# Penanganan kasus ekstrem untuk plotting (menghindari division by zero)
if b1 == 0 and a1 == 0:
    st.sidebar.warning("a1 dan b1 tidak boleh nol bersamaan! Nilai a1 diatur ke 1.")
    a1 = 1
if b2 == 0 and a2 == 0:
    st.sidebar.warning("a2 dan b2 tidak boleh nol bersamaan! Nilai a2 diatur ke 1.")
    a2 = 1


# --- Fungsi Penyelesaian dan Plotting ---

def solve_and_plot(a1, b1, c1, a2, b2, c2):
    
    # 1. Hitung Determinan Matriks (Aturan Cramer)
    D = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1
    
    # 2. Setup Plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    x = np.linspace(-10, 10, 400) # Rentang nilai X untuk plotting
    
    # Inisialisasi
    solution_type = "Tidak Diketahui"
    explanation = "Silakan ubah koefisien untuk memulai analisis."
    
    # --- Analisis Jenis Solusi ---
    
    if D != 0:
        # **A. Solusi Tunggal (Garis Berpotongan)**
        sol_x = Dx / D
        sol_y = Dy / D
        solution_type = "Solusi Tunggal"
        explanation = f"Determinan $D \\ne 0$. Kedua garis berpotongan pada satu titik: **({sol_x:.2f}, {sol_y:.2f})**."
        
        # Plot Garis 1 
        if b1 != 0:
            y1 = (c1 - a1 * x) / b1
            ax.plot(x, y1, 'b-', label=f'Garis 1: {a1}x + {b1}y = {c1}')
        else:
            ax.axvline(c1 / a1, color='blue', linestyle='-', label=f'Garis 1: x = {c1/a1:.2f}')
            
        # Plot Garis 2
        if b2 != 0:
            y2 = (c2 - a2 * x) / b2
            ax.plot(x, y2, 'r--', label=f'Garis 2: {a2}x + {b2}y = {c2}')
        else:
            ax.axvline(c2 / a2, color='red', linestyle='--', label=f'Garis 2: x = {c2/a2:.2f}')
            
        # Plot titik perpotongan (Solusi)
        ax.plot(sol_x, sol_y, 'ko', markersize=8, label='Titik Solusi')
        ax.text(sol_x + 0.3, sol_y, f'({sol_x:.2f}, {sol_y:.2f})', color='black', fontsize=10)

    elif D == 0 and (Dx != 0 or Dy != 0):
        # **B. Tidak Ada Solusi (Garis Sejajar)**
        solution_type = "Tidak Ada Solusi"
        explanation = "Determinan $D = 0$ tetapi $D_x \\ne 0$ atau $D_y \\ne 0$. Kedua garis **Sejajar** dan tidak pernah berpotongan."
        
        # Plot kedua garis sejajar
        if b1 != 0:
            y1 = (c1 - a1 * x) / b1
            ax.plot(x, y1, 'b-', label=f'Garis 1: {a1}x + {b1}y = {c1}')
        if b2 != 0:
            y2 = (c2 - a2 * x) / b2
            ax.plot(x, y2, 'r--', label=f'Garis 2: {a2}x + {b2}y = {c2}')
        
    elif D == 0 and Dx == 0 and Dy == 0:
        # **C. Solusi Tak Hingga (Garis Berimpit)**
        solution_type = "Solusi Tak Hingga"
        explanation = "Determinan $D = D_x = D_y = 0$. Kedua persamaan adalah kelipatan satu sama lain. Garis **Berimpit**."
        
        # Plot garis berimpit
        if b1 != 0:
            y1 = (c1 - a1 * x) / b1
            ax.plot(x, y1, 'b-', label='Garis Berimpit (Garis 1)')
            ax.plot(x, y1, 'r--', alpha=0.5, label='Garis Berimpit (Garis 2)') 
        
    # Pengaturan Plot Umum
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_title(f"Visualisasi SPLDV: {solution_type}")
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    ax.legend(loc='upper right')
    
    st.pyplot(fig)
    # Penting: Tutup plot Matplotlib agar tidak terjadi bug rendering
    plt.close(fig) 
    
    return D, Dx, Dy, solution_type, explanation

# --- Visualisasi dan Output Hasil ---

st.header("Visualisasi Geometris") # <--- BARIS INI KINI AMAN KARENA SEMUA VARIABEL DI ATASNYA SUDAH DIDEFINISIKAN

D, Dx, Dy, solution_type, explanation = solve_and_plot(a1, b1, c1, a2, b2, c2)


st.header("📚 Analisis Hasil")

col_a, col_b = st.columns([1, 2])

with col_a:
    st.subheader("Jenis Solusi")
    if solution_type == "Solusi Tunggal":
        st.success(f"**{solution_type}**")
    elif solution_type == "Tidak Ada Solusi":
        st.error(f"**{solution_type}**")
    else:
        st.warning(f"**{solution_type}**")

with col_b:
    st.subheader("Penjelasan Geometris")
    st.info(explanation)

st.subheader("Matriks dan Determinan (Aturan Cramer)")

# Tampilkan Matriks Koefisien A
st.markdown("**Matriks Koefisien (A):**")
st.latex(f"A = \\begin{{pmatrix}} {a1} & {b1} \\\\ {a2} & {b2} \\end{{pmatrix}}")

# Tampilkan Determinan
st.markdown(f"**Determinan Utama (D):**")
st.latex(f"
