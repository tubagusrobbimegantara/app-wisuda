import streamlit as st
import random
import math

# Pustaka untuk Portofolio
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Dashboard Interaktif",
    page_icon="🚀",
    layout="wide"
)

# ==============================================================================
# APLIKASI 1: GAME TEBAK ANGKA (Tidak Ada Perubahan)
# ==============================================================================
def run_game_app():
    # ... (Kode game tetap sama seperti sebelumnya, tidak perlu diubah) ...
    st.markdown("""
        <style>
            .status-box { background-color: #e8f0fe; border-left: 5px solid #005A9C; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; text-align: center; }
            .status-box h3 { margin: 0; color: #31333F; }
            .status-box.success { background-color: #d4edda; border-left-color: #155724; }
            .status-box.warning { background-color: #fff3cd; border-left-color: #856404; }
        </style>
    """, unsafe_allow_html=True)
    if 'game_secret_number' not in st.session_state:
        st.session_state.game_secret_number = random.randint(1, 100)
        st.session_state.game_attempts = 0
        st.session_state.game_over = False
        st.session_state.game_message = "Ayo, mulai tebak angkanya!"
        st.session_state.game_message_class = ""
        st.session_state.game_history = []
    def reset_game():
        st.session_state.game_secret_number = random.randint(1, 100)
        st.session_state.game_attempts = 0
        st.session_state.game_over = False
        st.session_state.game_message = "Game baru dimulai! Angka rahasia sudah direset."
        st.session_state.game_message_class = ""
        st.session_state.game_history = []
    st.title("🔮 Game: Tebak Angka Misterius!")
    st.image("https://www.ukri.ac.id/storage/upload/file/conten/file_1689928528lambang_foto_conten_.png", width=150)
    st.markdown("Aku sudah memilih sebuah angka rahasia antara 1 dan 100. Bisakah kamu menebaknya?")
    st.write("---")
    with st.container():
        col1, col2 = st.columns([1.5, 2])
        with col1:
            st.subheader("Ayo Tebak!")
            if not st.session_state.game_over:
                with st.form(key="guess_form", clear_on_submit=True):
                    guess = st.number_input("Masukkan angkamu:", min_value=1, max_value=100, step=1, key="user_guess", label_visibility="collapsed")
                    submit_button = st.form_submit_button(label="Tebak Sekarang!")
                if submit_button:
                    st.session_state.game_attempts += 1
                    secret = st.session_state.game_secret_number
                    if (guess - secret) <= -5:
                        st.session_state.game_message, st.session_state.game_message_class = f"Angka {guess} terlalu RENDAH! 📉", "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Rendah")
                    elif -5 < (guess - secret) < 0:
                        st.session_state.game_message, st.session_state.game_message_class = f"Angka {guess} Sedikit RENDAH! 📉, Ayo Semangat Sedikit Lagi!", "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Sedikit Rendah")
                    elif (guess - secret) >= 5:
                        st.session_state.game_message, st.session_state.game_message_class = f"Angka {guess} terlalu TINGGI! 📈", "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Tinggi")
                    elif 0 < (guess - secret) < 5:
                        st.session_state.game_message, st.session_state.game_message_class = f"Angka {guess} Sedikit TINGGI! 📈, Ayo Semangat Sedikit Lagi!", "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Sedikit Tinggi")
                    else:
                        st.session_state.game_over = True
                        st.session_state.game_message, st.session_state.game_message_class = f"🎉 BENAR! Angkanya adalah {secret}!", "success"
                        st.session_state.game_history.append(f"{guess} ➔ TEPAT! ✅")
                        st.balloons()
            else:
                st.success("Kamu berhasil! Klik 'Mulai Baru' untuk main lagi.")
            st.write("")
            st.button("Mulai Baru 🔄", on_click=reset_game)
        with col2:
            st.subheader("Status Petunjuk")
            st.markdown(f'<div class="status-box {st.session_state.game_message_class}"><h3>{st.session_state.game_message}</h3></div>', unsafe_allow_html=True)
            st.subheader("Riwayat Tebakan")
            with st.container():
                if not st.session_state.game_history:
                    st.write("Belum ada tebakan.")
                else:
                    for record in reversed(st.session_state.game_history):
                        st.markdown(f"- {record}")
                st.metric(label="Total Percobaan", value=st.session_state.game_attempts)


