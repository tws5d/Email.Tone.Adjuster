import streamlit as st
import requests
from PIL import Image
import base64
from io import BytesIO

# ✅ Load API key securely from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Email Tone Adjuster", layout="centered")

# --- Load and convert QR Image to base64 ---
qr = Image.open("tipjar_qr.png")

def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

qr_base64 = pil_to_base64(qr)

# --- Title and subtitle ---
st.markdown(
    """
    <h1 style="margin-bottom: 0.25rem;">✉️ Email Tone Adjuster</h1>
    <p style="margin-top: 0; margin-bottom: 0.75rem; font-size: 0.9rem;">
        Paste your email and choose a tone to rewrite it:
    </p>
    """,
    unsafe_allow_html=True
)

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

# --- QR Code Footer with Donation Message ---
st.markdown(
    f"""
    <div style="display: flex; flex-direction: column; align-items: flex-end; margin-top: 0.75rem;">
        <p style="margin: 0 0 0.25rem 0; font-size: 0.85rem; color: #aaa;">
            If you found this helpful, consider donating – it's not free to run!
        </p>
        <img src="{qr_base64}" width="135" style="display: block;" />
    </div>
    """,
    unsafe_allow_html=True
)
