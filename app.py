import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Bingo & Gogo Pizza Bot", page_icon="🍕", layout="wide")
st.title("🍕 Bingo & Gogo Pizza Assistant")

# Fetch API key
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("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"))

if not api_key:
    st.error("⚠️ GROQ_API_KEY is missing! Please check Streamlit App Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Get the exact directory where app.py resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_knowledge_base():
    files = ["menu.md", "operations.md", "policies.md"]
    combined_text = ""
    status_report = []
    
    for filename in files:
        # Construct absolute path to prevent container working directory mismatches
        filepath = os.path.join(BASE_DIR, filename)
        
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                combined_text += f"\n\n--- DOCUMENT: {filename} ---\n{content}"
                status_report.append(f"✅ Loaded {filename} ({len(content)} bytes)")
        else:
            combined_text += f"\n\n[WARNING: {filename} NOT FOUND]"
            status_report.append(f"❌ Missing {filename}")
            
    return combined_text, status_report

KNOWLEDGE_BASE, FILE_STATUS = load_knowledge_base()

# Sidebar for instant debugging
with st.sidebar:
    st.header("⚙️ Bot Diagnostics")
    st.subheader("File Status:")
    for status in FILE_STATUS:
        st.write(status)
    
    with st.expander("View Full Loaded Knowledge Base"):
        st.text_area("Context Sent to LLM", KNOWLEDGE_BASE, height=300)

SYSTEM_PROMPT = f"""
You are the helpful AI Assistant for Bingo & Gogo Pizza.

CONTEXT DATA:
{KNOWLEDGE_BASE}

INSTRUCTIONS:
1. Use the CONTEXT DATA above to answer user questions thoroughly.
2. If the user asks a question about Bingo & Gogo Pizza that is NOT in the context data, respond: "I don't have that specific detail right now. Please call us directly at (555) 839-7499."
3. If the user greets you or asks general conversational questions related to ordering pizza, respond warmly and guide them to the menu.
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
            temperature=0.2
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
            
    except Exception as e:
        st.error(f"Error connecting to Groq API: {e}")
