# app.py

import streamlit as st
import random

import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Dashboard Interaktif",
    page_icon="🚀",
    layout="wide"  # Menggunakan 'wide' agar cocok untuk aplikasi portofolio
)

# ==============================================================================
# APLIKASI 1: GAME TEBAK ANGKA
# ==============================================================================
def run_game_app():
    # CSS khusus untuk game
    st.markdown("""
        <style>
            /* Kontainer utama untuk game */
            .game-container {
                background-color: #f0f2f6;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: auto;
            }
            .status-box {
                background-color: #e8f0fe; border-left: 5px solid #005A9C; padding: 1rem;
                border-radius: 8px; margin-bottom: 1rem; text-align: center;
            }
            .status-box h3 { margin: 0; color: #31333F; }
            .status-box.success { background-color: #d4edda; border-left-color: #155724; }
            .status-box.warning { background-color: #fff3cd; border-left-color: #856404; }
            .history-box {
                padding: 1rem; background-color: #ffffff; border-radius: 8px;
                height: 200px; overflow-y: auto;
            }
            .stButton button {
                background-color: #0068c9; color: white; border-radius: 8px; border: none;
                padding: 10px 20px; width: 100%;
            }
            .stButton button:hover { background-color: #005A9C; }
        </style>
    """, unsafe_allow_html=True)
    
    # Inisialisasi state khusus game
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
    
    # Tampilan game
    st.title("🔮 Game: Tebak Angka Misterius!")
    st.image("https://www.ukri.ac.id/storage/upload/file/conten/file_1689928528lambang_foto_conten_.png", width=150)
    st.markdown("Aku sudah memilih sebuah angka rahasia antara 1 dan 100. Bisakah kamu menebaknya?")
    st.write("---")

    with st.container():
 #       st.markdown('<div class="game-container">', unsafe_allow_html=True)
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
                    if (guess - secret) <= -25:
                        st.session_state.game_message = f"Angka {guess} terlalu RENDAH! 📉"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Rendah")
                    elif -25 < (guess - secret) < 0:
                        st.session_state.game_message = f"Angka {guess} Sedikit RENDAH! 📉,\n Ayo Semangat Sedikit Lagi!"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Sedikit Rendah")
                    elif (guess - secret) >= 25:
                        st.session_state.game_message = f"Angka {guess} terlalu TINGGI! 📈"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Tinggi")
                    elif 0 < (guess - secret) < 25:
                        st.session_state.game_message = f"Angka {guess} Sedikit TINGGI! 📉,\n Ayo Semangat Sedikit Lagi!"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Sedikit Tinggi")
                    else:
                        st.session_state.game_over = True
                        st.session_state.game_message = f"🎉 BENAR! Angkanya adalah {secret}!"
                        st.session_state.game_message_class = "success"
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
#                st.markdown('<div class="history-box">', unsafe_allow_html=True)
                if not st.session_state.game_history:
                    st.write("Belum ada tebakan.")
                else:
                    for record in reversed(st.session_state.game_history):
                        st.markdown(f"- {record}")
#                st.markdown('</div>', unsafe_allow_html=True)
                st.metric(label="Total Percobaan", value=st.session_state.game_attempts)
