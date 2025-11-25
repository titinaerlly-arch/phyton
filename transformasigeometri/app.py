import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Virtual Lab Transformasi Geometri")

st.title("🔬 Virtual Lab Transformasi Geometri Interaktif")
st.markdown("Eksplorasi Translasi, Rotasi, Refleksi, dan Dilatasi secara visual.")

# --- Definisi Bentuk Awal (Segitiga) ---
# Koordinat awal (x, y) dalam format Matriks: [[x1, x2, x3], [y1, y2, y3], [1, 1, 1]]
# Baris 1: Koordinat X
# Baris 2: Koordinat Y
# Baris 3: Untuk perhitungan homogen (Translasi/geser)
DEFAULT_POINTS = np.array([
    [1, 5, 3],
    [1, 1, 4],
    [1, 1, 1]
])

# --- Fungsi Transformasi Geometri ---

def apply_transform(points, matrix):
    """Menerapkan matriks transformasi ke koordinat titik."""
    # Mengalikan Matriks Transformasi dengan Matriks Koordinat
    transformed_points = matrix @ points
    return transformed_points

# 1. Translasi (Pergeseran)
def get_translation_matrix(tx, ty):
    """Matriks Translasi 3x3"""
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

# 2. Rotasi (Perputaran)
def get_rotation_matrix(angle_deg, cx=0, cy=0):
    """Matriks Rotasi 3x3 terhadap titik (cx, cy)"""
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    
    # 1. Geser ke Pusat (cx, cy)
    T_to_center = get_translation_matrix(-cx, -cy)
    # 2. Rotasi di Origin
    R = np.array([
        [cos_a, -sin_a, 0],
        [sin_a, cos_a, 0],
        [0, 0, 1]
    ])
    # 3. Geser kembali
    T_from_center = get_translation_matrix(cx, cy)
    
    # Kombinasi: T_from_center @ R @ T_to_center
    return T_from_center @ R @ T_to_center

# 3. Refleksi (Pencerminan)
def get_reflection_matrix(axis_type):
    """Matriks Refleksi 3x3"""
    if axis_type == "sumbu-X": # Refleksi thd y=0
        return np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
    elif axis_type == "sumbu-Y": # Refleksi thd x=0
        return np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    elif axis_type == "garis y=x":
        return np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
    elif axis_type == "garis y=-x":
        return np.array([
            [0, -1, 0],
            [-1, 0, 0],
            [0, 0, 1]
        ])
    # Bisa ditambahkan refleksi terhadap titik (0,0) / Origin
    elif axis_type == "titik (0,0)":
        return np.array([
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])

# 4. Dilatasi (Perkalian)
def get_dilation_matrix(k, cx=0, cy=0):
    """Matriks Dilatasi 3x3 terhadap titik (cx, cy)"""
    # 1. Geser ke Pusat (cx, cy)
    T_to_center = get_translation_matrix(-cx, -cy)
    # 2. Dilatasi di Origin
    D = np.array([
        [k, 0, 0],
        [0, k, 0],
        [0, 0, 1]
    ])
    # 3. Geser kembali
    T_from_center = get_translation_matrix(cx, cy)
    
    # Kombinasi: T_from_center @ D @ T_to_center
    return T_from_center @ D @ T_to_center


# --- Fungsi Plotting ---
def plot_transformation(original, transformed, title, explanation):
    """Fungsi untuk memvisualisasikan transformasi"""
    
    # Batas plot
    all_points = np.hstack((original, transformed))
    min_x, max_x = np.min(all_points[0, :]), np.max(all_points[0, :])
    min_y, max_y = np.min(all_points[1, :]), np.max(all_points[1, :])
    
    # Tambahkan padding untuk batas
    padding = 2
    x_min, x_max = min_x - padding, max_x + padding
    y_min, y_max = min_y - padding, max_y + padding
    
    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot bentuk awal (biru)
    ax.plot(
        np.append(original[0, :], original[0, 0]), 
        np.append(original[1, :], original[1, 0]), 
        'b-', marker='o', label='Bentuk Awal (P)'
    )
    # Label titik awal
    for i in range(original.shape[1]):
        ax.text(original[0, i], original[1, i] + 0.2, f'P{i+1}', color='blue')
        
    # Plot bentuk transformasi (merah)
    ax.plot(
        np.append(transformed[0, :], transformed[0, 0]), 
        np.append(transformed[1, :], transformed[1, 0]), 
        'r--', marker='x', label='Hasil Transformasi (P\')'
    )
    # Label titik transformasi
    for i in range(transformed.shape[1]):
        ax.text(transformed[0, i], transformed[1, i] - 0.3, f'P\'{i+1}', color='red')
        
    # Pengaturan plot
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_title(title)
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")
    ax.set_xlim(min(x_min, -10), max(x_max, 10))
    ax.set_ylim(min(y_min, -10), max(y_max, 10))
    ax.set_aspect('equal', adjustable='box')
    ax.legend()
    
    st.pyplot(fig)
    st.markdown(explanation)
    

# --- Sidebar untuk Pilihan dan Pengaturan ---
st.sidebar.title("⚙️ Pengaturan Transformasi")

# Pilihan Transformasi
transform_type = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ("Translasi", "Rotasi", "Refleksi", "Dilatasi")
)

