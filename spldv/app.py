# --- Fungsi Penyelesaian dan Plotting (Bagian yang Dikoreksi) ---

def solve_and_plot(a1, b1, c1, a2, b2, c2):
    
    # ... (kode perhitungan determinan D, Dx, Dy, dan setup plot lainnya) ...
    
    # 2. Setup Plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    # ... (sisa kode plotting garis dan analisis solusi) ...
        
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
    
    # BARIS PENTING: Tampilkan plot ke Streamlit
    st.pyplot(fig) 
    
    # BARIS KOREKSI: Tutup plot Matplotlib agar tidak terjadi masalah rendering saat rerunning
    plt.close(fig) 
    
    return D, Dx, Dy, solution_type, explanation

# --- Visualisasi dan Output Hasil ---

st.header("Visualisasi Geometris")

D, Dx, Dy, solution_type, explanation = solve_and_plot(a1, b1, c1, a2, b2, c2)
#  <-- PASTIKAN TAG INI DIHAPUS JIKA ANDA TIDAK MENGGUNAKANNYA SEBAGAI KOMENTAR!
