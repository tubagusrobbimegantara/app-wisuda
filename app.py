import streamlit as st
import random
import math
from io import BytesIO

# Pustaka untuk Portofolio, Fraktal, & Harvesting
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Arena Game & Analisis",
    page_icon="🎮",
    layout="wide"
)

# ==============================================================================
# APLIKASI UTAMA: GAME TEBAK ANGKA
# ==============================================================================
def run_game_app():
    # --- CSS Kustom untuk Tampilan Game Modern ---
    st.markdown("""
        <style>
            .main > div { padding-top: 2rem; }
            .block-container { padding-top: 2rem; }
            .game-container {
                background: linear-gradient(145deg, #2b2b2b, #1e1e1e);
                padding: 2rem; border-radius: 20px;
                box-shadow: 10px 10px 20px #1c1c1c, -10px -10px 20px #2e2e2e;
                color: #e0e0e0;
            }
            .st-emotion-cache-10trblm { color: #e0e0e0; font-family: 'Consolas', 'Courier New', monospace; }
            .stNumberInput input {
                background-color: #333; color: #fff; border: 2px solid #555;
                border-radius: 10px; text-align: center; font-size: 2rem; font-weight: bold;
            }
            .stButton>button {
                background: linear-gradient(145deg, #00d4ff, #009de0); color: white; font-weight: bold;
                border: none; border-radius: 12px; padding: 12px 24px; width: 100%;
                box-shadow: 5px 5px 10px #1c1c1c, -5px -5px 10px #2e2e2e;
                transition: all 0.2s ease-in-out;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                box-shadow: 7px 7px 15px #1c1c1c, -7px -7px 15px #2e2e2e;
            }
            .score-box {
                background-color: #252525; text-align: center; padding: 1rem;
                border-radius: 15px; border: 1px solid #444;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.high_score = st.session_state.get('high_score', 999)
        st.session_state.game_over = False
        st.session_state.message = "Mulai permainan dengan menebak angka!"
    def restart_game():
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.message = "Game baru dimulai! Angka rahasia telah direset."

    st.title("🎮 Arena Tebak Angka 🔮")
    st.markdown("Uji intuisimu! Aku telah memilih angka rahasia antara **1 dan 100**. Bisakah kamu menebaknya dengan percobaan sesedikit mungkin?")
    st.write("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        message_placeholder = st.empty()
        if st.session_state.game_over:
            message_placeholder.success(st.session_state.message)
            st.balloons()
            if st.button("Main Lagi? 🔄"):
                restart_game()
                st.rerun()
        else:
            message_placeholder.info(f"**Petunjuk:** {st.session_state.message}")
            with st.form(key="guess_form"):
                guess = st.number_input("Masukkan tebakanmu di sini:", min_value=1, max_value=100, step=1, label_visibility="collapsed")
                submit = st.form_submit_button(label="🔑 Tebak!")
            if submit:
                st.session_state.attempts += 1
                secret = st.session_state.secret_number
                if guess < secret:
                    st.session_state.message = f"Angka {guess} **terlalu RENDAH**! 📉 Coba angka yang lebih besar."
                elif guess > secret:
                    st.session_state.message = f"Angka {guess} **terlalu TINGGI**! 📈 Coba angka yang lebih kecil."
                else:
                    st.session_state.game_over = True
                    st.session_state.message = f"🎉 Selamat! Kamu berhasil menebak angka **{secret}**!"
                    if st.session_state.attempts < st.session_state.high_score:
                        st.session_state.high_score = st.session_state.attempts
                        st.session_state.message += " Kamu mencetak **REKOR BARU**!"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("📊 Papan Skor")
        with st.container(border=True):
            st.markdown('<div class="score-box">', unsafe_allow_html=True)
            st.metric(label="Percobaan Saat Ini", value=f"{st.session_state.attempts} 🎯")
            st.markdown('</div><br>', unsafe_allow_html=True)
            st.markdown('<div class="score-box">', unsafe_allow_html=True)
            st.metric(label="Skor Terbaik (Percobaan Terendah)", value=f"{st.session_state.high_score} 🏆")
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# APLIKASI 1: ANALISIS PORTOFOLIO
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
            if isinstance(data, pd.Series): data = data.to_frame(name=tickers)
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
                    if isinstance(annualized_volatility, pd.Series): annualized_volatility = annualized_volatility.iloc[0]
                    return {"Nilai Akhir": f"Rp {last_val:,.0f}", "Total Return": f"{total_return:.2%}", "Return Tahunan": f"{annualized_return:.2%}", "Risiko Tahunan": f"{annualized_volatility:.2%}"}
                out_sample_start, out_sample_end = '2024-01-01', datetime.now().strftime('%Y-%m-%d')
                out_sample_portfolio_data = get_data(df_alokasi['Saham'].tolist(), out_sample_start, out_sample_end)
                out_sample_benchmark_data = get_data(BENCHMARK_TICKER, out_sample_start, out_sample_end)
                portfolio_metrics, benchmark_metrics = {}, {}
                if not out_sample_portfolio_data.empty:
                    portfolio_returns = out_sample_portfolio_data.pct_change().dropna()
                    valid_weights = df_alokasi.set_index('Saham').loc[portfolio_returns.columns]
                    weighted_returns = portfolio_returns.dot(valid_weights['Bobot'])
                    portfolio_growth = modal * (1 + weighted_returns).cumprod()
                    portfolio_metrics = calculate_metrics(portfolio_growth, weighted_returns)
                if not out_sample_benchmark_data.empty:
                    benchmark_returns = out_sample_benchmark_data.pct_change().dropna().iloc[:, 0]
                    benchmark_growth = modal * (1 + benchmark_returns).cumprod()
                    benchmark_metrics = calculate_metrics(benchmark_growth, benchmark_returns)
                if not portfolio_metrics or not benchmark_metrics: st.warning("Tidak cukup data Out-of-Sample untuk backtesting."); return
                st.subheader("📊 Perbandingan Kinerja"); st.table(pd.DataFrame([portfolio_metrics, benchmark_metrics], index=["Portofolio Anda", "IHSG"]).T)
                st.subheader("📈 Grafik Pertumbuhan Investasi")
                fig = go.Figure()
                if 'portfolio_growth' in locals(): fig.add_trace(go.Scatter(x=portfolio_growth.index, y=portfolio_growth, mode='lines', name='Portofolio Anda'))
                if 'benchmark_growth' in locals(): fig.add_trace(go.Scatter(x=benchmark_growth.index, y=benchmark_growth, mode='lines', name='IHSG (Benchmark)', line={'dash': 'dash'}))
                fig.update_layout(title='Perbandingan Pertumbuhan Nilai Portofolio vs. IHSG', yaxis_title='Nilai Portofolio (Rp)', template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# APLIKASI 2: PANEN BERKELANJUTAN
# ==============================================================================
def run_harvesting_app():
    st.title("🐄 Simulasi Panen Ternak Berkelanjutan")
    st.markdown("Aplikasi ini mensimulasikan dampak panen tahunan terhadap populasi ternak. Gunakan model ini untuk menentukan apakah tingkat panen Anda berkelanjutan atau akan menyebabkan kepunahan.")
    st.write("---")
    col1, col2 = st.columns([2, 1])
    with col2:
        st.subheader("⚙️ Atur Parameter")
        p0 = st.slider("Populasi Awal (Ekor)", 10, 1000, 50, 10)
        K = st.slider("Daya Tampung Lahan (K)", 100, 2000, 1000, 50, help="Jumlah maksimum ternak yang dapat didukung oleh lahan.")
        r = st.slider("Laju Pertumbuhan (r)", 0.05, 1.0, 0.2, 0.05, format="%.2f", help="Laju pertumbuhan alami populasi per tahun.")
        H = st.slider("Jumlah Panen per Tahun (H)", 0, 200, 40, 5, help="Jumlah ternak yang diambil/dipanen setiap tahun.")
    years = 50
    population = [p0]
    for _ in range(1, years):
        last_pop = population[-1]
        growth = r * last_pop * (1 - last_pop / K)
        next_pop = last_pop + growth - H
        population.append(max(0, next_pop))
    df_pop = pd.DataFrame({'Tahun': range(years), 'Populasi': population})
    msy = (r * K) / 4
    with col1:
        st.header("📈 Hasil Simulasi Populasi")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_pop['Tahun'], y=df_pop['Populasi'], mode='lines+markers', name='Populasi Ternak'))
        fig.update_layout(xaxis_title="Tahun", yaxis_title="Jumlah Ekor")
        st.plotly_chart(fig, use_container_width=True)
        final_population = population[-1]
        st.header("🎯 Status & Rekomendasi")
        if final_population <= 1:
            st.error(f"**Status: Tidak Berkelanjutan.** Dengan tingkat panen {H} ekor per tahun, populasi ternak akan habis.")
        elif H > msy:
            st.warning(f"**Status: Berisiko.** Tingkat panen Anda ({H} ekor/tahun) melebihi batas lestari maksimum. Populasi akan menurun dalam jangka panjang dan rentan punah.")
            st.info(f"💡 **Rekomendasi panen optimal** (MSY) untuk parameter ini adalah **{msy:,.0f} ekor/tahun**. Ini adalah jumlah panen terbanyak yang bisa dilakukan setiap tahun agar populasi tetap lestari dalam jangka panjang.")
        else:
            st.success(f"**Status: Berkelanjutan.** Tingkat panen Anda ({H} ekor/tahun) berada pada level yang aman dan populasi dapat bertahan atau bertumbuh.")
        
# ==============================================================================
# APLIKASI 3: GEOMETRI FRAKTAL
# ==============================================================================
def run_fractal_app():
    st.title("🎨 Visualisasi Fraktal Eye-Catching")
    st.markdown("Jelajahi keindahan matematika fraktal dengan visualisasi warna yang cerah dan memukau. Pilih jenis fraktal untuk melihat pola unik yang dihasilkan.")
    col1, col2 = st.columns(2)
    with col1:
        fractal_type = st.selectbox("Pilih Jenis Fraktal", ("Segitiga Sierpinski", "Kapal Terbakar", "Mandelbrot Klasik"))
    with col2:
        if fractal_type == "Segitiga Sierpinski":
            iterations = st.slider("Jumlah Titik (Detail)", 1, 10, 6, 1, help="Semakin tinggi, semakin detail dan padat segitiga.")
        else:
            iterations = st.slider("Jumlah Iterasi (Detail)", 20, 300, 75, 10, help="Semakin tinggi, semakin detail polanya.")
    @st.cache_data
    def generate_fractal(width, height, max_iter, type):
        if type == "Segitiga Sierpinski":
            points = np.array([[width/2, 0], [0, height-1], [width-1, height-1]])
            p = np.array([random.uniform(0, width), random.uniform(0, height)])
            image_data = np.zeros((height, width))
            for _ in range(max_iter * 50000):
                target_vertex = random.choice(points)
                p = (p + target_vertex) / 2
                x_coord, y_coord = int(p[0]), int(p[1])
                if 0 <= x_coord < width and 0 <= y_coord < height:
                    image_data[y_coord, x_coord] = 1
            return image_data
        else:
            x, y = np.linspace(-2, 2, width), np.linspace(-2, 2, height)
            c = x[:, np.newaxis] + 1j * y[np.newaxis, :]; z = np.zeros_like(c, dtype=complex)
            output = np.zeros(c.shape)
            for it in range(max_iter):
                not_diverged = np.abs(z) < 10
                output[not_diverged] = it
                if type == "Mandelbrot Klasik":
                    z[not_diverged] = z[not_diverged]**2 + c[not_diverged]
                elif type == "Kapal Terbakar":
                    z_abs = np.abs(z[not_diverged].real) + 1j * np.abs(z[not_diverged].imag)
                    z[not_diverged] = z_abs**2 + c[not_diverged]
            return output
    with st.spinner(f"Menciptakan '{fractal_type}' dengan {iterations} iterasi..."):
        img_width, img_height = 800, 800 
        fractal_data = generate_fractal(img_width, img_height, iterations, fractal_type)
        selected_colorscale = 'Plasma'
        fig = go.Figure(data=go.Heatmap(z=fractal_data, colorscale=selected_colorscale, showscale=False))
        fig.update_layout(title=f"Fraktal: {fractal_type}", xaxis_visible=False, yaxis_visible=False, height=600, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.title("🎮 Menu Utama")
app_choice = st.sidebar.radio(
    "Pilih Aplikasi:",
    ("🔮 Arena Tebak Angka",
     "📈 Analisis Portofolio", 
     "🐄 Panen Berkelanjutan",
     "🎨 Geometri Fraktal")
)
st.sidebar.markdown("---")
st.sidebar.image("https://www.ukri.ac.id/storage/upload/file/conten/file_1689928528lambang_foto_conten_.png", width=100)
st.sidebar.info("Dashboard Analisis & Game.")

if app_choice == "🔮 Arena Tebak Angka":
    run_game_app()
elif app_choice == "📈 Analisis Portofolio":
    run_portfolio_app()
elif app_choice == "🐄 Panen Berkelanjutan":
    run_harvesting_app()
elif app_choice == "🎨 Geometri Fraktal":
    run_fractal_app()