#        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# APLIKASI 2: MANAJEMEN INVESTASI (REVISI FINAL)
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Optimisasi & Simulasi Portofolio Saham LQ45")
    st.markdown("Aplikasi ini memiliki dua langkah: **(1)** Hitung alokasi optimal dari data historis, lalu **(2)** Jalankan simulasi numerik untuk memproyeksikan kinerjanya di masa depan.")

    LQ45_TICKERS = sorted(["ACES.JK", "ADRO.JK", "AKRA.JK", "AMMN.JK", "AMRT.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "JSMR.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK"])

    @st.cache_data
    def get_stock_data(tickers, start_date, end_date):
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']
        return data.dropna(axis=1)

    def calculate_portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate):
        returns = np.sum(mean_returns * weights) * 252
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        sharpe = (returns - risk_free_rate) / volatility if volatility > 0 else 0
        return returns, volatility, sharpe

    def optimize_portfolio(num_assets, mean_returns, cov_matrix, risk_free_rate):
        args = (mean_returns, cov_matrix, risk_free_rate)
        # Objective: minimize negative Sharpe ratio
        objective_func = lambda w, m, c, rfr: -calculate_portfolio_stats(w, m, c, rfr)[2]
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0.0, 1.0) for _ in range(num_assets))
        initial_guess = np.array(num_assets * [1. / num_assets,])
        result = minimize(objective_func, initial_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x

    def run_future_simulation_gbm(data, weights, modal, T, n_simulations):
        returns = data.pct_change().dropna()
        mu, sigma = returns.mean(), returns.std()
        portfolio_values = np.zeros((T, n_simulations))
        for i in range(n_simulations):
            initial_prices = data.iloc[-1]
            simulated_prices = [initial_prices]
            for _ in range(1, T):
                Z = np.random.normal(size=len(data.columns))
                daily_returns = np.exp((mu - 0.5 * sigma**2) + sigma * Z)
                simulated_prices.append(simulated_prices[-1] * daily_returns)
            df_simulated_prices = pd.DataFrame(simulated_prices)
            portfolio_daily_value = (df_simulated_prices * (weights * modal / initial_prices)).sum(axis=1)
            portfolio_values[:, i] = portfolio_daily_value
        return portfolio_values

    # --- LANGKAH 1: INPUT OPTIMISASI (DI SIDEBAR) ---
    st.sidebar.header("Langkah 1: Hitung Portofolio Optimal")
    modal = st.sidebar.number_input("Modal Investasi (Rp)", min_value=1_000_000, step=1_000_000, value=100_000_000)
    risk_free_rate = st.sidebar.number_input("Tingkat Bebas Risiko (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.1) / 100
    selected_tickers = st.sidebar.multiselect("Pilih Saham LQ45 (minimal 2)", options=LQ45_TICKERS, default=["BBCA.JK", "BBRI.JK", "TLKM.JK", "ASII.JK", "UNTR.JK"])

    if st.sidebar.button("Hitung Portofolio Optimal!", type="primary"):
        if len(selected_tickers) < 2:
            st.sidebar.error("Mohon pilih minimal 2 saham.")
        else:
            with st.spinner("Menghitung portofolio optimal dari data historis..."):
                end_date = datetime.now()
                start_date = end_date - timedelta(days=3*365)
                data = get_stock_data(selected_tickers, start_date, end_date)
                returns = data.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                num_assets = len(data.columns)
                weights_max_sharpe = optimize_portfolio(num_assets, mean_returns, cov_matrix, risk_free_rate)
                
                # Simpan hasil ke session state untuk Langkah 2
                st.session_state.optimal_weights = weights_max_sharpe
                st.session_state.historical_data = data
                st.session_state.calculation_done = True
                st.session_state.mean_returns = mean_returns
                st.session_state.cov_matrix = cov_matrix
                st.session_state.modal = modal
                st.session_state.risk_free_rate = risk_free_rate

    # --- TAMPILKAN HASIL OPTIMISASI JIKA SUDAH DIHITUNG ---
    if st.session_state.get('calculation_done', False):
        st.header("✅ Hasil Optimisasi Portofolio (Max Sharpe Ratio)")
        exp_ret, exp_vol, exp_sharpe = calculate_portfolio_stats(st.session_state.optimal_weights, st.session_state.mean_returns, st.session_state.cov_matrix, st.session_state.risk_free_rate)
        col1, col2, col3 = st.columns(3)
        col1.metric("Estimasi Return Historis", f"{exp_ret:.2%}")
        col2.metric("Estimasi Risiko Historis", f"{exp_vol:.2%}")
        col3.metric("Sharpe Ratio Historis", f"{exp_sharpe:.2f}")
        df_alokasi = pd.DataFrame({"Saham": st.session_state.historical_data.columns, "Bobot (%)": st.session_state.optimal_weights * 100, "Alokasi Dana (Rp)": st.session_state.optimal_weights * st.session_state.modal})
        df_alokasi = df_alokasi[df_alokasi['Bobot (%)'] > 0.1].sort_values(by="Bobot (%)", ascending=False)
        st.dataframe(df_alokasi.style.format({'Bobot (%)': '{:.2f}%', 'Alokasi Dana (Rp)': 'Rp {:,.0f}'}), use_container_width=True)
        st.markdown("---")

        # --- LANGKAH 2: INPUT & JALANKAN SIMULASI (DI HALAMAN UTAMA) ---
        st.header("🔮 Langkah 2: Simulasi Kinerja Masa Depan")
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            sim_years = st.slider("Periode Simulasi (Tahun)", 1, 5, 1)
        with sim_col2:
            n_simulations = st.select_slider("Jumlah Jalur Simulasi", options=[100, 250, 500, 1000], value=250)
        
        if st.button("Jalankan Simulasi Numerik", use_container_width=True):
            with st.spinner(f"Menjalankan {n_simulations} simulasi untuk {sim_years} tahun ke depan..."):
                sim_days = sim_years * 252
                sim_results = run_future_simulation_gbm(st.session_state.historical_data, st.session_state.optimal_weights, st.session_state.modal, sim_days, n_simulations)

                # Visualisasi Jalur Simulasi
                fig_paths = go.Figure()
                for i in range(min(n_simulations, 100)):
                    fig_paths.add_trace(go.Scatter(x=np.arange(sim_days), y=sim_results[:, i], mode='lines', line=dict(width=1), showlegend=False))
                fig_paths.update_layout(title='Simulasi Jalur Nilai Portofolio di Masa Depan', xaxis_title=f'Hari Trading (ke depan)', yaxis_title='Nilai Portofolio (Rp)', template='plotly_white')
                st.plotly_chart(fig_paths, use_container_width=True)

                # Visualisasi Distribusi Hasil Akhir
                final_values = sim_results[-1, :]
                fig_dist = go.Figure(data=[go.Histogram(x=final_values, nbinsx=50, name='Distribusi')])
                fig_dist.update_layout(title='Distribusi Nilai Akhir Portofolio', xaxis_title='Nilai Akhir Portofolio (Rp)', yaxis_title='Frekuensi', template='plotly_white')
                st.plotly_chart(fig_dist, use_container_width=True)

                # Statistik Hasil Simulasi
                st.subheader("Statistik Proyeksi Kinerja")
                mean_final, median_final = np.mean(final_values), np.median(final_values)
                percentile_5, percentile_95 = np.percentile(final_values, 5), np.percentile(final_values, 95)
                
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                stat_col1.metric("Rata-rata Nilai Akhir", f"Rp {mean_final:,.0f}")
                stat_col2.metric("Nilai Akhir Paling Mungkin (Median)", f"Rp {median_final:,.0f}")
                stat_col3.metric("Rentang 90% Kemungkinan", f"Rp {percentile_5:,.0f} - Rp {percentile_95:,.0f}")

# ==============================================================================
# NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.title("Menu Utama")
app_choice = st.sidebar.radio("Pilih Aplikasi:", ("📈 Manajemen Investasi", "🔮 Game"))
st.sidebar.markdown("---")

if app_choice == "🔮 Game":
    run_game_app()
elif app_choice == "📈 Manajemen Investasi":
    run_portfolio_app()
