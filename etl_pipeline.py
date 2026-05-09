import requests
import pandas as pd
import sqlite3
from datetime import datetime

# --- 1. EXTRACT ---
def extract_market_data(coin_id="bitcoin", days="30"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    
    print(f"[EXTRACT] Menarik data untuk {coin_id}...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error Extract: {e}")
        return None

# --- 2. TRANSFORM ---
def transform_data(raw_data):
    print("[TRANSFORM] Memproses dan membersihkan data...")
    
    prices = raw_data.get('prices', [])
    df = pd.DataFrame(prices, columns=['timestamp', 'price_usd'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
    df = df[['date', 'price_usd']]
    
    # Menghitung Simple Moving Average 20 Hari (SMA20)
    df['sma_20'] = df['price_usd'].rolling(window=20).mean()
    
    df['price_usd'] = df['price_usd'].round(2)
    df['sma_20'] = df['sma_20'].round(2)
    
    return df

# --- 3. LOAD ---
def load_to_database(df, table_name="market_data"):
    print(f"[LOAD] Menyimpan data ke database tabel '{table_name}'...")
    conn = sqlite3.connect('market_db.sqlite')
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print("[SUKSES] Seluruh data berhasil dimuat ke database!")
    except Exception as e:
        print(f"Error Load: {e}")
    finally:
        conn.close()

# --- EKSEKUSI PIPELINE ---
if __name__ == "__main__":
    # 1. Menyiapkan daftar koin yang ingin ditarik
    target_coins = ["bitcoin", "ethereum", "solana"]
    
    # 2. Melakukan perulangan (looping) untuk mengeksekusi pipeline pada tiap koin
    for coin in target_coins:
        print(f"\n{'='*40}")
        print(f"Memulai Pipeline untuk Koin: {coin.upper()}")
        print(f"{'='*40}")
        
        # Ekstrak data 60 hari terakhir
        raw_data = extract_market_data(coin_id=coin, days="60")
        
        if raw_data:
            # Transformasi data
            clean_df = transform_data(raw_data)
            print(f"\nContoh Hasil Transformasi Data {coin.capitalize()}:")
            print(clean_df.tail(3)) # Menampilkan 3 data terbaru agar rapi
            
            # Load ke Database (Setiap koin akan memiliki tabelnya masing-masing)
            load_to_database(clean_df, table_name=f"{coin}_daily_metrics")
            
    print("\n[SELESAI] Seluruh koin berhasil diproses!")