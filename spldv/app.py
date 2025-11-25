import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Virtual Lab Distribusi Normal")

st.title("🔔 Virtual Lab Distribusi Normal & Teorema Limit Pusat")
st.markdown("Eksplorasi bagaimana ukuran sampel memengaruhi distribusi rata-rata sampel.")

# --- Sidebar Input Parameter ---
st.sidebar.title("⚙️ Parameter Populasi")
mu = st.sidebar.slider("Rata-rata Populasi (μ)", 0, 100, 50)
sigma = st.sidebar.slider("Simpangan Baku Populasi (σ)", 1, 20, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("🔬 Parameter Sampling")
sample_size = st.sidebar.slider("Ukuran Sampel (n)", 2, 100, 5) # Ukuran n
num_samples = st.sidebar.slider("Jumlah Sampel Simulasi", 100, 5000, 1000) # Jumlah pengulangan

# --- Fungsi Plotting dan Simulasi ---

def plot_distributions(mu, sigma, n, N):
    
    # 1. Distribusi Populasi (Kurva Normal Asli)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    # y_pop = norm.pdf(x, mu, sigma) 
    
    # 2. Simulasi Pengambilan Sampel (Distribusi Rata-rata Sampel)
    sample_means = []
    for _ in range(N):
        # Ambil sampel dari populasi normal
        sample = np.random.normal(loc=mu, scale=sigma, size=n)
        sample_means.append(np.mean(sample))
        
    sample_means = np.array(sample_means)
    
    # Simpangan Baku Rata-rata Sampel (Standard Error)
    SE = sigma / np.sqrt(n)
    
    # --- Visualisasi ---
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Histogram Rata-rata Sampel
    ax.hist(sample_means, bins=30, density=True, alpha=0.6, color='skyblue', label=f'Rata-rata Sampel (n={n})')
    
    # Plot Kurva Normal Rata-rata Sampel (sesuai CLT)
    y_clt = norm.pdf(x, mu, SE)
    ax.plot(x, y_clt, 'red', linewidth=2, label=f'Kurva Teoritis (SE={SE:.2f})')
    
    # Plot Kurva Populasi (untuk perbandingan lebar)
    y_pop = norm.pdf(x, mu, sigma)
    ax.plot(x, y_pop, 'black', linestyle='--', alpha=0.5, label=f'Populasi (σ={sigma})')

    
    # Pengaturan Grafik
    ax.set_title(f'Distribusi Rata-rata Sampel vs. Populasi (N={N} kali simulasi)')
    ax.set_xlabel('Nilai Rata-rata')
    ax.set_ylabel('Probabilitas Densitas')
    ax.axvline(mu, color='green', linestyle='-', linewidth=1.5, label=f'μ = {mu}')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.5)
    
    st.pyplot(fig)
    plt.close(fig) # Tutup figure Matplotlib

    return sample_means, SE

# --- Bagian Utama Streamlit ---

st.header("Visualisasi Simulasi Sampling")

# Jalankan simulasi dan plot
sample_means, SE = plot_distributions(mu, sigma, sample_size, num_samples)


st.header("📊 Hasil Analisis Teorema Limit Pusat (CLT)")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Populasi")
    st.metric("Rata-rata Teoritis (μ)", f"{mu}")
    st.metric("Simpangan Baku (σ)", f"{sigma}")

with col2:
    st.subheader("Rata-rata Sampel")
    st.metric(f"Ukuran Sampel (n)", f"{sample_size}")
    st.metric(f"Rata-rata Histogram ($\overline{{\mu}}$)", f"{np.mean(sample_means):.2f}")


with col3:
    st.subheader("Efek Ukuran Sampel")
    st.info(f"Semakin besar **Ukuran Sampel ($n$)**, semakin kecil **Standard Error** (SE).")
    st.metric("Standard Error (SE)", f"{SE:.2f}")
    st.latex(f"SE = \\frac{{\\sigma}}{{\\sqrt{{n}}}} = \\frac{{{sigma}}}{{\\sqrt{{{sample_size}}}}} = {SE:.2f}")


st.markdown("---")
st.subheader("Kesimpulan CLT:")
st.markdown(
    "1. **Bentuk Distribusi:** Saat $n$ meningkat, histogram rata-rata sampel akan semakin menyerupai **Kurva Normal**, bahkan jika populasi aslinya tidak normal (walaupun kita menggunakan populasi normal di sini).\n"
    "2. **Akurasi:** Saat $n$ meningkat, **Standard Error (SE)** menurun, menyebabkan kurva rata-rata sampel menjadi **lebih ramping dan tinggi** di sekitar $\mu$. Ini menunjukkan bahwa rata-rata sampel lebih akurat mencerminkan rata-rata populasi."
)