# ==============================================================================
# APLIKASI 2: KALKULATOR PERSEDIAAN (EOQ) (Tidak Ada Perubahan)
# ==============================================================================
def run_eoq_app():
    # ... (Kode EOQ tetap sama seperti sebelumnya, tidak perlu diubah) ...
    def calculate_eoq(D, S, H):
        if H > 0 and D > 0:
            return math.sqrt((2 * D * S) / H)
        return 0
    st.title("📦 Kalkulator Economic Order Quantity (EOQ)")
    st.write("Aplikasi ini menghitung kuantitas pesanan optimal berdasarkan **data penjualan bulanan** dan biaya persediaan Anda.")
    st.markdown("---")
    with st.expander("🛠️ Klik di sini untuk memasukkan data dan parameter", expanded=True):
        with st.form(key='eoq_form'):
            st.markdown("##### 1. Masukkan Data Penjualan (Unit) per Bulan")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                jan = st.number_input("Januari", min_value=0, value=80, step=10)
                feb = st.number_input("Februari", min_value=0, value=85, step=10)
                mar = st.number_input("Maret", min_value=0, value=90, step=10)
            with c2:
                apr = st.number_input("April", min_value=0, value=80, step=10)
                may = st.number_input("Mei", min_value=0, value=100, step=10)
                jun = st.number_input("Juni", min_value=0, value=110, step=10)
            with c3:
                jul = st.number_input("Juli", min_value=0, value=120, step=10)
                aug = st.number_input("Agustus", min_value=0, value=100, step=10)
                sep = st.number_input("September", min_value=0, value=90, step=10)
            with c4:
                okt = st.number_input("Oktober", min_value=0, value=85, step=10)
                nov = st.number_input("November", min_value=0, value=80, step=10)
                des = st.number_input("Desember", min_value=0, value=100, step=10)
            st.markdown("---")
            st.markdown("##### 2. Masukkan Parameter Biaya dan Waktu")
            p1, p2, p3 = st.columns(3)
            with p1: S = st.number_input("Biaya Pemesanan (S)", min_value=0.0, value=50.0, step=5.0, format="%.2f", help="Biaya tetap yang dikeluarkan setiap kali melakukan pemesanan.")
            with p2: H = st.number_input("Biaya Penyimpanan/Unit (H)", min_value=0.01, value=5.0, step=0.5, format="%.2f", help="Biaya untuk menyimpan satu unit barang selama satu tahun.")
            with p3: L = st.number_input("Lead Time (hari)", min_value=1, value=7, step=1, help="Waktu yang dibutuhkan dari saat pemesanan hingga barang diterima.")
            submit_button = st.form_submit_button(label='✅ Hitung EOQ', use_container_width=True)
    if submit_button:
        D = sum([jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, des])
        if H <= 0: st.error("Biaya Penyimpanan (H) harus lebih besar dari nol.")
        elif D <= 0: st.warning("Total penjualan tahunan adalah nol. Tidak ada yang perlu dipesan.")
        else:
            eoq = calculate_eoq(D, S, H)
            num_orders = D / eoq if eoq > 0 else 0
            daily_demand = D / 365
            rop = daily_demand * L
            annual_ordering_cost = num_orders * S
            annual_holding_cost = (eoq / 2) * H
            total_inventory_cost = annual_ordering_cost + annual_holding_cost
            st.header("📊 Hasil Perhitungan")
            st.metric(label="Total Permintaan Tahunan (D) yang Dihitung", value=f"{D:,.0f} unit")
            st.success(f"**Rekomendasi:** Pesan **{eoq:,.2f} unit** setiap kali persediaan mencapai **{rop:,.2f} unit**.")
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("Economic Order Quantity (EOQ)", f"{eoq:,.2f} unit")
            col2.metric("Titik Pemesanan Kembali (ROP)", f"{rop:,.2f} unit")
            col3.metric("Total Biaya Persediaan Minimum", f"Rp {total_inventory_cost:,.2f}")


