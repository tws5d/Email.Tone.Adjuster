import streamlit as st
import requests

# ✅ Load API key securely from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Email Tone Adjuster", layout="centered")

# Create three columns: left for title, middle for message, right for QR code
col1, col_msg, col2 = st.columns([4, 1.5, 1])

with col1:
    st.title("✉️ Email Tone Adjuster")
    st.write("Paste your email and choose a tone to rewrite it.")

with col_msg:
    st.markdown(
        "<p style='font-size: 0.85rem; color: gray; margin-top: 115px; text-align: center;'>"
        "☕ Enjoying the app?<br>Help support it.</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("tipjar_qr.png", width=140)

email_input = st.text_area("📨 Your Email", height=200)

tone_options = [
    "Polite", "Confident", "Formal", "Informal", "Concise",
    "Apologetic", "Appreciative", "Supportive", "Neutral", "Direct",
    "Empathetic", "Sympathetic", "Understanding", "Encouraging", "Positive"
]

selected_tone = st.selectbox("🎯 Choose a Tone", tone_options)

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
            "model": "gpt-3.5-turbo",  # or "gpt-4" if you have access
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
