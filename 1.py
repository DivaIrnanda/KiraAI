# pip install google-genai streamlit

import streamlit as st
from google import genai
from google.genai import types

# ======================
#      SYSTEM PROMPT
# ======================
SYSTEM_PROMPT = """
Anda adalah chatbot khusus tentang Seni Ukir Jepara.
Chatbot ini dibuat dan dikembangkan oleh Muhammad Diva Irnanda, mahasiswa Universitas Dian Nuswantoro.
Anda diperbolehkan menjawab seluruh hal yang masih berkaitan dengan Seni Ukir Jepara, termasuk: sejarah, motif ukiran, teknik ukir, jenis kayu, alat ukir, proses pembuatan, nilai budaya, tokoh pengrajin, daerah penghasil ukiran, sentra industri ukir, serta informasi edukatif lain seputar seni ukir di Kabupaten Jepara.
Jika pengguna mengajukan pertanyaan yang benar-benar tidak berkaitan dengan seni ukir Jepara, berikan jawaban penolakan secara sopan dengan menyampaikan bahwa chatbot ini hanya dapat menjawab pertanyaan seputar topik tersebut.
"""


# ======================
#      API KEY
# ======================
def load_api_key():
    try:
        return st.secrets["API_KEY"]
    except:
        return None


# ======================
#    CUSTOM CSS STYLE
# ======================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Poppins:wght@300;400;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Background dengan warna hijau atas bawah */
.stApp {
    background: linear-gradient(180deg, 
        #2D5016 0%, 
        #3D6B1F 5%,
        #8B4513 15%, 
        #A0522D 50%, 
        #CD853F 85%,
        #3D6B1F 95%,
        #2D5016 100%
    );
    background-attachment: fixed;
}

/* Header dengan ornamen kayu dan aksen hijau */
.main-header {
    background: linear-gradient(145deg, #5D4037 0%, #6D4C41 50%, #4E342E 100%);
    padding: 40px 20px 30px;
    border-radius: 0 0 30px 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    border-bottom: 4px solid #4A7C2C;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, 
        #4A7C2C 0%, 
        #D4AF37 20%,
        #F4E4C1 40%, 
        #D4AF37 60%, 
        #4A7C2C 100%
    );
}

.main-header::after {
    content: '🌿 ✦ 🌿';
    position: absolute;
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    color: #4A7C2C;
    font-size: 14px;
    letter-spacing: 8px;
}

.title-header {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #F4E4C1 0%, #D4AF37 50%, #F4E4C1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    letter-spacing: 3px;
}

.subtitle-text {
    font-family: 'Poppins', sans-serif;
    text-align: center;
    color: #E8D5B7;
    font-size: 18px;
    font-weight: 300;
    letter-spacing: 4px;
    margin-top: 5px;
}

/* Chat container dengan efek kayu */
.stApp > div > div > div {
    max-width: 900px;
    margin: 0 auto;
}