# ==============================================================================
# APLIKASI 3: ANALISIS PORTOFOLIO DENGAN BACKTESTING (KODE DIPERBAIKI)
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Analisis & Backtesting Portofolio Saham")
    st.markdown("Aplikasi ini mengoptimalkan alokasi portofolio pada data **In-Sample (2015-2023)** dan menguji kinerjanya pada data **Out-of-Sample (2024-sekarang)** dengan membandingkannya terhadap **IHSG**.")
    st.write("---")

    LQ45_TICKERS = sorted(["ACES.JK", "ADRO.JK", "AKRA.JK", "AMMN.JK", "AMRT.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "JSMR.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK"])
    BENCHMARK_TICKER = "^JKSE"

    @st.cache_data
    def get_data(tickers, start_date, end_date):
        try:
            # Selalu ambil kolom 'Close' untuk konsistensi
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
            # Jika hanya satu ticker, yfinance mengembalikan Series, ubah ke DataFrame
            if isinstance(data, pd.Series):
                data = data.to_frame(tickers)
            return data.dropna(axis=1, how='all')
        except Exception:
            return pd.DataFrame()

    def calculate_portfolio_stats(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return returns, volatility

    def run_monte_carlo(mean_returns, cov_matrix, num_portfolios):
        num_assets = len(mean_returns)
        results = np.zeros((2, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            p_return, p_vol = calculate_portfolio_stats(weights, mean_returns, cov_matrix)
            results[0, i], results[1, i] = p_return, p_vol
        return results, weights_record

    # --- Input Parameter ---
    st.subheader("⚙️ Masukkan Parameter Analisis")
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_tickers = st.multiselect("1. Pilih Saham LQ45 (minimal 2)", options=LQ45_TICKERS, default=["BBCA.JK", "TLKM.JK", "BMRI.JK", "ASII.JK"])
    with col2:
        modal = st.number_input("2. Modal Awal (Rp)", min_value=1_000_000, step=1_000_000, value=100_000_000)
    
    if st.button("🚀 Hitung & Uji Portofolio", type="primary", use_container_width=True):
        if len(selected_tickers) < 2:
            st.error("Mohon pilih minimal 2 saham.")
        else:
            # --- TAHAP 1: OPTIMISASI (IN-SAMPLE) ---
            st.header("1. Hasil Optimisasi (In-Sample: 2015-2023)")
            with st.spinner("Menjalankan optimisasi pada data 2015-2023..."):
                in_sample_data = get_data(selected_tickers, '2015-01-01', '2023-12-31')
                if in_sample_data.empty:
                    st.error("Gagal mendapatkan data In-Sample. Proses dihentikan."); return

                returns = in_sample_data.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                
                mc_results, mc_weights = run_monte_carlo(mean_returns, cov_matrix, 5000)
                sharpe_ratios = mc_results[0] / mc_results[1]
                max_sharpe_idx = np.argmax(sharpe_ratios)
                optimal_weights = np.array(mc_weights[max_sharpe_idx])
                
                df_alokasi = pd.DataFrame({"Saham": in_sample_data.columns, "Bobot": optimal_weights})
                df_alokasi = df_alokasi[df_alokasi['Bobot'] > 0.001].sort_values("Bobot", ascending=False)
                
                st.info("Alokasi portofolio optimal ditemukan berdasarkan Sharpe Ratio tertinggi dari 5,000 simulasi.")
                st.dataframe(df_alokasi.assign(Bobot=lambda x: x['Bobot'].map('{:.2%}'.format)), use_container_width=True)

            st.markdown("---")
            # --- TAHAP 2: BACKTESTING (OUT-OF-SAMPLE) ---
            st.header("2. Performa Portofolio (Out-of-Sample: 2024-Sekarang)")
            with st.spinner("Menguji portofolio dan membandingkan dengan IHSG..."):
                out_sample_start, out_sample_end = '2024-01-01', datetime.now().strftime('%Y-%m-%d')
                
                out_sample_portfolio_data = get_data(df_alokasi['Saham'].tolist(), out_sample_start, out_sample_end)
                out_sample_benchmark_data = get_data(BENCHMARK_TICKER, out_sample_start, out_sample_end)

                # ### FUNGSI DENGAN PERBAIKAN ###
                def calculate_metrics(growth_series, returns_series):
                    # Kondisi 1: Cek jika data kosong
                    if growth_series.empty or returns_series.empty:
                        return {"Nilai Akhir": "N/A", "Total Return": "N/A", "Return Tahunan": "N/A", "Risiko Tahunan": "N/A"}
                    
                    # Ekstrak nilai pertama dan terakhir
                    last_val = growth_series.iloc[-1]
                    first_val = growth_series.iloc[0]

                    # Kondisi 2: Cek jika nilai yang diekstrak adalah Series (ambil nilai pertama)
                    if isinstance(last_val, pd.Series): last_val = last_val.iloc[0]
                    if isinstance(first_val, pd.Series): first_val = first_val.iloc[0]

                    # Kondisi 3: Cek jika pembagi adalah nol
                    if first_val == 0:
                        return {"Nilai Akhir": "N/A", "Total Return": "N/A", "Return Tahunan": "N/A", "Risiko Tahunan": "N/A"}

                    total_return = (last_val / first_val) - 1
                    trading_days = len(returns_series)
                    annualized_return = (1 + total_return)
                    annualized_volatility = returns_series.std()
                    
                    return {
                        "Nilai Akhir": f"Rp {last_val:,.0f}",
                        "Total Return": f"{total_return:.2%}",
                        "Return Tahunan": f"{annualized_return:.2%}",
                        "Risiko Tahunan": f"{annualized_volatility:.2%}"
                    }

                # Hitung metrik portofolio & benchmark
                portfolio_metrics, benchmark_metrics = {}, {}
                
                if not out_sample_portfolio_data.empty:
                    portfolio_returns = out_sample_portfolio_data.pct_change().dropna()
                    weighted_returns = portfolio_returns.dot(df_alokasi.set_index('Saham').loc[portfolio_returns.columns]['Bobot'])
                    portfolio_growth = modal * (1 + weighted_returns).cumprod()
                    portfolio_metrics = calculate_metrics(portfolio_growth, weighted_returns)

                if not out_sample_benchmark_data.empty:
                    benchmark_returns = out_sample_benchmark_data.pct_change().dropna().iloc[:, 0] # Ambil kolom pertama
                    benchmark_growth = modal * (1 + benchmark_returns).cumprod()
                    benchmark_metrics = calculate_metrics(benchmark_growth, benchmark_returns)

                if not portfolio_metrics or not benchmark_metrics:
                    st.warning("Tidak cukup data Out-of-Sample untuk melakukan backtesting lengkap."); return
                
                st.subheader("📊 Perbandingan Kinerja")
                df_comparison = pd.DataFrame([portfolio_metrics, benchmark_metrics], index=["Portofolio Anda", "IHSG"]).T
                st.table(df_comparison)

                st.subheader("📈 Grafik Pertumbuhan Investasi")
                fig_growth = go.Figure()
                fig_growth.add_trace(go.Scatter(x=portfolio_growth.index, y=portfolio_growth, mode='lines', name='Portofolio Anda'))
                fig_growth.add_trace(go.Scatter(x=benchmark_growth.index, y=benchmark_growth, mode='lines', name='IHSG (Benchmark)', line={'dash': 'dash'}))
                fig_growth.update_layout(title='Perbandingan Pertumbuhan Nilai Portofolio vs. IHSG', yaxis_title='Nilai Portofolio (Rp)', template='plotly_white')
                st.plotly_chart(fig_growth, use_container_width=True)


# ==============================================================================
# NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.title("Menu Utama")
app_choice = st.sidebar.radio(
    "Pilih Aplikasi:",
    ("📈 Analisis Portofolio", "📦 Kalkulator Persediaan (EOQ)", "🔮 Game Tebak Angka")
)
st.sidebar.markdown("---")
st.sidebar.info("Dashboard ini dibuat untuk analisis interaktif.")

if app_choice == "🔮 Game Tebak Angka":
    run_game_app()
elif app_choice == "📈 Analisis Portofolio":
    run_portfolio_app()
elif app_choice == "📦 Kalkulator Persediaan (EOQ)":
    run_eoq_app()
