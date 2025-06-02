import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Email Tone Adjuster", layout="centered")

st.title("✉️ Email Tone Adjuster")
st.write("Paste your email and choose a tone to rewrite it.")

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
        # Placeholder for rewritten result
        headers = {
          "Authorization": f"Bearer {groq_api_key}",
          "Content-Type": "application/json"
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
          rewritten = response.json()["choices"][0]["message"]["content"]
        st.success("✅ Rewritten Email:")
        st.write(rewritten)
        else:
        st.error("❌ Failed to get a response from API.")






      
