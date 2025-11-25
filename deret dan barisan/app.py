import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Virtual Lab Deret dan Barisan")

st.title("🔢 Virtual Lab Deret & Barisan Interaktif")
st.markdown("Eksplorasi **Barisan Aritmatika** (pertumbuhan linear) dan **Barisan Geometri** (pertumbuhan eksponensial), serta perhitungan Deretnya.")

# --- Sidebar untuk Pengaturan Utama ---
st.sidebar.title("⚙️ Pengaturan Barisan")

# Pilihan Jenis Barisan
sequence_type = st.sidebar.selectbox(
    "Pilih Jenis Barisan",
    ("Aritmatika", "Geometri")
)

st.sidebar.subheader("➡️ Parameter")
a = st.sidebar.number_input("Suku Awal (a)", value=2)
n_max = st.sidebar.slider("Batas Suku (N)", 5, 20, 10)

# Parameter Khusus
if sequence_type == "Aritmatika":
    diff_or_ratio = st.sidebar.slider("Beda (b)", -5.0, 5.0, 3.0)
    b = diff_or_ratio
    
elif sequence_type == "Geometri":
    # Untuk Geometri, faktor skala (rasio) sangat sensitif. Batas 2.0 agar grafik tetap terlihat baik.
    diff_or_ratio = st.sidebar.slider("Rasio (r)", -2.0, 2.0, 1.5)
    r = diff_or_ratio

# --- Fungsi Perhitungan Barisan dan Deret ---

def calculate_sequences(a, param, N, type):
    """Menghitung suku (Un) dan jumlah deret (Sn)"""
    U = np.zeros(N)
    S = np.zeros(N)
    
    current_sum = 0
    for i in range(N):
        n = i + 1 # n dimulai dari 1
        
        if type == "Aritmatika":
            # Un = a + (n-1)b
            Un = a + (n - 1) * param 
        elif type == "Geometri":
            # Un = a * r^(n-1)
            Un = a * (param ** (n - 1))
            
        U[i] = Un
        current_sum += Un
        S[i] = current_sum
        
    return U, S

# Hitung hasil
U_n, S_n = calculate_sequences(a, diff_or_ratio, n_max, sequence_type)
indices = np.arange(1, n_max + 1) # Indeks n = 1, 2, 3, ... N

# --- Bagian Utama: Visualisasi ---
st.header(f"Visualisasi Barisan {sequence_type}")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Grafik Nilai Suku ($U_n$)")
    fig_u, ax_u = plt.subplots(figsize=(6, 4))
    
    # Plot Un vs n
    if sequence_type == "Aritmatika":
        ax_u.plot(indices, U_n, 'bo-', label='Barisan Aritmatika', linewidth=2)
        ax_u.set_title(f'Pertumbuhan Linear (Beda = {b})')
    else:
        ax_u.plot(indices, U_n, 'ro-', label='Barisan Geometri', linewidth=2)
        ax_u.set_title(f'Pertumbuhan Eksponensial (Rasio = {r})')
        
    ax_u.set_xlabel("Indeks Suku (n)")
    ax_u.set_ylabel("Nilai Suku ($U_n$)")
    ax_u.grid(True, linestyle=':', alpha=0.7)
    ax_u.legend()
    st.pyplot(fig_u)


with col2:
    st.subheader("Grafik Jumlah Deret ($S_n$)")
    fig_s, ax_s = plt.subplots(figsize=(6, 4))
    
    # Plot Sn vs n
    ax_s.plot(indices, S_n, 'g^-', label='Jumlah Deret', linewidth=2)
    ax_s.set_title(f'Akumulasi {sequence_type}')
    ax_s.set_xlabel("Indeks Suku (n)")
    ax_s.set_ylabel("Jumlah Deret ($S_n$)")
    ax_s.grid(True, linestyle=':', alpha=0.7)
    ax_s.legend()
    st.pyplot(fig_s)

# --- Detail Matematis dan Hasil ---
st.markdown("---")
st.header("📚 Detail Perhitungan")

# 1. Matriks Hasil
data = {
    'n': indices,
    f'Un (Suku ke-{sequence_type})': np.round(U_n, 4),
    f'Sn (Jumlah Deret)': np.round(S_n, 4)
}
# Pastikan data frame ditampilkan di layar
st.dataframe(data, height=300)

# 2. Rumus dan Penjelasan
st.subheader("Rumus Utama")

if sequence_type == "Aritmatika":
    st.markdown(f"**Barisan Aritmatika** (Beda, $b = {b}$)")
    st.latex(f"U_n = a + (n-1)b \\rightarrow U_n = {a} + (n-1){b}")
    st.latex(f"S_n = \\frac{{n}}{{2}} (a + U_n) \\text{{ atau }} S_n = \\frac{{n}}{{2}} (2a + (n-1)b)")

elif sequence_type == "Geometri":
    st.markdown(f"**Barisan Geometri** (Rasio, $r = {r}$)")
    st.latex(f"U_n = a \\cdot r^{{n-1}} \\rightarrow U_n = {a} \\cdot ({r})^{{n-1}}")
    st.latex(f"S_n = \\frac{{a(r^n - 1)}}{{r-1}} \\text{{ untuk }} r \\ne 1")
    
    # Konvergensi untuk Geometri Tak Hingga
    if np.abs(r) < 1:
        S_inf = a / (1 - r)
        st.subheader("Deret Geometri Tak Hingga (Konvergen)")
        st.info(f"Karena $|r| = |{r}| < 1$, deret ini **Konvergen** (memiliki jumlah tak hingga yang terbatas).")
        st.latex(f"S_\\infty = \\frac{{a}}{{1-r}} = \\frac{{{a}}}{{1 - ({r})}} = {np.round(S_inf, 4)}")
        
    else:
        st.info(f"Karena $|r| = |{r}| \\ge 1$, deret ini **Divergen** (tidak memiliki jumlah tak hingga yang terbatas).")

# --- Kesimpulan ---
st.markdown("---")
st.write(
    f"Dengan Lab ini, siswa dapat melihat bagaimana perubahan **Suku Awal** ($a$), **Beda** ($b$), atau **Rasio** ($r$) mengubah pola pertumbuhan barisan. Perhatikan perbedaan jelas antara pertumbuhan **Linear** (Aritmatika) dan **Eksponensial** (Geometri)!"
)
