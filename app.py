import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Bingo & Gogo Pizza Bot", page_icon="🍕")
st.title("🍕 Bingo & Gogo Pizza Assistant")

# Safely fetch API key from secrets or environment
api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("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"))

if not api_key:
    st.error("⚠️ GROQ_API_KEY is missing! Please add it to your Streamlit App Secrets.")
    st.stop()

client = Groq(api_key=api_key)

KNOWLEDGE_BASE = """
Bingo & Gogo Pizza Knowledge Base:
- Location: 742 Evergreen Terrace, Springfield, OR
- Phone: (555) 839-7499
- Hours: Mon-Thurs 11am-10pm, Fri-Sat 11am-11:30pm, Sun 12pm-9:30pm
- Delivery: 5-mile radius. $15 minimum order. $3.99 fee (0-3 mi), $5.99 fee (3-5 mi).
- Gluten-Free: Available in 10" Small crust (+ $3.00).
- Halal: All chicken toppings (grilled chicken & wings) are Halal certified.
- Top Pizza: The Bingo Supreme ($14.99 S / $19.99 M / $24.99 L).
"""

SYSTEM_PROMPT = f"""
You are the official AI Assistant for Bingo & Gogo Pizza.

CONTEXT:
{KNOWLEDGE_BASE}

RULES:
1. Answer ONLY using the CONTEXT above.
2. If the answer is not in the context, say: "I don't have that detail. Please call us at (555) 839-7499."
3. Refuse any questions unrelated to Bingo & Gogo Pizza.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about menu, hours, or delivery..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Standard fast model ID
            messages=api_messages,
            temperature=0.1
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
            
    except Exception as e:
        st.error(f"Error connecting to Groq: {e}")
