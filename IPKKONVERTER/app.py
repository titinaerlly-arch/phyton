import streamlit as st

def sort_numbers(a, b, c):
    """Fungsi untuk mengurutkan tiga bilangan."""
    numbers = [a, b, c]
    # Menggunakan fungsi sort bawaan Python lebih sederhana dan efisien
    numbers.sort()
    return numbers

st.title("🔢 Pengurut Tiga Bilangan Sederhana")

st.write("Masukkan tiga bilangan di bawah ini:")

# Input bilangan dari pengguna menggunakan widget number_input
# st.number_input memungkinkan pengguna memasukkan angka
a = st.number_input("Masukkan bilangan pertama (a):", value=0, step=1)
b = st.number_input("Masukkan bilangan kedua (b):", value=0, step=1)
c = st.number_input("Masukkan bilangan ketiga (c):", value=0, step=1)

# Tombol untuk menjalankan pengurutan
if st.button("Urutkan!"):
    # Memastikan semua input telah diberikan (meskipun number_input selalu memiliki nilai)
    if a is not None and b is not None and c is not None:
        # Panggil fungsi pengurutan
        sorted_list = sort_numbers(a, b, c)

        # Tampilkan hasil
        st.success(f"Urutan bilangan dari yang paling kecil adalah: {sorted_list[0]}, {sorted_list[1]}, {sorted_list[2]}")
    else:
        st.error("Pastikan Anda memasukkan ketiga bilangan.")
