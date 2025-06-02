import streamlit as st
import requests
from PIL import Image

# ✅ Load API key securely from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Email Tone Adjuster", layout="centered")

# --- Load QR Image ---
qr = Image.open("tipjar_qr.png")

# --- Layout: Title + QR Code ---
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown(
        """
        <div style='margin-bottom: 0.5rem;'>
            <h1 style='margin-bottom: 0;'>✉️ Email Tone Adjuster</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<div style='padding-top: 8px;'>", unsafe_allow_html=True)
    st.image(qr, width=135)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Email Input Label ---
st.markdown("### 📨 Your Email")

# --- Email Input ---
email_input = st.text_area("", height=200)

# --- Tone Selection ---
tone_options = [
    "Polite", "Confident", "Formal", "Informal", "Concise",
    "Apologetic", "Appreciative", "Supportive", "Neutral", "Direct",
    "Empathetic", "Sympathetic", "Understanding", "Encouraging", "Positive"
]

selected_tone = st.selectbox("🎯 Choose a Tone", tone_options)

# --- Rewrite Button ---
if st.button("🔁 Rewrite Email"):
    if not email_input.strip():
        st.warning("Please paste an email first.")
    else:
        st.info(f"Rewriting email in a *{selected_tone.lower()}* tone...")

        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an assistant that rewrites emails in a {selected_tone.lower()} tone."
                },
                {
                    "role": "user",
                    "content": email_input
                }
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            rewritten = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Rewritten Email:")
            st.write(rewritten)
        else:
            st.error(f"❌ OpenAI error: {response.status_code} - {response.text}")
