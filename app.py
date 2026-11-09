import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Bingo & Gogo Pizza Bot", page_icon="🍕")
st.title("🍕 Bingo & Gogo Pizza Assistant")

# Fetch API key
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("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"))

if not api_key:
    st.error("⚠️ GROQ_API_KEY is missing! Please check Streamlit App Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Function to automatically read and merge all 3 Markdown files
def load_knowledge_base():
    files = ["menu.md", "operations.md", "policies.md"]
    combined_text = ""
    
    for filename in files:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                combined_text += file.read() + "\n\n"
        else:
            combined_text += f"\n[Warning: {filename} missing]\n"
            
    return combined_text

KNOWLEDGE_BASE = load_knowledge_base()

SYSTEM_PROMPT = f"""
You are the official AI Assistant for Bingo & Gogo Pizza.

CONTEXT:
{KNOWLEDGE_BASE}

RULES:
1. Answer strictly using ONLY the CONTEXT information provided above.
2. If an answer cannot be found in the context, say: "I don't have that detail right now. Please call us directly at (555) 839-7499."
3. Do not invent prices, hours, or items not listed in the context.
4. Refuse questions unrelated to Bingo & Gogo Pizza politely.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about our menu, hours, or policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=api_messages,
            temperature=0.1
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
            
    except Exception as e:
        st.error(f"Error connecting to Groq API: {e}")