/* Bubble user - warna kayu jati gelap */
.user-bubble {
    background: linear-gradient(135deg, #6D4C41 0%, #5D4037 100%);
    color: #F4E4C1;
    padding: 14px 20px;
    border-radius: 20px 20px 5px 20px;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 16px;
    display: block;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    line-height: 1.6;
    border: 2px solid rgba(74, 124, 44, 0.4);
    position: relative;
}

.user-bubble::before {
    content: '👤';
    position: absolute;
    right: -35px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 24px;
    background: linear-gradient(135deg, #6D4C41 0%, #5D4037 100%);
    padding: 8px;
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Bubble bot - warna kayu mahoni terang */
.bot-bubble {
    background: linear-gradient(135deg, #F5DEB3 0%, #E8D5B7 50%, #DEB887 100%);
    color: #3E2723;
    padding: 14px 20px;
    border-radius: 20px 20px 20px 5px;
    max-width: 75%;
    margin-right: auto;
    margin-bottom: 16px;
    display: block;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    line-height: 1.7;
    border: 2px solid rgba(74, 124, 44, 0.3);
    position: relative;
}

.bot-bubble::before {
    content: '🎨';
    position: absolute;
    left: -35px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 24px;
    background: linear-gradient(135deg, #F5DEB3 0%, #DEB887 100%);
    padding: 8px;
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Animasi cursor kedip-kedip */
@keyframes blink-cursor {
    0%, 49% { 
        opacity: 1;
    }
    50%, 100% { 
        opacity: 0;
    }
}

/* Input area SELALU PUTIH dengan teks hitam */
.stChatInput,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: #FFFFFF !important;
    border-radius: 25px !important;
    border: 3px solid #4A7C2C !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}

.stChatInput input,
.stChatInput textarea {
    font-family: 'Poppins', sans-serif !important;
    color: #000000 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    background: #FFFFFF !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #4A7C2C !important;
}

/* Styling cursor supaya lebih tebal dan jelas */
.stChatInput input:focus,
.stChatInput textarea:focus {
    caret-color: #4A7C2C !important;
    animation: none !important;
}

/* Override caret untuk semua input */
[data-testid="stChatInput"] input,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"] textarea {
    caret-color: #4A7C2C !important;
}

.stChatInput input::placeholder,
.stChatInput textarea::placeholder {
    color: #666666 !important;
    opacity: 1 !important;
}

/* Override semua selector Streamlit untuk input */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] input,
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

[data-testid="stChatInputTextArea"],
[data-testid="stChatInputTextArea"] textarea {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Ornamen dekoratif */
.decorative-line {
    text-align: center;
    margin: 20px 0;
    color: #4A7C2C;
    font-size: 20px;
    letter-spacing: 10px;
}

/* Scrollbar custom dengan aksen hijau */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(45, 80, 22, 0.3);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #4A7C2C 0%, #6D4C41 100%);
    border-radius: 10px;
    border: 2px solid rgba(74, 124, 44, 0.4);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #3D6B1F 0%, #5D4037 100%);
}

/* Welcome message */
.welcome-card {
    background: linear-gradient(135deg, rgba(245, 222, 179, 0.95) 0%, rgba(222, 184, 135, 0.95) 100%);
    border-radius: 20px;
    padding: 30px;
    margin: 20px auto;
    max-width: 700px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    border: 3px solid rgba(74, 124, 44, 0.4);
    text-align: center;
}

.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: #3E2723;
    margin-bottom: 15px;
    font-weight: 700;
}

.welcome-text {
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    color: #5D4037;
    line-height: 1.8;
}

/* Floating animation untuk ornamen */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}

/* Footer dengan aksen hijau */
.stApp::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 80px;
    background: linear-gradient(180deg, transparent 0%, rgba(45, 80, 22, 0.3) 100%);
    pointer-events: none;
    z-index: 0;
}

</style>
"""

# ======================
#   STREAMLIT UI SETUP
# ======================
st.set_page_config(page_title="Kira Chat - Seni Ukir Jepara", page_icon="🎨", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown("""
<div class='main-header'>
    <div class='title-header floating'>KIRA CHAT</div>
    <div class='subtitle-text'>CHATBOT SENI UKIR JEPARA</div>
</div>
""", unsafe_allow_html=True)

api_key = load_api_key()

if not api_key:
    st.error("⚠️ API Key tidak ditemukan di st.secrets! Tambahkan ke .streamlit/secrets.toml")
    st.stop()

client = genai.Client(api_key=api_key)
model = "gemini-flash-latest"  

# ======================
#   SESSION STATE CHAT
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
#   TAMPILKAN RIWAYAT CHAT
# ======================

# Welcome message jika belum ada chat
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class='welcome-card'>
        <div class='welcome-title'>🪵 Selamat Datang di Kira Chat! 🪵</div>
        <div class='decorative-line'>✦ ❖ ✦</div>
        <div class='welcome-text'>
            Saya adalah asisten virtual yang siap membantu Anda menjelajahi keindahan 
            <strong>Seni Ukir Jepara</strong>. Tanyakan tentang sejarah, motif, teknik ukir, 
            jenis kayu, alat ukir, atau informasi lainnya seputar seni ukir jepara.
        </div>
        <div class='decorative-line'>✦ ❖ ✦</div>
    </div>
    """, unsafe_allow_html=True)

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# ======================
#   INPUT PENGGUNA
# ======================
user_input = st.chat_input("💬 Ketik pertanyaan Anda tentang Seni Ukir Jepara...")

if user_input:
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Gabungkan prompt
    combined_prompt = f"{SYSTEM_PROMPT}\n\nPertanyaan pengguna: {user_input}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=combined_prompt)],
        )
    ]

    generate_config = types.GenerateContentConfig()

# Streaming response
    full_response = ""
    try:
        with st.spinner("🎨 Sedang menyiapkan jawaban..."):
            response = client.models.generate_content_stream(
                model=model,
                contents=combined_prompt, 
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT, 
                    temperature=0.7,
                ),
            )
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    
    except Exception as e:
        # Baris di bawah ini HARUS menjorok ke dalam (4 spasi)
        st.error(f"Detail Eror dari Google: {e}")
        st.stop()

    # Simpan pesan bot ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Jalankan ulang untuk menampilkan pesan terbaru
    st.rerun()
