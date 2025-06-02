import streamlit as st
import requests

# 🔑 Just paste your Groq API key between the quotes below
groq_api_key = "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"

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

        headers = {
            "Authorization": groq_api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an assistant that rewrites emails in a {selected_tone.lower()} tone."
                },
                {
                    "role": "user",
                    "content": email_input
                }
            ],
            "model": "mixtral-8x7b-32768"
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            rewritten = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Rewritten Email:")
            st.write(rewritten)
        else:
            st.error(f"❌ Groq error: {response.status_code} - {response.text}")
