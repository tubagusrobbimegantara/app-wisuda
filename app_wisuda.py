# app.py

import streamlit as st
import random

# --- Konfigurasi Halaman & CSS Kustom ---
st.set_page_config(
    page_title="Tebak Angka Misterius",
    page_icon="🔮",
    layout="centered"
)

# CSS untuk membuat tampilan kartu dan styling lainnya
st.markdown("""
    <style>
        /* Mengubah font utama */
        html, body, [class*="st-"] {
            font-family: 'Helvetica', 'Arial', sans-serif;
        }
        
        /* Kontainer utama untuk game */
        .game-container {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Kotak status dengan warna dinamis */
        .status-box {
            background-color: #e8f0fe; /* Biru muda default */
            border-left: 5px solid #005A9C;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            text-align: center;
        }
        .status-box h3 {
            margin: 0;
            color: #31333F;
        }
        .status-box.success {
            background-color: #d4edda;
            border-left-color: #155724;
        }
        .status-box.warning {
            background-color: #fff3cd;
            border-left-color: #856404;
        }

        /* Styling untuk riwayat tebakan */
        .history-box {
            padding: 1rem;
            background-color: #ffffff;
            border-radius: 8px;
            height: 200px;
            overflow-y: auto; /* Membuat bisa di-scroll jika riwayat panjang */
        }
        
        /* Tombol lebih menonjol */
        .stButton button {
            background-color: #0068c9;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #005A9C;
        }
        
    </style>
""", unsafe_allow_html=True)

# --- Inisialisasi State Permainan ---
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = "Ayo, mulai tebak angkanya!"
    st.session_state.message_class = "" # Untuk styling CSS
    st.session_state.history = [] # Untuk menyimpan riwayat

# --- Fungsi Reset Game ---
def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = "Game baru dimulai! Angka rahasia sudah direset."
    st.session_state.message_class = ""
    st.session_state.history = []


# --- Tampilan Utama ---

# Judul
st.title("🔮 Tebak Angka Misterius!")
st.markdown("Aku sudah memilih sebuah angka rahasia antara 1 dan 100. Bisakah kamu menebaknya?")
st.write("---")

# Kontainer Utama
with st.container():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # Layout 2 kolom
    col1, col2 = st.columns([1.5, 2])

    # --- Kolom Kiri: Input & Kontrol ---
    with col1:
        st.subheader("Ayo Tebak!")
        
        # Form tebakan hanya muncul jika game belum selesai
        if not st.session_state.game_over:
            with st.form(key="guess_form", clear_on_submit=True):
                guess = st.number_input("Masukkan angkamu:", min_value=1, max_value=100, step=1, key="user_guess", label_visibility="collapsed")
                submit_button = st.form_submit_button(label="Tebak Sekarang!")

            if submit_button:
                st.session_state.attempts += 1
                secret = st.session_state.secret_number
                
                if guess < secret:
                    st.session_state.message = f"Angka {guess} terlalu RENDAH! 📉"
                    st.session_state.message_class = "warning"
                    st.session_state.history.append(f"{guess} ➔ Terlalu Rendah")
                elif guess > secret:
                    st.session_state.message = f"Angka {guess} terlalu TINGGI! 📈"
                    st.session_state.message_class = "warning"
                    st.session_state.history.append(f"{guess} ➔ Terlalu Tinggi")
                else:
                    st.session_state.game_over = True
                    st.session_state.message = f"🎉 BENAR! Angkanya adalah {secret}!"
                    st.session_state.message_class = "success"
                    st.session_state.history.append(f"{guess} ➔ TEPAT! ✅")
                    st.balloons()
        else:
            st.success("Kamu berhasil! Klik 'Mulai Baru' untuk main lagi.")

        st.write("") # Spasi
        st.button("Mulai Baru 🔄", on_click=reset_game)

    # --- Kolom Kanan: Status & Riwayat ---
    with col2:
        # Kotak Status
        st.subheader("Status Petunjuk")
        st.markdown(f'<div class="status-box {st.session_state.message_class}"><h3>{st.session_state.message}</h3></div>', unsafe_allow_html=True)

        # Kotak Riwayat
        st.subheader("Riwayat Tebakan")
        with st.container():
            st.markdown('<div class="history-box">', unsafe_allow_html=True)
            if not st.session_state.history:
                st.write("Belum ada tebakan.")
            else:
                # Tampilkan riwayat dari yang terbaru
                for record in reversed(st.session_state.history):
                    st.markdown(f"- {record}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tampilkan jumlah percobaan
            st.metric(label="Total Percobaan", value=st.session_state.attempts)

    st.markdown('</div>', unsafe_allow_html=True)