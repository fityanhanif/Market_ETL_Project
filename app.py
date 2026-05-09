import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

# 1. Konfigurasi Halaman (iOS Dark Mode Style)
st.set_page_config(page_title="Crypto Market Overview", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #1c1c1e; color: white; }
    h1, h2, h3 { color: white; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Market Overviews")
st.write("Real-time automated tracking via GitHub Actions.")

# 2. Fungsi Helper untuk Grafik
def create_crypto_chart(coin_name, table_name):
    conn = sqlite3.connect('market_db.sqlite')
    df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY date ASC", conn)
    conn.close()

    fig = go.Figure()

    # Garis Harga (Cyan - Entertainment Style)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['price_usd'], 
        mode='lines', name='Price',
        line=dict(color='#32ade6', width=3)
    ))

    # Garis SMA 20 (Orange - Social Style)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['sma_20'], 
        mode='lines', name='SMA 20',
        line=dict(color='#ff9500', width=3)
    ))

    fig.update_layout(
        title=f"<b>{coin_name}</b> Trend",
        plot_bgcolor='#1c1c1e',
        paper_bgcolor='#1c1c1e',
        font=dict(color='white'),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor='#3a3a3c'),
        yaxis=dict(showgrid=True, gridcolor='#3a3a3c'),
        hovermode="x unified",
        showlegend=False
    )
    return fig

# 3. Menampilkan Semua Grafik Langsung
# Kita susun secara vertikal agar grafik memanjang ke samping (enak dilihat)
st.plotly_chart(create_crypto_chart("Bitcoin (BTC)", "bitcoin_daily_metrics"), use_container_width=True)
st.plotly_chart(create_crypto_chart("Ethereum (ETH)", "ethereum_daily_metrics"), use_container_width=True)
st.plotly_chart(create_crypto_chart("Solana (SOL)", "solana_daily_metrics"), use_container_width=True)

st.info("💡 Garis biru adalah harga aset, garis oranye adalah rata-rata tren 20 hari (SMA 20).")