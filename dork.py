import base64
import requests
import csv
import time

# === KONFIGURASI ===
# Ganti dengan kredensial FOFA kamu
email = "nanajnnaj@gmail.com"
api_key = "670ce12c348323f1448cde9e32cd9963"

# Ganti Dork sesuai CVE target
dork = 'body="/wp-content/plugins/simple-file-list" || body="simple-file-list" || header="simple-file-list"'
max_results = 1000  # total hasil yang ingin diambil
results_per_page = 100  # maksimal 100 per request

# === ENCODE DORK ===
dork_encoded = base64.b64encode(dork.encode()).decode()

# === SIAPKAN FILE OUTPUT ===
output_file = "fofa_results.csv"
csv_file = open(output_file, "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Host", "Title", "IP", "Port", "Country", "Banner"])

# === LOOP AMBIL DATA FOFA ===
print("[*] Mulai ambil data dari FOFA...")
total_fetched = 0
page = 1

while total_fetched < max_results:
    url = f"https://fofa.info/api/v1/search/all?email={email}&key={api_key}&qbase64={dork_encoded}&size={results_per_page}&page={page}"

    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"[✗] Error HTTP {res.status_code}: {res.text}")
            break

        data = res.json()
        results = data.get("results", [])

        if not results:
            print("[!] Tidak ada hasil lagi.")
            break

        for r in results:
            host = r[0]
            title = r[1]
            ip = r[2]
            port = r[3]
            country = r[4]
            banner = r[5]
            csv_writer.writerow([host, title, ip, port, country, banner])

        total_fetched += len(results)
        print(f"[✓] Fetched {total_fetched} / {max_results} hasil")
        page += 1
        time.sleep(1)  # hindari rate limit

    except Exception as e:
        print(f"[✗] Gagal: {e}")
        break

csv_file.close()
print(f"[✓] Selesai! Hasil disimpan ke '{output_file}'")
