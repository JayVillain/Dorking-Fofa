def masukkan_data():
    """
    Fungsi untuk memasukkan data nama dan usia ke dalam file.
    """
    nama = input("Masukkan nama: ")
    usia = input("Masukkan usia: ")
    
    with open("data_penduduk.txt", "a") as file:
        file.write(f"Nama: {nama}, Usia: {usia}\n")
    
    print("Data berhasil disimpan!")

def lihat_data():
    """
    Fungsi untuk membaca dan menampilkan semua data dari file.
    """
    try:
        with open("data_penduduk.txt", "r") as file:
            data = file.readlines()
            if not data:
                print("Belum ada data yang tersimpan.")
            else:
                print("--- Daftar Data ---")
                for baris in data:
                    print(baris.strip())
                print("-------------------")
    except FileNotFoundError:
        print("Belum ada data yang tersimpan. Silakan masukkan data terlebih dahulu.")

# Loop utama untuk menampilkan menu
while True:
    print("\nMenu Pendataan:")
    print("1. Masukkan data")
    print("2. Lihat data")
    print("3. Keluar")
    
    pilihan = input("Masukkan pilihan (1/2/3): ")
    
    if pilihan == '1':
        masukkan_data()
    elif pilihan == '2':
        lihat_data()
    elif pilihan == '3':
        print("Terima kasih, sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")