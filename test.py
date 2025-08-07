import datetime

# Daftar produk dan harganya dalam bentuk dictionary
DAFTAR_PRODUK = {
    "apel": 5000,
    "jeruk": 7000,
    "mangga": 10000,
    "anggur": 15000,
    "pisang": 4000
}

def tampilkan_menu_produk():
    """Menampilkan daftar produk dan harganya."""
    print("--- Daftar Produk ---")
    for produk, harga in DAFTAR_PRODUK.items():
        print(f"- {produk.capitalize()}: Rp{harga}")
    print("---------------------")

def proses_transaksi():
    """
    Memproses alur transaksi, dari input belanjaan sampai hitung kembalian.
    """
    keranjang_belanja = []
    
    print("\nSelamat datang di Kasir Sederhana!")
    tampilkan_menu_produk()
    print("Ketik 'selesai' untuk menyelesaikan belanja.")
    
    while True:
        nama_produk = input("Masukkan nama produk: ").lower()
        if nama_produk == 'selesai':
            break  # Keluar dari loop input produk

        if nama_produk in DAFTAR_PRODUK:
            try:
                jumlah = int(input(f"Masukkan jumlah {nama_produk}: "))
                if jumlah > 0:
                    harga_satuan = DAFTAR_PRODUK[nama_produk]
                    keranjang_belanja.append({
                        'produk': nama_produk,
                        'jumlah': jumlah,
                        'harga_satuan': harga_satuan
                    })
                    print(f"{jumlah} {nama_produk} berhasil ditambahkan ke keranjang.")
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Jumlah tidak valid. Harap masukkan angka.")
        else:
            print("Produk tidak tersedia.")

    # Jika keranjang kosong, transaksi dibatalkan
    if not keranjang_belanja:
        print("Transaksi dibatalkan karena keranjang kosong.")
        return

    # Menghitung total belanja dari keranjang
    total_belanja = sum(item['jumlah'] * item['harga_satuan'] for item in keranjang_belanja)

    print("\n--- Rincian Belanja ---")
    for item in keranjang_belanja:
        subtotal = item['jumlah'] * item['harga_satuan']
        print(f"{item['produk'].capitalize()} ({item['jumlah']} x Rp{item['harga_satuan']}) = Rp{subtotal}")
    
    print(f"\nTotal Belanja: Rp{total_belanja}")

    # Proses pembayaran
    while True:
        try:
            uang_pembayaran = int(input("Masukkan uang pembayaran: Rp"))
            if uang_pembayaran >= total_belanja:
                kembalian = uang_pembayaran - total_belanja
                print(f"Kembalian: Rp{kembalian}")
                simpan_riwayat(keranjang_belanja, total_belanja, uang_pembayaran, kembalian)
                print("Transaksi selesai! Riwayat disimpan.")
                break
            else:
                print("Uang pembayaran kurang. Silakan masukkan jumlah yang cukup.")
        except ValueError:
            print("Jumlah uang tidak valid. Harap masukkan angka.")

def simpan_riwayat(keranjang, total, pembayaran, kembalian):
    """Mencatat transaksi ke dalam file teks."""
    waktu_transaksi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("riwayat_transaksi.txt", "a") as file:
        file.write("====================================\n")
        file.write(f"Waktu Transaksi: {waktu_transaksi}\n")
        file.write("--- Detail Pembelian ---\n")
        for item in keranjang:
            subtotal = item['jumlah'] * item['harga_satuan']
            file.write(f"- {item['produk'].capitalize()}: {item['jumlah']} x Rp{item['harga_satuan']} = Rp{subtotal}\n")
        file.write(f"\nTotal Belanja: Rp{total}\n")
        file.write(f"Uang Pembayaran: Rp{pembayaran}\n")
        file.write(f"Kembalian: Rp{kembalian}\n")
        file.write("====================================\n\n")

# Main loop
if __name__ == "__main__":
    while True:
        print("\n--- Sistem Kasir ---")
        print("1. Mulai Transaksi Baru")
        print("2. Keluar")
        
        pilihan = input("Masukkan pilihan (1/2): ")
        
        if pilihan == '1':
            proses_transaksi()
        elif pilihan == '2':
            print("Terima kasih sudah menggunakan kasir ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")