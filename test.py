import datetime

# Daftar produk dengan harga
DAFTAR_PRODUK = {
    "apel": 5000,
    "jeruk": 7000,
    "mangga": 10000,
    "anggur": 15000,
    "pisang": 4000
}

# Menyimpan riwayat transaksi sementara di memori
riwayat_transaksi = []

def tampilkan_menu_produk():
    """Menampilkan daftar produk dan harganya."""
    print("=" * 40)
    print(" " * 15 + "DAFTAR PRODUK")
    print("=" * 40)
    for produk, harga in DAFTAR_PRODUK.items():
        print(f"- {produk.capitalize():<15}: Rp{harga:,.0f}")
    print("=" * 40)

def proses_transaksi():
    """Memproses alur transaksi, dari input belanjaan sampai hitung kembalian."""
    keranjang_belanja = []
    
    print("\n" + "=" * 40)
    print(" " * 12 + "TRANSAKSI BARU")
    print("=" * 40)
    tampilkan_menu_produk()
    print("Ketik 'selesai' untuk menyelesaikan belanja.")
    
    while True:
        nama_produk = input("Masukkan nama produk: ").lower()
        if nama_produk == 'selesai':
            break

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
                    print(f"-> {jumlah} {nama_produk} berhasil ditambahkan.")
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Jumlah tidak valid. Harap masukkan angka.")
        else:
            print("Produk tidak tersedia.")

    if not keranjang_belanja:
        print("Transaksi dibatalkan karena keranjang kosong.")
        return

    total_belanja = sum(item['jumlah'] * item['harga_satuan'] for item in keranjang_belanja)
    
    print("\n" + "=" * 40)
    print(" " * 12 + "RINCIAN BELANJA")
    print("=" * 40)
    for item in keranjang_belanja:
        subtotal = item['jumlah'] * item['harga_satuan']
        print(f"{item['produk'].capitalize():<15}: {item['jumlah']} x Rp{item['harga_satuan']:,.0f} = Rp{subtotal:,.0f}")
    
    print("-" * 40)
    print(f"TOTAL BELANJA      : Rp{total_belanja:,.0f}")
    print("=" * 40)

    while True:
        try:
            uang_pembayaran = int(input("Masukkan uang pembayaran: Rp"))
            if uang_pembayaran >= total_belanja:
                kembalian = uang_pembayaran - total_belanja
                print(f"KEMBALIAN          : Rp{kembalian:,.0f}")
                print("=" * 40)
                
                # Simpan transaksi ke dalam riwayat
                riwayat_transaksi.append({
                    'waktu': datetime.datetime.now(),
                    'keranjang': keranjang_belanja,
                    'total': total_belanja,
                    'pembayaran': uang_pembayaran,
                    'kembalian': kembalian
                })
                
                print("🎉 Transaksi berhasil!")
                break
            else:
                print("Uang pembayaran kurang. Silakan masukkan jumlah yang cukup.")
        except ValueError:
            print("Jumlah uang tidak valid. Harap masukkan angka.")

def tampilkan_riwayat():
    """Menampilkan semua riwayat transaksi yang sudah dilakukan."""
    if not riwayat_transaksi:
        print("Belum ada riwayat transaksi.")
        return
        
    print("\n" + "=" * 40)
    print(" " * 10 + "RIWAYAT TRANSAKSI")
    print("=" * 40)

    for i, transaksi in enumerate(riwayat_transaksi):
        waktu = transaksi['waktu'].strftime("%Y-%m-%d %H:%M:%S")
        print(f"Transaksi #{i+1} ({waktu})")
        print("-" * 40)
        for item in transaksi['keranjang']:
            subtotal = item['jumlah'] * item['harga_satuan']
            print(f"- {item['produk'].capitalize():<15}: {item['jumlah']} x Rp{item['harga_satuan']:,.0f} = Rp{subtotal:,.0f}")
        
        print(f"Total Belanja      : Rp{transaksi['total']:,.0f}")
        print(f"Pembayaran         : Rp{transaksi['pembayaran']:,.0f}")
        print(f"Kembalian          : Rp{transaksi['kembalian']:,.0f}")
        print("=" * 40)

# Main loop
if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        print(" " * 12 + "SISTEM KASIR")
        print("=" * 40)
        print("1. Mulai Transaksi Baru")
        print("2. Tampilkan Riwayat Transaksi")
        print("3. Keluar")
        
        pilihan = input("Masukkan pilihan (1/2/3): ")
        
        if pilihan == '1':
            proses_transaksi()
        elif pilihan == '2':
            tampilkan_riwayat()
        elif pilihan == '3':
            print("Terima kasih sudah menggunakan kasir ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
print ("sss")