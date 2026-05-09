# Crypto Multi-Asset ETL Pipeline

Proyek ini adalah sistem **ETL (Extract, Transform, Load)** otomatis yang dirancang untuk melacak data historis kripto (Bitcoin, Ethereum, dan Solana) secara real-time menggunakan Python dan GitHub Actions.

## 📊 Fitur Utama
- **Automated Extraction**: Mengambil data pasar 60 hari terakhir dari Coingecko API.
- **Data Transformation**: Membersihkan data, mengonversi timestamp, dan menghitung indikator teknis (SMA 20) menggunakan Pandas.
- **Automated Loading**: Menyimpan hasil pengolahan ke dalam database SQLite (`market_db.sqlite`) dengan tabel terpisah untuk tiap aset.
- **Serverless Automation**: Berjalan otomatis setiap hari pada jam 00:00 UTC menggunakan GitHub Actions.

## 🛠️ Teknologi yang Digunakan
- **Bahasa**: Python 3.10
- **Library**: `Pandas`, `Requests`, `Sqlite3`
- **Automation**: GitHub Actions (CI/CD)
- **Database**: SQLite

## 🏗️ Struktur Proyek
- `etl_pipeline.py`: Skrip utama Python untuk proses ETL.
- `.github/workflows/daily_etl.yml`: Konfigurasi robot otomatisasi.
- `market_db.sqlite`: Database tempat penyimpanan data hasil olahan.
- `requirements.txt`: Daftar library yang dibutuhkan.

## ⚙️ Cara Kerja Pipeline
1. **Extract**: Skrip memanggil API Coingecko untuk mendapatkan harga harian koin.
2. **Transform**: Data mentah diubah menjadi tabel (DataFrame). Kolom `sma_20` dihitung untuk analisis tren.
3. **Load**: Data dimasukkan ke database. Jika data hari yang sama sudah ada, sistem akan melewatinya agar tidak duplikat.
4. **Push**: Robot GitHub Actions melakukan *commit* dan *push* database terbaru kembali ke repositori.

---
*Proyek ini dikembangkan oleh [Fityan Hanif] sebagai portofolio Data Engineering.*