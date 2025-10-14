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
# APLIKASI 2: MANAJEMEN INVESTASI (REVISI TOTAL)
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Simulasi Optimisasi Portofolio Markowitz")
    st.markdown("Aplikasi ini melakukan simulasi ribuan portofolio untuk memvisualisasikan **Efficient Frontier** dan menemukan alokasi optimal berdasarkan saham-saham pilihan Anda dari indeks LQ45.")

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

    def run_monte_carlo_simulation(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
        num_assets = len(mean_returns)
        results = np.zeros((3, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolio_return, portfolio_volatility, portfolio_sharpe = calculate_portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate)
            results[0, i] = portfolio_return
            results[1, i] = portfolio_volatility
            results[2, i] = portfolio_sharpe
        return results, weights_record

    def optimize_portfolio(num_assets, mean_returns, cov_matrix, risk_free_rate, objective_func):
        args = (mean_returns, cov_matrix, risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0.0, 1.0) for _ in range(num_assets))
        initial_guess = np.array(num_assets * [1. / num_assets,])
        result = minimize(objective_func, initial_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x

    st.sidebar.header("⚙️ Parameter Simulasi")
    modal = st.sidebar.number_input("1. Modal Investasi (Rp)", min_value=1_000_000, step=1_000_000, value=100_000_000)
    risk_free_rate = st.sidebar.number_input("2. Tingkat Bebas Risiko (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.1, help="Gunakan acuan BI Rate atau imbal hasil obligasi pemerintah.") / 100
    selected_tickers = st.sidebar.multiselect("3. Pilih Saham LQ45 (minimal 2)", options=LQ45_TICKERS, default=["BBCA.JK", "BBRI.JK", "TLKM.JK", "ASII.JK", "UNTR.JK"])
    num_simulations = st.sidebar.select_slider("4. Jumlah Simulasi Portofolio", options=[1000, 5000, 10000, 20000], value=10000)

    if st.sidebar.button("🚀 Jalankan Simulasi & Optimisasi!", type="primary"):
        if len(selected_tickers) < 2:
            st.sidebar.error("Mohon pilih minimal 2 saham.")
        else:
            with st.spinner("Mengambil data dan menjalankan ribuan simulasi... Ini mungkin butuh waktu sejenak."):
                end_date = datetime.now()
                start_date = end_date - timedelta(days=3*365)
                
                data = get_stock_data(selected_tickers, start_date, end_date)
                returns = data.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                num_assets = len(data.columns)

                # Jalankan simulasi Monte Carlo
                mc_results, _ = run_monte_carlo_simulation(num_simulations, mean_returns, cov_matrix, risk_free_rate)
                
                # Cari portofolio dengan Sharpe Ratio maksimal dari hasil simulasi
                max_sharpe_idx = np.argmax(mc_results[2])
                max_sharpe_ret, max_sharpe_vol = mc_results[0, max_sharpe_idx], mc_results[1, max_sharpe_idx]
                
                # Cari portofolio dengan Volatilitas minimum dari hasil simulasi
                min_vol_idx = np.argmin(mc_results[1])
                min_vol_ret, min_vol_vol = mc_results[0, min_vol_idx], mc_results[1, min_vol_idx]

                # Optimisasi presisi untuk mendapatkan bobot yang akurat
                weights_max_sharpe = optimize_portfolio(num_assets, mean_returns, cov_matrix, risk_free_rate, lambda w, m, c, rfr: -calculate_portfolio_stats(w, m, c, rfr)[2])
                weights_min_vol = optimize_portfolio(num_assets, mean_returns, cov_matrix, risk_free_rate, lambda w, m, c, rfr: calculate_portfolio_stats(w, m, c, rfr)[1])

                st.header("📊 Visualisasi Efficient Frontier")
                st.markdown("Setiap titik mewakili satu kemungkinan portofolio. Warna yang lebih cerah menunjukkan **Sharpe Ratio** (return per unit risiko) yang lebih tinggi.")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=mc_results[1], y=mc_results[0], mode='markers',
                    marker=dict(color=mc_results[2], showscale=True, colorscale='Viridis', size=5, colorbar=dict(title='Sharpe Ratio')),
                    name='Simulasi Portofolio'
                ))
                fig.add_trace(go.Scatter(x=[max_sharpe_vol], y=[max_sharpe_ret], mode='markers', marker=dict(symbol='star', color='red', size=15), name='Max Sharpe Ratio'))
                fig.add_trace(go.Scatter(x=[min_vol_vol], y=[min_vol_ret], mode='markers', marker=dict(symbol='diamond', color='black', size=15), name='Min Volatility'))
                fig.update_layout(title='Simulasi Portofolio & Batas Efisien', xaxis_title='Risiko (Volatilitas Tahunan)', yaxis_title='Return Tahunan', template='plotly_white', height=600)
                st.plotly_chart(fig, use_container_width=True)

                st.header("✅ Rekomendasi Alokasi Portofolio Optimal")
                col1, col2 = st.columns(2)

                def display_portfolio_details(container, title, weights, returns, cov, modal, rfr):
                    exp_ret, exp_vol, exp_sharpe = calculate_portfolio_stats(weights, returns, cov, rfr)
                    container.subheader(title)
                    container.metric("Estimasi Return Tahunan", f"{exp_ret:.2%}")
                    container.metric("Estimasi Risiko (Volatilitas)", f"{exp_vol:.2%}")
                    container.metric("Sharpe Ratio", f"{exp_sharpe:.2f}")
                    df = pd.DataFrame({"Saham": data.columns, "Bobot (%)": weights * 100, "Alokasi Dana (Rp)": weights * modal})
                    df = df[df['Bobot (%)'] > 0.1].sort_values(by="Bobot (%)", ascending=False)
                    container.dataframe(df.style.format({'Bobot (%)': '{:.2f}%', 'Alokasi Dana (Rp)': 'Rp {:,.0f}'}), use_container_width=True)
                
                with col1:
                    display_portfolio_details(st, "⭐ Portofolio Return Optimal (Max Sharpe Ratio)", weights_max_sharpe, mean_returns, cov_matrix, modal, risk_free_rate)
                with col2:
                    display_portfolio_details(st, "🛡️ Portofolio Risiko Terendah (Min Volatility)", weights_min_vol, mean_returns, cov_matrix, modal, risk_free_rate)


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
