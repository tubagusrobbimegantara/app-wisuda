import streamlit as st
import random
import math
from io import BytesIO

# Pustaka untuk Portofolio, EOQ, Fraktal, & Harvesting
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

# --- Helper Function untuk Download Excel ---
@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Penjualan')
    processed_data = output.getvalue()
    return processed_data

# ==============================================================================
# APLIKASI 1: ANALISIS PORTOFOLIO (Tidak Ada Perubahan)
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
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
            if isinstance(data, pd.Series): data = data.to_frame(tickers)
            return data.dropna(axis=1, how='all')
        except Exception: return pd.DataFrame()
    def run_monte_carlo(mean_returns, cov_matrix, num_portfolios):
        num_assets = len(mean_returns)
        results = np.zeros((2, num_portfolios)); weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(num_assets); weights /= np.sum(weights)
            weights_record.append(weights)
            p_return, p_vol = np.sum(mean_returns * weights) * 252, np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
            results[0, i], results[1, i] = p_return, p_vol
        return results, weights_record
    st.subheader("⚙️ Masukkan Parameter Analisis")
    col1, col2 = st.columns([3, 1])
    with col1: selected_tickers = st.multiselect("1. Pilih Saham LQ45 (minimal 2)", options=LQ45_TICKERS, default=["BBCA.JK", "TLKM.JK", "BMRI.JK", "ASII.JK"])
    with col2: modal = st.number_input("2. Modal Awal (Rp)", min_value=1_000_000, step=1_000_000, value=100_000_000)
    if st.button("🚀 Hitung & Uji Portofolio", type="primary", use_container_width=True):
        if len(selected_tickers) < 2: st.error("Mohon pilih minimal 2 saham.")
        else:
            st.header("1. Hasil Optimisasi (In-Sample: 2015-2023)");
            with st.spinner("Menjalankan optimisasi..."):
                in_sample_data = get_data(selected_tickers, '2015-01-01', '2023-12-31')
                if in_sample_data.empty: st.error("Gagal mendapatkan data In-Sample."); return
                returns = in_sample_data.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                mc_results, mc_weights = run_monte_carlo(mean_returns, cov_matrix, 5000)
                sharpe_ratios = mc_results[0] / mc_results[1]
                optimal_weights = np.array(mc_weights[np.argmax(sharpe_ratios)])
                df_alokasi = pd.DataFrame({"Saham": in_sample_data.columns, "Bobot": optimal_weights}).query("Bobot > 0.001").sort_values("Bobot", ascending=False)
                st.info("Alokasi portofolio optimal ditemukan berdasarkan Sharpe Ratio tertinggi.")
                st.dataframe(df_alokasi.assign(Bobot=lambda x: x['Bobot'].map('{:.2%}'.format)), use_container_width=True)
            st.markdown("---")
            st.header("2. Performa Portofolio (Out-of-Sample: 2024-Sekarang)")
            with st.spinner("Menguji portofolio dan membandingkan dengan IHSG..."):
                def calculate_metrics(growth_series, returns_series):
                    if growth_series.empty or returns_series.empty: return {}
                    last_val, first_val = growth_series.iloc[-1], growth_series.iloc[0]
                    if isinstance(last_val, pd.Series): last_val = last_val.iloc[0]
                    if isinstance(first_val, pd.Series): first_val = first_val.iloc[0]
                    if first_val == 0: return {}
                    total_return = (last_val / first_val) - 1
                    trading_days = len(returns_series)
                    annualized_return = (1 + total_return)**(252/trading_days) - 1 if trading_days > 0 else 0
                    annualized_volatility = returns_series.std() * np.sqrt(252)
                    return {"Nilai Akhir": f"Rp {last_val:,.0f}", "Total Return": f"{total_return:.2%}", "Return Tahunan": f"{annualized_return:.2%}", "Risiko Tahunan": f"{annualized_volatility:.2%}"}
                out_sample_start, out_sample_end = '2024-01-01', datetime.now().strftime('%Y-%m-%d')
                out_sample_portfolio_data = get_data(df_alokasi['Saham'].tolist(), out_sample_start, out_sample_end)
                out_sample_benchmark_data = get_data(BENCHMARK_TICKER, out_sample_start, out_sample_end)
                portfolio_metrics, benchmark_metrics = {}, {}
                if not out_sample_portfolio_data.empty:
                    portfolio_returns = out_sample_portfolio_data.pct_change().dropna()
                    weighted_returns = portfolio_returns.dot(df_alokasi.set_index('Saham').loc[portfolio_returns.columns]['Bobot'])
                    portfolio_growth = modal * (1 + weighted_returns).cumprod()
                    portfolio_metrics = calculate_metrics(portfolio_growth, weighted_returns)
                if not out_sample_benchmark_data.empty:
                    benchmark_returns = out_sample_benchmark_data.pct_change().dropna()
                    # Handle jika benchmark hanya punya 1 kolom (Series) atau lebih (DataFrame)
                    if isinstance(benchmark_returns, pd.Series):
                        benchmark_growth = modal * (1 + benchmark_returns).cumprod()
                    else:
                        benchmark_growth = modal * (1 + benchmark_returns.iloc[:, 0]).cumprod()
                    benchmark_metrics = calculate_metrics(benchmark_growth, benchmark_returns)
                if not portfolio_metrics or not benchmark_metrics: st.warning("Tidak cukup data Out-of-Sample untuk backtesting."); return
                st.subheader("📊 Perbandingan Kinerja"); st.table(pd.DataFrame([portfolio_metrics, benchmark_metrics], index=["Portofolio Anda", "IHSG"]).T)
                st.subheader("📈 Grafik Pertumbuhan Investasi")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=portfolio_growth.index, y=portfolio_growth, mode='lines', name='Portofolio Anda'))
                fig.add_trace(go.Scatter(x=benchmark_growth.index, y=benchmark_growth, mode='lines', name='IHSG (Benchmark)', line={'dash': 'dash'}))
                fig.update_layout(title='Perbandingan Pertumbuhan Nilai Portofolio vs. IHSG', yaxis_title='Nilai Portofolio (Rp)', template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# APLIKASI 2: KALKULATOR PERSEDIAAN (EOQ) (Tidak Ada Perubahan)
# ==============================================================================
def run_eoq_app():
    st.title("📦 Kalkulator Keputusan Persediaan (EOQ)")
    st.markdown("Unggah data penjualan bulanan Anda dalam format Excel atau CSV untuk mendapatkan rekomendasi pemesanan barang yang optimal.")
    st.write("---")
    with st.expander("Lihat Petunjuk Format & Unduh Template"):
        st.info("Pastikan file Anda memiliki satu kolom dengan nama header `Penjualan` yang berisi data penjualan unit per periode (misal, per bulan).")
        sample_df = pd.DataFrame({'Penjualan': [100, 110, 120, 105, 115, 130, 140, 125, 110, 100, 105, 120]})
        st.dataframe(sample_df, use_container_width=True)
        st.download_button(label="Unduh Template Excel (.xlsx)", data=to_excel(sample_df), file_name='template_penjualan_eoq.xlsx', mime='application/vnd.ms-excel')
    st.subheader("⚙️ Masukkan Parameter & Data")
    c1, c2, c3, c4 = st.columns(4)
    with c1: uploaded_file = st.file_uploader("1. Unggah File Penjualan", type=['csv', 'xlsx'], label_visibility="collapsed")
    with c2: S = st.number_input("Biaya Pesan (S)", 0.0, value=50000.0, step=1000.0, format="%.0f", help="Biaya tetap setiap kali memesan barang.")
    with c3: H = st.number_input("Biaya Simpan/Unit (H)", 0.01, value=5000.0, step=100.0, format="%.0f", help="Biaya menyimpan satu unit barang selama setahun.")
    with c4: L = st.number_input("Lead Time (Hari)", 1, value=7, step=1, help="Waktu tunggu dari pemesanan hingga barang tiba.")
    if st.button("💡 Buat Rekomendasi Keputusan", type="primary", use_container_width=True):
        if uploaded_file is None: st.warning("Mohon unggah file data penjualan."); return
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            if 'Penjualan' not in df.columns: st.error("Format Salah: File tidak memiliki kolom 'Penjualan'."); return
            D = df['Penjualan'].sum()
            if D <= 0: st.info("Total penjualan nol. Tidak perlu memesan."); return
            eoq = math.sqrt((2 * D * S) / H)
            rop = (D / 365) * L
            st.header("🎯 Keputusan Optimal Anda")
            st.success(f"**Lakukan pemesanan sebanyak {eoq:,.0f} unit setiap kali sisa persediaan di gudang mencapai {rop:,.0f} unit.**")
            with st.expander("Lihat Detail Hasil Perhitungan"):
                m1, m2, m3 = st.columns(3); m1.metric("Total Permintaan Tahunan (D)", f"{D:,.0f} unit"); m2.metric("Kuantitas Pesan Optimal (EOQ)", f"{eoq:,.0f} unit"); m3.metric("Titik Pemesanan Kembali (ROP)", f"{rop:,.0f} unit")
        except Exception as e: st.error(f"Terjadi error saat memproses file: {e}")

# ==============================================================================
# APLIKASI 3: GAME TEBAK ANGKA (Tidak Ada Perubahan)
# ==============================================================================
def run_game_app():
    st.title("🔮 Game: Tebak Angka Misterius!")
    if 'game_secret_number' not in st.session_state:
        st.session_state.game_secret_number = random.randint(1, 100)
        st.session_state.game_attempts = 0
        st.session_state.game_history = []
    st.markdown("Saya telah memilih angka rahasia antara 1 dan 100. Coba tebak!")
    with st.form(key="game_form", clear_on_submit=True):
        guess = st.number_input("Masukkan tebakan Anda:", 1, 100, step=1, key="guess")
        submit_button = st.form_submit_button(label="Tebak")
    if submit_button:
        st.session_state.game_attempts += 1
        secret = st.session_state.game_secret_number
        if guess < secret:
            st.warning("Terlalu rendah!")
            st.session_state.game_history.append(f"{guess} (Rendah)")
        elif guess > secret:
            st.warning("Terlalu tinggi!")
            st.session_state.game_history.append(f"{guess} (Tinggi)")
        else:
            st.success(f"Benar! Angkanya {secret}. Ditebak dalam {st.session_state.game_attempts} percobaan.")
            st.balloons()
            # Reset game
            st.session_state.game_secret_number = random.randint(1, 100)
            st.session_state.game_attempts = 0
            st.session_state.game_history = []
    if st.session_state.get('game_history'):
        st.write("Riwayat Tebakan:", ", ".join(st.session_state.game_history))

# ==============================================================================
# APLIKASI 4: GEOMETRI FRAKTAL (Tidak Ada Perubahan)
# ==============================================================================
def run_fractal_app():
    st.title("🌌 Visualisasi Geometri Fraktal: Mandelbrot Set")
    st.markdown("Fraktal adalah pola geometris kompleks yang berulang pada setiap skala. Mandelbrot set adalah contoh paling terkenal, diciptakan dari persamaan sederhana $Z_{n+1} = Z_n^2 + C$.")
    st.subheader("⚙️ Atur Parameter Visualisasi")
    iterations = st.slider("Jumlah Iterasi (Detail)", 10, 200, 50, 10, help="Semakin tinggi, semakin detail gambar fraktal, namun waktu proses lebih lama.")
    @st.cache_data
    def generate_mandelbrot(width, height, max_iter):
        x, y = np.linspace(-2, 1, width), np.linspace(-1.5, 1.5, height)
        c = x[:, np.newaxis] + 1j * y[np.newaxis, :]; z = np.zeros_like(c, dtype=complex)
        output = np.zeros(c.shape)
        for it in range(max_iter):
            not_diverged = np.abs(z) < 2; output[not_diverged] = it
            z[not_diverged] = z[not_diverged]**2 + c[not_diverged]
        return output
    with st.spinner(f"Menghasilkan fraktal dengan {iterations} iterasi..."):
        mandelbrot_data = generate_mandelbrot(800, 800, iterations)
        fig = go.Figure(data=go.Heatmap(z=mandelbrot_data, colorscale='viridis', showscale=False))
        fig.update_layout(title="Mandelbrot Set", xaxis_visible=False, yaxis_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# APLIKASI 5: PANEN BERKELANJUTAN (KODE DIPERBAIKI)
# ==============================================================================
def run_harvesting_app():
    st.title("🐄 Simulasi Panen Ternak Berkelanjutan")
    st.markdown("Aplikasi ini mensimulasikan dampak panen tahunan terhadap populasi ternak. Gunakan model ini untuk menentukan apakah tingkat panen Anda berkelanjutan atau akan menyebabkan kepunahan.")
    st.write("---")

    col1, col2 = st.columns([2, 1])

    with col2:
        st.subheader("⚙️ Atur Parameter")
        p0 = st.slider("Populasi Awal (Ekor)", min_value=10, max_value=1000, value=50, step=10)
        K = st.slider("Daya Tampung Lahan (K)", min_value=100, max_value=2000, value=1000, step=50, help="Jumlah maksimum ternak yang dapat didukung oleh lahan.")
        r = st.slider("Laju Pertumbuhan (r)", min_value=0.05, max_value=1.0, value=0.2, step=0.05, format="%.2f", help="Laju pertumbuhan alami populasi per tahun.")
        H = st.slider("Jumlah Panen per Tahun (H)", min_value=0, max_value=200, value=40, step=5, help="Jumlah ternak yang diambil/dipanen setiap tahun.")
    
    # --- SIMULASI ---
    years = 50
    population = [p0]
    for _ in range(1, years):
        # Perhitungan populasi tahun berikutnya
        last_pop = population[-1]
        growth = r * last_pop * (1 - last_pop / K)
        next_pop = last_pop + growth - H
        population.append(max(0, next_pop)) # Pastikan populasi tidak negatif
    
    df_pop = pd.DataFrame({'Tahun': range(years), 'Populasi': population})
    
    # --- HITUNG REKOMENDASI SETELAH SLIDER DIBACA ---
    msy = (r * K) / 4

    with col1:
        st.header("📈 Hasil Simulasi Populasi")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_pop['Tahun'], y=df_pop['Populasi'], mode='lines+markers', name='Populasi Ternak'))
        fig.update_layout(xaxis_title="Tahun", yaxis_title="Jumlah Ekor")
        st.plotly_chart(fig, use_container_width=True)

        final_population = population[-1]

        st.header("🎯 Status & Rekomendasi")
        
        # Analisis Status
        if final_population <= 1: # Dianggap punah jika sisa 1 atau kurang
            st.error(f"**Status: Tidak Berkelanjutan.** Dengan tingkat panen {H} ekor per tahun, populasi ternak akan habis.")
        elif H > msy:
            st.warning(f"**Status: Berisiko.** Tingkat panen Anda ({H} ekor/tahun) melebihi batas lestari maksimum. Populasi akan menurun dalam jangka panjang dan rentan punah.")
        else:
            st.success(f"**Status: Berkelanjutan.** Tingkat panen Anda ({H} ekor/tahun) berada pada level yang aman dan populasi dapat bertahan atau bertumbuh.")

        # Rekomendasi Optimal
        st.info(f"💡 **Rekomendasi panen optimal** (MSY) untuk parameter ini adalah **{msy:,.0f} ekor/tahun**. Ini adalah jumlah panen terbanyak yang bisa dilakukan setiap tahun agar populasi tetap lestari dalam jangka panjang.")


# ==============================================================================
# NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.title("Menu Utama")
app_choice = st.sidebar.radio(
    "Pilih Aplikasi:",
    ("📦 Kalkulator Persediaan (EOQ)", 
     "📈 Analisis Portofolio", 
     "🐄 Panen Berkelanjutan",
     "🌌 Geometri Fraktal",
     "🔮 Game Tebak Angka")
)
st.sidebar.markdown("---")
st.sidebar.image("https://www.ukri.ac.id/storage/upload/file/conten/file_1689928528lambang_foto_conten_.png", width=100)
st.sidebar.info("Dashboard Analisis Interaktif.")

if app_choice == "📈 Analisis Portofolio":
    run_portfolio_app()
elif app_choice == "📦 Kalkulator Persediaan (EOQ)":
    run_eoq_app()
elif app_choice == "🐄 Panen Berkelanjutan":
    run_harvesting_app()
elif app_choice == "🌌 Geometri Fraktal":
    run_fractal_app()
elif app_choice == "🔮 Game Tebak Angka":
    run_game_app()
