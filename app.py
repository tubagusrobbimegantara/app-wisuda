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
    st.write(
        "Aplikasi ini menghitung kuantitas pesanan optimal berdasarkan **data penjualan bulanan** dan biaya persediaan Anda."
    )
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
            with p1:
                S = st.number_input("Biaya Pemesanan (S)", min_value=0.0, value=50.0, step=5.0, format="%.2f", help="Biaya tetap yang dikeluarkan setiap kali melakukan pemesanan.")
            with p2:
                H = st.number_input("Biaya Penyimpanan/Unit (H)", min_value=0.01, value=5.0, step=0.5, format="%.2f", help="Biaya untuk menyimpan satu unit barang selama satu tahun.")
            with p3:
                L = st.number_input("Lead Time (hari)", min_value=1, value=7, step=1, help="Waktu yang dibutuhkan dari saat pemesanan hingga barang diterima.")
            submit_button = st.form_submit_button(label='✅ Hitung EOQ', use_container_width=True)
    if submit_button:
        D = jan + feb + mar + apr + may + jun + jul + aug + sep + okt + nov + des
        if H <= 0:
            st.error("Biaya Penyimpanan (H) harus lebih besar dari nol.")
        elif D <= 0:
            st.warning("Total penjualan tahunan adalah nol. Tidak ada yang perlu dipesan.")
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
            col1.metric(label="Economic Order Quantity (EOQ)", value=f"{eoq:,.2f} unit")
            col2.metric(label="Titik Pemesanan Kembali (ROP)", value=f"{rop:,.2f} unit")
            col3.metric(label="Total Biaya Persediaan Minimum", value=f"Rp {total_inventory_cost:,.2f}")
            col4, col5, col6 = st.columns(3)
            col4.metric(label="Jumlah Pesanan per Tahun", value=f"{num_orders:,.2f} kali")
            col5.metric(label="Biaya Pemesanan Tahunan", value=f"Rp {annual_ordering_cost:,.2f}")
            col6.metric(label="Biaya Penyimpanan Tahunan", value=f"Rp {annual_holding_cost:,.2f}")
            st.header("📈 Visualisasi Kurva Biaya")
            q_values = np.linspace(max(1, eoq * 0.1), eoq * 2, 400)
            holding_costs = (q_values / 2) * H
            ordering_costs = (D / q_values) * S
            total_costs = holding_costs + ordering_costs
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=q_values, y=holding_costs, mode='lines', name='Biaya Penyimpanan'))
            fig.add_trace(go.Scatter(x=q_values, y=ordering_costs, mode='lines', name='Biaya Pemesanan'))
            fig.add_trace(go.Scatter(x=q_values, y=total_costs, mode='lines', name='Total Biaya', line=dict(color='black', width=3, dash='dash')))
            fig.add_vline(x=eoq, line_width=2, line_dash="dot", line_color="green", annotation_text="EOQ", annotation_position="top right")
            fig.add_trace(go.Scatter(x=[eoq], y=[total_inventory_cost], mode='markers', marker=dict(color='red', size=12, symbol='star'), name='Titik Biaya Minimum'))
            fig.update_layout(title='Analisis Biaya Persediaan vs. Kuantitas Pesanan', xaxis_title='Kuantitas Pesanan (Unit)', yaxis_title='Biaya Tahunan (Rp)', legend_title='Komponen Biaya', hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            st.info("Titik terendah pada kurva Total Biaya menunjukkan biaya persediaan minimum, yang tercapai tepat pada nilai EOQ.")

# ==============================================================================
# APLIKASI 3: ANALISIS PORTOFOLIO DENGAN BACKTESTING (DIMODIFIKASI TOTAL)
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Analisis & Backtesting Portofolio Saham")
    st.markdown(
        """
        Aplikasi ini melakukan analisis portofolio dalam dua tahap:
        1.  **Optimisasi (In-Sample)**: Menentukan alokasi bobot saham terbaik menggunakan data historis **2015-2023** untuk mendapatkan *Sharpe Ratio* tertinggi.
        2.  **Backtesting (Out-of-Sample)**: Menguji kinerja alokasi tersebut pada data **2024-sekarang** untuk melihat performa di dunia nyata.
        """
    )
    st.write("---")

    LQ45_TICKERS = sorted(["ACES.JK", "ADRO.JK", "AKRA.JK", "AMMN.JK", "AMRT.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "JSMR.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK"])

    @st.cache_data
    def get_stock_data(tickers, start_date, end_date):
        try:
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
            return data.dropna(axis=1)
        except Exception as e:
            st.error(f"Gagal mengambil data: {e}")
            return pd.DataFrame()

    def calculate_portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate):
        returns = np.sum(mean_returns * weights) * 252
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        sharpe = (returns - risk_free_rate) / volatility if volatility != 0 else 0
        return returns, volatility, sharpe

    def run_monte_carlo_simulation(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
        num_assets = len(mean_returns)
        results = np.zeros((3, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            p_return, p_vol, p_sharpe = calculate_portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate)
            results[0, i], results[1, i], results[2, i] = p_return, p_vol, p_sharpe
        return results, weights_record

    # --- Input Parameter ---
    st.subheader("⚙️ Masukkan Parameter Analisis")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_tickers = st.multiselect(
            "1. Pilih Saham LQ45 (minimal 2)", 
            options=LQ45_TICKERS, 
            default=["BBCA.JK", "TLKM.JK", "BMRI.JK", "ASII.JK"]
        )
    with col2:
        modal = st.number_input("2. Modal Awal (Rp)", min_value=1_000_000, step=1_000_000, value=100_000_000)
    with col3:
        risk_free_rate = st.number_input("3. Tingkat Bebas Risiko (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.1) / 100
        
    num_simulations = st.select_slider("4. Jumlah Simulasi", options=[1000, 5000, 10000, 20000], value=5000)
    st.write("")

    if st.button("🚀 Hitung & Uji Portofolio", type="primary", use_container_width=True):
        if len(selected_tickers) < 2:
            st.error("Mohon pilih minimal 2 saham.")
        else:
            # --- TAHAP 1: OPTIMISASI (IN-SAMPLE) ---
            st.header("1. Hasil Optimisasi (In-Sample: 2015-2023)")
            with st.spinner("Menjalankan optimisasi pada data 2015-2023..."):
                in_sample_start, in_sample_end = '2015-01-01', '2023-12-31'
                in_sample_data = get_stock_data(selected_tickers, in_sample_start, in_sample_end)

                if in_sample_data.empty:
                    st.error("Gagal mendapatkan data In-Sample. Proses dihentikan.")
                    return

                returns = in_sample_data.pct_change().dropna()
                mean_returns, cov_matrix = returns.mean(), returns.cov()
                
                mc_results, mc_weights = run_monte_carlo_simulation(num_simulations, mean_returns, cov_matrix, risk_free_rate)
                
                max_sharpe_idx = np.argmax(mc_results[2])
                optimal_weights = np.array(mc_weights[max_sharpe_idx])
                
                exp_return, exp_vol, exp_sharpe = mc_results[0, max_sharpe_idx], mc_results[1, max_sharpe_idx], mc_results[2, max_sharpe_idx]

                st.info(f"Ditemukan alokasi optimal dari {num_simulations:,} simulasi pada data historis **{in_sample_start}** hingga **{in_sample_end}**.")

                st.subheader("✅ Rekomendasi Alokasi Optimal")
                m1, m2, m3 = st.columns(3)
                m1.metric("Estimasi Return Tahunan", f"{exp_return:.2%}")
                m2.metric("Estimasi Risiko (Volatilitas)", f"{exp_vol:.2%}")
                m3.metric("Sharpe Ratio", f"{exp_sharpe:.2f}")

                df_alokasi = pd.DataFrame({
                    "Saham": in_sample_data.columns, 
                    "Bobot": optimal_weights
                })
                df_alokasi = df_alokasi[df_alokasi['Bobot'] > 0.001].sort_values(by="Bobot", ascending=False)

                c1, c2 = st.columns([1, 1])
                with c1:
                    st.dataframe(
                        df_alokasi.assign(Bobot=lambda x: x['Bobot'].map('{:.2%}'.format)),
                        use_container_width=True
                    )
                with c2:
                    fig_pie = go.Figure(data=[go.Pie(labels=df_alokasi['Saham'], values=df_alokasi['Bobot'], hole=.3)])
                    fig_pie.update_layout(title_text='Distribusi Alokasi Dana', showlegend=False)
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("---")
            # --- TAHAP 2: BACKTESTING (OUT-OF-SAMPLE) ---
            st.header("2. Hasil Backtesting (Out-of-Sample: 2024-Sekarang)")
            with st.spinner("Menguji portofolio pada data 2024-sekarang..."):
                out_sample_start, out_sample_end = '2024-01-01', datetime.now().strftime('%Y-%m-%d')
                out_sample_data = get_stock_data(selected_tickers, out_sample_start, out_sample_end)

                if out_sample_data.empty or len(out_sample_data) < 2:
                    st.warning("Tidak cukup data Out-of-Sample (2024-sekarang) untuk melakukan backtesting.")
                    return
                
                # Pastikan kolom saham sama antara in-sample dan out-of-sample
                common_tickers = list(set(in_sample_data.columns) & set(out_sample_data.columns))
                if len(common_tickers) != len(selected_tickers):
                    st.warning("Beberapa saham tidak memiliki data di kedua periode. Backtest disesuaikan.")
                
                # Filter bobot dan data untuk saham yang ada di kedua periode
                df_alokasi_filtered = df_alokasi[df_alokasi['Saham'].isin(common_tickers)]
                filtered_weights = df_alokasi_filtered['Bobot'].values
                filtered_weights /= np.sum(filtered_weights) # Normalisasi ulang bobot
                
                out_sample_returns = out_sample_data[df_alokasi_filtered['Saham']].pct_change().dropna()
                
                # Hitung return portofolio harian
                portfolio_returns = out_sample_returns.dot(filtered_weights)
                
                # Hitung pertumbuhan modal
                cumulative_returns = (1 + portfolio_returns).cumprod()
                portfolio_growth = modal * cumulative_returns

                # Hitung metrik kinerja out-of-sample
                total_return = cumulative_returns.iloc[-1] - 1
                trading_days = len(portfolio_returns)
                annualized_return = (1 + total_return)**(252/trading_days) - 1 if trading_days > 0 else 0
                annualized_volatility = portfolio_returns.std() * np.sqrt(252)

                st.success(f"Portofolio diuji pada data **{out_sample_start}** hingga **{out_sample_end}**.")
                
                bm1, bm2, bm3, bm4 = st.columns(4)
                bm1.metric("Nilai Akhir Portofolio", f"Rp {portfolio_growth.iloc[-1]:,.0f}")
                bm2.metric("Total Return", f"{total_return:.2%}")
                bm3.metric("Return Tahunan (Annualized)", f"{annualized_return:.2%}")
                bm4.metric("Risiko Tahunan (Annualized)", f"{annualized_volatility:.2%}")

                # Visualisasi Pertumbuhan Portofolio
                fig_growth = go.Figure()
                fig_growth.add_trace(go.Scatter(x=portfolio_growth.index, y=portfolio_growth, mode='lines', name='Nilai Portofolio'))
                fig_growth.update_layout(
                    title='Pertumbuhan Nilai Portofolio (Out-of-Sample)',
                    xaxis_title='Tanggal',
                    yaxis_title='Nilai Portofolio (Rp)',
                    template='plotly_white'
                )
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

if app_choice == "📈 Analisis Portofolio":
    run_portfolio_app()
elif app_choice == "📦 Kalkulator Persediaan (EOQ)":
    run_eoq_app()
elif app_choice == "🔮 Game Tebak Angka":
    run_game_app()
