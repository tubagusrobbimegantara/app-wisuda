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
                    if guess < secret:
                        st.session_state.game_message = f"Angka {guess} terlalu RENDAH! 📉"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Rendah")
                    elif guess > secret:
                        st.session_state.game_message = f"Angka {guess} terlalu TINGGI! 📈"
                        st.session_state.game_message_class = "warning"
                        st.session_state.game_history.append(f"{guess} ➔ Terlalu Tinggi")
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
                st.markdown('<div class="history-box">', unsafe_allow_html=True)
                if not st.session_state.game_history:
                    st.write("Belum ada tebakan.")
                else:
                    for record in reversed(st.session_state.game_history):
                        st.markdown(f"- {record}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.metric(label="Total Percobaan", value=st.session_state.game_attempts)
#        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# APLIKASI 2: MANAJEMEN INVESTASI
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Kalkulator Optimisasi Portofolio Saham")
    st.markdown(
        "Aplikasi ini membantu Anda membentuk portofolio saham yang optimal berdasarkan Model Markowitz. "
        "Pilih profil risiko, modal, dan sektor saham yang Anda minati di menu sebelah kanan."
    )

    SEKTOR_SAHAM = {
        "🏦 Keuangan": ["BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK"],
        "📦 Barang Konsumen Primer": ["ICBP.JK", "INDF.JK", "GGRM.JK", "HMSP.JK"],
        "💻 Teknologi": ["GOTO.JK", "BUKA.JK", "EMTK.JK"],
        "⚡️ Energi": ["ADRO.JK", "PTBA.JK", "PGAS.JK", "MEDC.JK"],
        "🏭 Infrastruktur": ["TLKM.JK", "JSMR.JK", "WIKA.JK", "PGEO.JK"]
    }

    @st.cache_data
    def get_stock_data(tickers, start_date, end_date):
        data_download = yf.download(tickers, start=start_date, end=end_date, progress=False)
        if data_download.empty: return pd.DataFrame()
        if len(tickers) == 1:
            data = data_download[['Close']]
            data.columns = tickers
        else:
            data = data_download['Close']
        return data.dropna(axis=1)

    def hitung_portfolio_performance(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return returns, std

    def minimize_volatility(weights, mean_returns, cov_matrix):
        return hitung_portfolio_performance(weights, mean_returns, cov_matrix)[1]

    def optimasi_markowitz(mean_returns, cov_matrix, target_return):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                       {'type': 'eq', 'fun': lambda x: hitung_portfolio_performance(x, mean_returns, cov_matrix)[0] - target_return})
        bounds = tuple((0, 1) for asset in range(num_assets))
        initial_guess = num_assets * [1. / num_assets,]
        result = minimize(minimize_volatility, initial_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    # Input pengguna dipindah ke main body agar tidak tercampur dengan navigasi
    st.sidebar.header("⚙️ Parameter Investasi")
    profil_risiko = st.sidebar.selectbox("1. Pilih Profil Risiko Anda:", ("Rendah", "Moderat", "Tinggi"))
    modal = st.sidebar.number_input("2. Masukkan Modal Investasi (Rp):", min_value=1000000, step=1000000, value=100000000)
    sektor_terpilih = st.sidebar.multiselect("3. Pilih Sektor Saham:", options=list(SEKTOR_SAHAM.keys()), default=["🏦 Keuangan", "⚡️ Energi"])
    
    if not sektor_terpilih:
        st.warning("Mohon pilih minimal satu sektor saham.")
    else:
        tickers_pilihan = sorted([saham for sektor in sektor_terpilih for saham in SEKTOR_SAHAM[sektor]])
        
        if st.sidebar.button("🚀 Buat Rekomendasi Portofolio!", type="primary"):
            with st.spinner("Mengambil data dan menghitung..."):
                end_date = datetime.now()
                start_date_insample = end_date - timedelta(days=3*365)
                end_date_insample = end_date - timedelta(days=1*365)
                start_date_outsample = end_date_insample
                
                stock_data_insample = get_stock_data(tickers_pilihan, start_date_insample, end_date_insample)
                
                if stock_data_insample.empty or stock_data_insample.shape[1] < 2:
                    st.error("Data saham tidak cukup untuk optimisasi. Pastikan minimal ada 2 saham dengan data lengkap. Coba pilih sektor lain.")
                    st.stop()

                tickers = stock_data_insample.columns.tolist()
                returns = stock_data_insample.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                min_return, max_return = np.min(mean_returns) * 252, np.max(mean_returns) * 252
                
                if profil_risiko == 'Rendah': target_return = min_return + 0.2 * (max_return - min_return)
                elif profil_risiko == 'Moderat': target_return = min_return + 0.5 * (max_return - min_return)
                else: target_return = min_return + 0.8 * (max_return - min_return)

                result = optimasi_markowitz(mean_returns, cov_matrix, target_return)
                
                if not result.success:
                    st.error(f"Optimisasi gagal: {result.message}. Coba ubah pilihan.")
                    st.stop()
                    
                bobot_optimal = result.x
                exp_return, exp_volatility = hitung_portfolio_performance(bobot_optimal, mean_returns, cov_matrix)
                sharpe_ratio = exp_return / exp_volatility if exp_volatility > 0 else 0

                st.header("✅ Rekomendasi Portofolio Optimal Anda")
                col1, col2, col3 = st.columns(3)
                col1.metric("Target Return Tahunan", f"{exp_return:.2%}")
                col2.metric("Estimasi Risiko (Volatilitas)", f"{exp_volatility:.2%}")
                col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

                df_alokasi = pd.DataFrame({"Saham": tickers, "Bobot (%)": bobot_optimal * 100, "Alokasi Dana (Rp)": bobot_optimal * modal})
                df_alokasi = df_alokasi[df_alokasi['Bobot (%)'] > 0.1].sort_values(by="Bobot (%)", ascending=False)
                st.dataframe(df_alokasi.style.format({'Bobot (%)': '{:.2f}%', 'Alokasi Dana (Rp)': 'Rp {:,.0f}'}), use_container_width=True)
                
                st.header("🔬 Analisis Kinerja Portofolio (Uji Out-of-Sample)")
                stock_data_outsample = get_stock_data(tickers, start_date_outsample, end_date)
                ihsg_data = get_stock_data(['^JKSE'], start_date_outsample, end_date)
                
                if not stock_data_outsample.empty and not ihsg_data.empty:
                    portfolio_returns = stock_data_outsample.pct_change().dropna().dot(bobot_optimal)
                    cumulative_returns = (1 + portfolio_returns).cumprod() - 1
                    ihsg_returns = ihsg_data.pct_change().dropna().iloc[:,0]
                    cumulative_ihsg_returns = (1 + ihsg_returns).cumprod() - 1
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=cumulative_returns.index, y=cumulative_returns.values * 100, mode='lines', name='Portofolio Optimal Anda'))
                    fig.add_trace(go.Scatter(x=cumulative_ihsg_returns.index, y=cumulative_ihsg_returns.values * 100, mode='lines', name='IHSG (Benchmark)'))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    final_return, final_ihsg_return = cumulative_returns.iloc[-1], cumulative_ihsg_returns.iloc[-1]
                    st.metric(f"Return Portofolio Anda (1 Tahun)", f"{final_return:.2%}", delta=f"{(final_return - final_ihsg_return):.2%} vs IHSG")


# ==============================================================================
# NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.title("Menu Utama")
app_choice = st.sidebar.radio(
    "Pilih Aplikasi:",
    ("🔮 Game", "📈 Manajemen Investasi")
)
st.sidebar.markdown("---")


# Panggil fungsi aplikasi yang sesuai dengan pilihan
if app_choice == "🔮 Game":
    run_game_app()
elif app_choice == "📈 Manajemen Investasi":
    run_portfolio_app()
