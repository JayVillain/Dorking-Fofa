import requests
import json
import csv
import base64 # Import modul base64

# --- Konfigurasi ---
# Ganti dengan email dan kunci API Fofa kamu
FOFA_EMAIL = "@gmail.com"
FOFA_KEY = "api lssu nih "

# Nama file untuk menyimpan URL yang ditemukan
OUTPUT_FILENAME = "fofa_urls.txt"

# Dork Fofa yang sudah diatur sebelumnya
PRESET_DORK = '/wp-content/plugins/simple-file-list/ee-upload-engine.php'

# Nama file CSV (opsional, uncomment baris di bawah jika ingin menyimpan ke CSV)
# OUTPUT_CSV_FILENAME = "fofa_urls.csv"

def search_fofa(dork, page=1, page_size=100):
    """
    Melakukan pencarian di Fofa menggunakan dork tertentu.
    
    Args:
        dork (str): String dork Fofa yang akan dicari.
        page (int): Nomor halaman hasil pencarian.
        page_size (int): Jumlah hasil per halaman (maksimal 10.000 untuk Fofa API, 
                         tapi umumnya dibatasi oleh akunmu).
                         Direkomendasikan 100 untuk performa.

    Returns:
        dict: Data JSON hasil dari API Fofa, atau None jika terjadi error.
    """
    base_url = "https://fofa.info/api/v2/search/all"
    
    # Encode dork ke Base64, lalu decode kembali ke string untuk parameter URL
    # Ini adalah perbaikan dari error 'LookupError: 'base64' is not a text encoding'
    encoded_dork = base64.b64encode(dork.encode("utf-8")).decode("utf-8")
    
    params = {
        "email": FOFA_EMAIL,
        "key": FOFA_KEY,
        "qbase64": encoded_dork,
        "page": page,
        "size": page_size
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Cek jika ada error HTTP (misal: 4xx atau 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error saat melakukan permintaan ke Fofa: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Respons dari Fofa bukan JSON yang valid.")
        return None

def save_urls_to_file(urls, filename):
    """
    Menyimpan daftar URL ke dalam file teks.
    
    Args:
        urls (list): Daftar URL yang akan disimpan.
        filename (str): Nama file teks tempat URL akan disimpan.
    """
    with open(filename, "a") as f: # Mode "a" untuk append (menambahkan ke file yang sudah ada)
        for url in urls:
            f.write(url + "\n")
    print(f"{len(urls)} URL berhasil disimpan ke {filename}")

def save_urls_to_csv(urls, filename):
    """
    Menyimpan daftar URL ke dalam file CSV.
    
    Args:
        urls (list): Daftar URL yang akan disimpan.
        filename (str): Nama file CSV tempat URL akan disimpan.
    """
    with open(filename, "a", newline='') as csvfile:
        fieldnames = ['url'] # Kamu bisa menambahkan field lain jika dibutuhkan dari data Fofa
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Jika file baru dan kosong, tulis header CSV
        if csvfile.tell() == 0:
            writer.writeheader()

        for url in urls:
            writer.writerow({'url': url})
    print(f"{len(urls)} URL berhasil disimpan ke {filename}")

def main():
    """
    Fungsi utama untuk menjalankan proses auto dorking Fofa.
    """
    # Menggunakan dork yang sudah diatur (PRESET_DORK)
    dork = PRESET_DORK
    print(f"Menggunakan dork yang sudah diatur: '{dork}'")

    try:
        max_pages = int(input("Berapa halaman hasil yang ingin diambil? (misal: 5): "))
        if max_pages <= 0:
            print("Jumlah halaman harus lebih besar dari 0.")
            return
    except ValueError:
        print("Input halaman tidak valid. Masukkan angka.")
        return

    all_found_urls = []

    for page in range(1, max_pages + 1):
        print(f"Mencari dork '{dork}' di halaman {page}...")
        results = search_fofa(dork, page=page)

        if results is None:
            print("Terjadi kesalahan saat mengambil data dari Fofa. Menghentikan pencarian.")
            break
        elif results.get("error"):
            print(f"API Error dari Fofa: {results.get('errmsg')}. Menghentikan pencarian.")
            break
        elif results.get("results"):
            for item in results["results"]:
                # Asumsi item[0] adalah host/IP, item[1] adalah port, dan item[2] adalah protokol
                # Sesuaikan ini berdasarkan format respons API Fofa terbaru jika ada perubahan
                try:
                    # Pastikan item memiliki cukup elemen sebelum mengaksesnya
                    host = item[0] if len(item) > 0 else ""
                    port = item[1] if len(item) > 1 else ""
                    protocol = item[2] if len(item) > 2 else "http" # Default ke http jika tidak ada protokol

                    if not host: # Lewati jika tidak ada host
                        continue

                    if port and str(port) not in ["80", "443"]: # Jangan tampilkan port default
                        url = f"{protocol}://{host}:{port}"
                    else:
                        url = f"{protocol}://{host}"
                    all_found_urls.append(url)
                except IndexError as e:
                    print(f"Peringatan: Format data tidak sesuai di item: {item}. Error: {e}")
                    continue
                except TypeError as e:
                    print(f"Peringatan: Tipe data tidak sesuai di item: {item}. Error: {e}")
                    continue
        else:
            print("Tidak ada hasil ditemukan di halaman ini atau pencarian selesai.")
            # Ini bisa jadi indikasi akhir hasil jika total hasil < (page * page_size)
            if page == 1 and not all_found_urls:
                print("Tidak ada URL yang ditemukan sama sekali dengan dork ini.")
            break # Hentikan jika tidak ada hasil di halaman ini

    if all_found_urls:
        print(f"\nTotal {len(all_found_urls)} URL ditemukan.")
        save_urls_to_file(all_found_urls, OUTPUT_FILENAME)
        
        # Uncomment baris di bawah ini jika kamu ingin menyimpan ke CSV juga
        # save_urls_to_csv(all_found_urls, OUTPUT_CSV_FILENAME) 
    else:
        print("Tidak ada URL yang berhasil dikumpulkan.")

if __name__ == "__main__":
    main()