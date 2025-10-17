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
# APLIKASI UTAMA: GAME TEBAK ANGKA (DENGAN ENTER & TANPA SCOREBOX)
# ==============================================================================
def run_game_app():
    # --- CSS Modern UI (Glassmorphism & Neon Glow) ---
    st.markdown("""
        <style>
        .main {
            background: radial-gradient(circle at top left, #111, #000);
            color: #fff;
        }
        .main-title {
            font-size: 2.5rem;
            text-align: center;
            font-weight: 900;
            background: linear-gradient(90deg, #00f2ff, #ff00d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stButton>button {
            background: linear-gradient(135deg, #00d4ff, #007bff);
            border: none;
            border-radius: 12px;
            padding: 0.8rem 2rem;
            font-weight: bold;
            color: white;
            box-shadow: 0px 0px 10px #00d4ff55;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0px 0px 20px #00d4ff88;
        }
        </style>
    """, unsafe_allow_html=True)

    # Inisialisasi Session State yang aman
    defaults = {
        "secret_number": random.randint(1, 100), "attempts": 0, "high_score": 999,
        "game_over": False, "feedback": "Ayo mulai! Aku sudah memilih angka rahasia 🎲"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    def restart_game():
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.feedback = "Game baru dimulai! Coba tebak angkanya 🎯"

    # Header
    st.markdown("<h1 class='main-title'>🎮 Arena Tebak Angka 🔮</h1>", unsafe_allow_html=True)
    
    # Menampilkan skor secara ringkas di tengah
    st.markdown(f"<div style='text-align: center; font-size: 1.1rem; margin-bottom: 20px;'>Percobaan: <b>{st.session_state.attempts}</b> | Rekor Terbaik: <b>{st.session_state.high_score}</b> 🏆</div>", unsafe_allow_html=True)

    st.write("Tebak angka rahasia antara **1 dan 100**. Coba capai rekor **percobaan paling sedikit!**")
    st.divider()

    # --- Layout Utama (Disederhanakan tanpa kolom) ---
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    
    st.markdown(f"### 💬 {st.session_state.feedback}", unsafe_allow_html=True)

    if st.session_state.game_over:
        st.success("🎉 Selamat! Kamu menebak dengan benar!")
        st.balloons()
        if st.session_state.attempts < st.session_state.high_score:
            st.session_state.high_score = st.session_state.attempts
            st.toast("🏆 Rekor Baru!", icon="🥇")
        if st.button("🔁 Main Lagi"):
            restart_game()
            st.rerun()
    else:
        # Menggunakan st.form agar 'Enter' berfungsi
        with st.form(key="guess_form"):
            guess = st.number_input("Masukkan tebakanmu:", min_value=1, max_value=100, step=1, label_visibility="visible")
            submitted = st.form_submit_button("🚀 Tebak Sekarang!")

        if submitted:
            st.session_state.attempts += 1
            secret = st.session_state.secret_number
            diff = abs(guess - secret)

            if guess < secret:
                st.toast("📉 Terlalu rendah!")
                if diff < 5: st.session_state.feedback = f"<span style='color:#00ff99'>🔥 Sangat dekat!</span> {guess} hanya sedikit **lebih rendah**!"
                elif diff <= 20: st.session_state.feedback = f"⚡ Hampir! {guess} sedikit **di bawah** 🎯"
                else: st.session_state.feedback = f"🥶 Masih jauh! {guess} terlalu **rendah**."
            elif guess > secret:
                st.toast("📈 Terlalu tinggi!")
                if diff < 5: st.session_state.feedback = f"<span style='color:#ff9933'>🔥 Sangat dekat!</span> {guess} hanya sedikit **lebih tinggi**!"
                elif diff <= 20: st.session_state.feedback = f"⚡ Hampir! {guess} sedikit **di atas** 🎯"
                else: st.session_state.feedback = f"🥵 Masih jauh! {guess} terlalu **tinggi**."
            else:
                st.toast("🎯 Tepat sekali!")
                st.session_state.feedback = f"🎉 Angka {secret} adalah tebakanmu! Kamu butuh {st.session_state.attempts} percobaan."
                st.session_state.game_over = True
            
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# APLIKASI 2: ANALISIS PORTOFOLIO
# ==============================================================================
def run_portfolio_app():
    st.title("📈 Analisis & Backtesting Portofolio Saham")
    
    st.markdown("""
    ### 🧮 Teori Model Matematika
    
    Aplikasi ini menggunakan prinsip **Optimisasi Portofolio Mean-Variance** 
    yang diperkenalkan oleh **Harry Markowitz (1952)** dalam teori portofolio modern (Modern Portfolio Theory).
    
    Tujuan utama model ini adalah **menyeimbangkan risiko dan imbal hasil (risk-return trade-off)** 
    melalui kombinasi bobot aset yang optimal.
    
    Secara matematis, untuk $n$ aset dengan return rata-rata $\\mu_i$ dan kovarians $\\Sigma_{ij}$:
    
    $$
    \\begin{aligned}
    \\text{Maksimalkan} \\quad & E[R_p] = \\sum_{i=1}^{n} w_i \\mu_i \\\\
    \\text{dengan risiko} \\quad & \\sigma_p^2 = w^T \\Sigma w \\\\
    \\text{dan kendala} \\quad & \\sum_{i=1}^{n} w_i = 1, \\quad w_i \\ge 0
    \\end{aligned}
    $$
    
    Rasio **Sharpe Ratio (William Sharpe, 1966)** digunakan sebagai ukuran efisiensi portofolio:
    
    $$
    S = \\frac{E[R_p] - R_f}{\\sigma_p}
    $$
    
    di mana:
    - $E[R_p]$ : return ekspektasi portofolio  
    - $R_f$ : tingkat bebas risiko (diasumsikan 0 dalam simulasi ini)  
    - $\\sigma_p$ : volatilitas (risiko) portofolio  
    
    Untuk menemukan kombinasi terbaik, digunakan metode **Simulasi Monte Carlo**, 
    yaitu menghasilkan ribuan kombinasi bobot acak $w_i$ yang memenuhi $\\sum w_i = 1$, 
    lalu memilih kombinasi dengan **Sharpe Ratio tertinggi**.
    
    Setelah portofolio optimal diperoleh berdasarkan data historis **(In-Sample)**, 
    performanya diuji terhadap data **(Out-of-Sample)** dan dibandingkan dengan indeks acuan **IHSG**.
    """)
    
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
    with col1: selected_tickers = st.multiselect("1. Pilih Saham LQ45 (minimal 2)", options=LQ45_TICKERS, default=["ACES.JK", "ADRO.JK", "AKRA.JK", "AMMN.JK", "AMRT.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "JSMR.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK"])
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
                df_alokasi = pd.DataFrame({"Saham": in_sample_data.columns, "Bobot": optimal_weights, "Alokasi_Dana": optimal_weights*modal}).query("Bobot > 0.001").sort_values("Bobot", ascending=False)
                st.info("Alokasi portofolio optimal ditemukan berdasarkan Sharpe Ratio tertinggi.")
                st.dataframe(df_alokasi.assign(Bobot=lambda x: x['Bobot'].map('{:.2%}'.format), Alokasi_Dana=lambda x: x['Alokasi_Dana'].map('Rp{:,.0f}'.format)), use_container_width=True)
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
# APLIKASI 3: PANEN BERKELANJUTAN
# ==============================================================================
def run_harvesting_app():
    st.title("🐄 Simulasi Panen Ternak Berkelanjutan")
    st.markdown("Aplikasi ini mensimulasikan dampak panen tahunan terhadap populasi ternak. Gunakan model ini untuk menentukan apakah tingkat panen Anda berkelanjutan atau akan menyebabkan kepunahan.")
    st.markdown("""
    ### 🧮 Teori Model Matematika
    
    Model yang digunakan pada simulasi ini adalah **model logistik dengan panen konstan**, 
    yang secara umum dinyatakan dengan persamaan diferensial berikut:
    
    $$
    \\frac{dP}{dt} = rP\\left(1 - \\frac{P}{K}\\right) - H
    $$
    
    di mana:
    
    - $P(t)$ : populasi ternak pada waktu $t$  
    - $r$ : laju pertumbuhan alami populasi  
    - $K$ : daya tampung maksimum lingkungan (*carrying capacity*)  
    - $H$ : tingkat panen tetap (jumlah ternak yang diambil setiap tahun)
    
    Tanpa panen ($H = 0$), populasi akan bertumbuh secara **logistik** hingga mencapai $K$.  
    Namun, dengan adanya panen, populasi dapat:
    
    - **Stabil dan berkelanjutan**, jika $H$ lebih kecil dari batas lestari maksimum  
    - **Menurun perlahan**, jika $H$ mendekati batas kritis  
    - **Pun⟨ah**, jika $H$ terlalu besar (melebihi kapasitas regenerasi populasi)
    
    Nilai panen maksimum berkelanjutan (*Maximum Sustainable Yield*, MSY) diperoleh ketika:
    
    $$
    H_{msy} = \\frac{rK}{4}
    $$
    
    Aplikasi ini menggunakan bentuk **diskretisasi tahunan** dari model tersebut untuk mensimulasikan 
    perubahan populasi selama beberapa tahun ke depan.
    """)
    
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
        else:
            st.success(f"**Status: Berkelanjutan.** Tingkat panen Anda ({H} ekor/tahun) berada pada level yang aman dan populasi dapat bertahan atau bertumbuh.")
        
# ==============================================================================
# APLIKASI 4: GEOMETRI FRAKTAL (KODE DISEMPURNAKAN & TATA LETAK DIUBAH)
# ==============================================================================
def run_fractal_app():
    st.title("🎨 Eksplorasi Fraktal Interaktif")
    st.markdown("Jelajahi pola **fraktal klasik dan modern** yang muncul dari aturan sederhana namun menghasilkan keindahan kompleks ✨.")
    
    col_plot, col_settings = st.columns([3, 1]) # Kolom untuk plot (kiri, lebih besar) dan settings (kanan, lebih kecil)

    with col_settings: # Pengaturan di kolom kanan
        fractal_type = st.selectbox(
            "🌀 Pilih Jenis Fraktal",
            ("Segitiga Sierpinski", "Pohon Fraktal", "Koch Snowflake", "Dragon Curve", "Kapal Terbakar", "Mandelbrot Klasik")
        )
        # Slider Cerdas yang menyesuaikan rentang nilai
        if fractal_type in ["Mandelbrot Klasik", "Kapal Terbakar"]:
            iterations = st.slider("🔁 Jumlah Iterasi", 20, 300, 75, 10)
        elif fractal_type == "Segitiga Sierpinski":
            iterations = st.slider("🔁 Kepadatan Titik", 1, 10, 6, 1)
        elif fractal_type == "Dragon Curve":
            iterations = st.slider("🔁 Jumlah Lipatan", 1, 16, 12, 1)
        elif fractal_type == "Koch Snowflake":
            iterations = st.slider("🔁 Tingkat Detail", 0, 6, 4, 1)
        elif fractal_type == "Pohon Fraktal":
            iterations = st.slider("🔁 Kedalaman Ranting", 1, 11, 8, 1)

    @st.cache_data
    def generate_fractal(width, height, max_iter, type):
        if type == "Segitiga Sierpinski":
            points = np.array([[width / 2, 0], [0, height - 1], [width - 1, height - 1]])
            p = np.array([random.uniform(0, width), random.uniform(0, height)])
            image_data = np.zeros((height, width))
            for _ in range(max_iter * 50000):
                target_vertex = random.choice(points); p = (p + target_vertex) / 2
                x, y = int(p[0]), int(p[1])
                if 0 <= x < width and 0 <= y < height: image_data[y, x] = 1
            return "heatmap", image_data

        elif type in ["Mandelbrot Klasik", "Kapal Terbakar"]:
            x, y = np.linspace(-2, 2, width), np.linspace(-2, 2, height)
            c = x[:, np.newaxis] + 1j * y[np.newaxis, :]; z = np.zeros_like(c, dtype=complex)
            output = np.zeros(c.shape)
            for it in range(max_iter):
                not_diverged = np.abs(z) < 10; output[not_diverged] = it
                if type == "Mandelbrot Klasik": z[not_diverged] = z[not_diverged] ** 2 + c[not_diverged]
                else: z_abs = np.abs(z[not_diverged].real) + 1j * np.abs(z[not_diverged].imag); z[not_diverged] = z_abs ** 2 + c[not_diverged]
            return "heatmap", output

        elif type == "Dragon Curve":
            axiom, rules = "FX", {"X": "X+YF+", "Y": "-FX-Y"}
            path = axiom
            for _ in range(max_iter): path = "".join(rules.get(c, c) for c in path)
            x, y, angle = 0, 0, 0
            coords = [(x, y)]
            for cmd in path:
                if cmd == "F": x += math.cos(math.radians(angle)); y += math.sin(math.radians(angle)); coords.append((x, y))
                elif cmd == "+": angle += 90
                elif cmd == "-": angle -= 90
            return "lines", np.array(coords)

        elif type == "Koch Snowflake":
            def koch_curve(p1, p2, depth):
                if depth == 0: return [p1, p2]
                p1, p2 = np.array(p1), np.array(p2); delta = (p2 - p1) / 3
                pA, pB = p1 + delta, p1 + 2 * delta
                pC = pA + np.array([delta[0] * 0.5 - delta[1] * 0.866, delta[0] * 0.866 + delta[1] * 0.5]) # Rotasi 60 derajat
                return koch_curve(p1, pA, depth - 1)[:-1] + koch_curve(pA, pC, depth - 1)[:-1] + koch_curve(pC, pB, depth - 1)[:-1] + koch_curve(pB, p2, depth - 1)
            # Koordinat titik awal segitiga sama sisi, diskalakan dan digeser agar terlihat bagus
            side_length = 0.8
            offset_y = 0.1
            p1_koch = np.array([0.1, 0.288]) + np.array([0, offset_y])
            p2_koch = np.array([0.9, 0.288]) + np.array([0, offset_y])
            p3_koch = np.array([0.5, 0.288 + side_length * math.sqrt(3)/2]) + np.array([0, offset_y])
            
            points = koch_curve(p1_koch, p2_koch, max_iter)[:-1] + \
                     koch_curve(p2_koch, p3_koch, max_iter)[:-1] + \
                     koch_curve(p3_koch, p1_koch, max_iter)[:-1]
            return "lines", np.array(points)

        elif type == "Pohon Fraktal":
            lines = []
            def draw_tree(x1, y1, angle, depth):
                if depth > 0:
                    # Skala panjang ranting agar ranting yang lebih dalam lebih pendek
                    length = depth * 10.0 
                    x2 = x1 + math.cos(math.radians(angle)) * length
                    y2 = y1 + math.sin(math.radians(angle)) * length
                    lines.append(((x1, y1), (x2, y2)))
                    draw_tree(x2, y2, angle - 25, depth - 1) # Sudut diubah agar lebih menarik
                    draw_tree(x2, y2, angle + 25, depth - 1)
            # Mulai pohon dari bagian bawah tengah gambar
            draw_tree(width // 2, height - 50, -90, max_iter) # y1 diubah ke bawah
            return "segments", lines
    
    with col_plot: # Gambar di kolom kiri
        with st.spinner(f"🧠 Membuat '{fractal_type}'..."):
            width, height = 800, 800
            render_mode, data = generate_fractal(width, height, iterations, fractal_type)
            fig = go.Figure()

            if render_mode == "heatmap":
                fig.add_trace(go.Heatmap(z=data, colorscale='Plasma', showscale=False))
                fig.update_yaxes(autorange="reversed") # Agar asal di kiri atas
            elif render_mode == "lines":
                fig.add_trace(go.Scatter(x=data[:, 0], y=data[:, 1], mode='lines', line=dict(color='cyan', width=1.5)))
                # Auto-scale sumbu untuk fraktal garis
                fig.update_layout(xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
            elif render_mode == "segments":
                all_x, all_y = [], []
                for (x1, y1), (x2, y2) in data:
                    all_x.extend([x1, x2, None])
                    all_y.extend([y1, y2, None])
                fig.add_trace(go.Scatter(x=all_x, y=all_y, mode='lines', line=dict(color='lightgreen', width=1.5)))
                # Auto-scale sumbu untuk fraktal garis
                fig.update_layout(xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
            
            fig.update_layout(title=f"Fraktal: {fractal_type}", xaxis_visible=False, yaxis_visible=False, height=600, template='plotly_dark', showlegend=False)
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