# Input Koordinat Awal
st.sidebar.subheader("📍 Titik Awal Segitiga (P)")
p1_x = st.sidebar.number_input("P1 (x)", value=1)
p1_y = st.sidebar.number_input("P1 (y)", value=1)
p2_x = st.sidebar.number_input("P2 (x)", value=5)
p2_y = st.sidebar.number_input("P2 (y)", value=1)
p3_x = st.sidebar.number_input("P3 (x)", value=3)
p3_y = st.sidebar.number_input("P3 (y)", value=4)

# Update Koordinat Awal
original_points = np.array([
    [p1_x, p2_x, p3_x],
    [p1_y, p2_y, p3_y],
    [1, 1, 1]
])

# --- Logika Transformasi Berdasarkan Pilihan ---

explanation = ""
transform_matrix = np.identity(3) # Matriks identitas 3x3

if transform_type == "Translasi":
    st.sidebar.subheader("➡️ Parameter Translasi")
    tx = st.sidebar.slider("Pergeseran X (tx)", -10, 10, 3)
    ty = st.sidebar.slider("Pergeseran Y (ty)", -10, 10, 2)
    
    transform_matrix = get_translation_matrix(tx, ty)
    explanation = (
        f"**Translasi (Pergeseran)**: Setiap titik digeser sejauh **${tx}$** satuan horizontal (kanan/kiri) dan **${ty}$** satuan vertikal (atas/bawah)."
        f" Rumus: $P'(x', y') = P(x, y) + T({tx}, {ty})$.\n\n"
        f"Matriks Transformasi:\n$$\\begin{{pmatrix}} 1 & 0 & {tx} \\\\ 0 & 1 & {ty} \\\\ 0 & 0 & 1 \\end{{pmatrix}}$$"
    )
    
elif transform_type == "Rotasi":
    st.sidebar.subheader("🔄 Parameter Rotasi")
    angle = st.sidebar.slider("Sudut Rotasi (derajat)", -360, 360, 90)
    cx = st.sidebar.number_input("Pusat Rotasi X (cx)", value=0)
    cy = st.sidebar.number_input("Pusat Rotasi Y (cy)", value=0)
    
    transform_matrix = get_rotation_matrix(angle, cx, cy)
    explanation = (
        f"**Rotasi (Perputaran)**: Bentuk diputar sebesar **${angle}^\circ$** berlawanan arah jarum jam (jika positif) mengelilingi titik pusat **$({cx}, {cy})$**."
        f" Rotasi melibatkan perkalian matriks kosinus dan sinus sudut."
    )

elif transform_type == "Refleksi":
    st.sidebar.subheader("↔️ Parameter Refleksi")
    reflection_axis = st.sidebar.selectbox(
        "Pencerminan terhadap:",
        ("sumbu-X", "sumbu-Y", "garis y=x", "garis y=-x", "titik (0,0)")
    )
    
    transform_matrix = get_reflection_matrix(reflection_axis)
    explanation = (
        f"**Refleksi (Pencerminan)**: Bentuk dicerminkan terhadap **{reflection_axis}**.\n\n"
        f"Contoh untuk Refleksi terhadap **sumbu-X**: $P'(x, y') = P(x, -y)$.\n\n"
        f"Matriks Transformasi:\n$$\\begin{{pmatrix}} {transform_matrix[0,0]} & {transform_matrix[0,1]} & 0 \\\\ {transform_matrix[1,0]} & {transform_matrix[1,1]} & 0 \\\\ 0 & 0 & 1 \\end{{pmatrix}}$$"
    )
    
elif transform_type == "Dilatasi":
    st.sidebar.subheader("🔍 Parameter Dilatasi")
    k = st.sidebar.slider("Faktor Skala (k)", 0.1, 5.0, 2.0)
    cx = st.sidebar.number_input("Pusat Dilatasi X (cx)", value=0)
    cy = st.sidebar.number_input("Pusat Dilatasi Y (cy)", value=0)
    
    transform_matrix = get_dilation_matrix(k, cx, cy)
    explanation = (
        f"**Dilatasi (Perkalian)**: Bentuk diperbesar/diperkecil dengan faktor skala **$k = {k}$** dari pusat **$({cx}, {cy})$**."
        f" Jika $k > 1$ (pembesaran), jika $0 < k < 1$ (pengecilan).\n\n"
        f"Matriks Skala Saja (pusat (0,0)):\n$$\\begin{{pmatrix}} {k} & 0 & 0 \\\\ 0 & {k} & 0 \\\\ 0 & 0 & 1 \\end{{pmatrix}}$$"
    )

# --- Penerapan dan Visualisasi Hasil Transformasi ---

transformed_points = apply_transform(original_points, transform_matrix)

st.header(f"Hasil {transform_type}")
plot_transformation(original_points, transformed_points, f"Transformasi: {transform_type}", explanation)

# Tampilkan Koordinat Hasil
st.subheader("📚 Detail Koordinat")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Titik Awal (P)**")
    st.dataframe(original_points[:2, :].T, columns=['X', 'Y'], height=150)
    
with col2:
    st.markdown("**Titik Hasil (P')**")
    # Tampilkan hasil pembulatan agar lebih mudah dibaca
    rounded_transformed = np.round(transformed_points[:2, :].T, 2)
    st.dataframe(rounded_transformed, columns=['X\'', 'Y\''], height=150)

# Tampilkan Matriks Transformasi yang Digunakan
st.subheader("📝 Matriks Transformasi")
st.markdown(f"Matriks **${transform_type}$** 3x3 yang digunakan:")
st.latex(f"T = {transform_matrix}")
