import os
import streamlit as st
from groq import Groq
from supabase import create_client, Client

st.set_page_config(page_title="Bingo & Gogo Pizza", page_icon="🍕", layout="wide")

# 1. Credentials Verification
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("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"))
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY"))
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "bingo123")

if not GROQ_API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Credentials missing! Ensure GROQ_API_KEY, SUPABASE_URL, and SUPABASE_KEY are configured in Secrets.")
    st.stop()

# Initialize API clients
client = Groq(api_key=GROQ_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Database Fetch Functions (Execute Live on Every Interaction)
def fetch_live_menu():
    """Queries Supabase Cloud DB live whenever called."""
    try:
        response = supabase.table("menu_items").select("*").order("id").execute()
        return response.data or []
    except Exception as e:
        st.error(f"Cloud DB Error: {e}")
        return []

def format_menu_for_llm(menu_rows):
    """Converts raw DB rows into formatted text for the LLM system prompt."""
    if not menu_rows:
        return "Menu data currently unavailable."
    
    text = "--- CLOUD DATABASE MENU ITEMS ---\n"
    current_cat = ""
    for item in menu_rows:
        cat = item.get("category", "General")
        name = item.get("name", "")
        pricing = item.get("pricing", "")
        desc = item.get("description", "")
        diet = item.get("dietary_info", "")
        
        if cat != current_cat:
            current_cat = cat
            text += f"\n### Category: {current_cat}\n"
        text += f"- **{name}**: {pricing}\n"
        if desc:
            text += f"  Description: {desc}\n"
        if diet and diet != "N/A":
            text += f"  Dietary: {diet}\n"
    return text

# Load static policy files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ops_file = os.path.join(BASE_DIR, "operations.md")
pol_file = os.path.join(BASE_DIR, "policies.md")
ops_text = open(ops_file, "r", encoding="utf-8").read() if os.path.exists(ops_file) else ""
pol_text = open(pol_file, "r", encoding="utf-8").read() if os.path.exists(pol_file) else ""

# 3. Sidebar Admin Control Panel (No-Code Database Updates)
with st.sidebar:
    st.header("⚙️ Store Admin")
    with st.expander("🔒 Menu Management Panel"):
        pwd = st.text_input("Admin Password", type="password")
        if pwd == ADMIN_PASSWORD:
            st.success("Authenticated")
            
            st.markdown("#### ➕ Add New Pizza / Item")
            with st.form("add_item_form", clear_on_submit=True):
                cat_input = st.selectbox("Category", ["Specialty Pizzas", "Sides & Appetizers", "Drinks & Desserts", "Crust Options"])
                name_input = st.text_input("Item Name")
                desc_input = st.text_area("Description")
                price_input = st.text_input("Pricing (e.g., Small: $14.99 | Large: $24.99)")
                diet_input = st.text_input("Dietary Info (e.g., Vegetarian, Halal)")
                submit_btn = st.form_submit_button("Save to Database")
                
                if submit_btn and name_input and price_input:
                    new_record = {
                        "category": cat_input,
                        "name": name_input,
                        "description": desc_input,
                        "pricing": price_input,
                        "dietary_info": diet_input
                    }
                    supabase.table("menu_items").insert(new_record).execute()
                    st.success(f"Added '{name_input}' directly to Cloud DB!")
                    st.rerun()

            st.markdown("#### 🗑️ Delete Existing Item")
            db_records = fetch_live_menu()
            if db_records:
                options_map = {f"{r['id']}: {r['name']} ({r['category']})": r['id'] for r in db_records}
                selected_label = st.selectbox("Select Item to Delete", list(options_map.keys()))
                if st.button("Delete Item"):
                    target_id = options_map[selected_label]
                    supabase.table("menu_items").delete().eq("id", target_id).execute()
                    st.warning("Deleted from Cloud DB!")
                    st.rerun()

# 4. Web Storefront UI
st.title("🍕 Bingo & Gogo Pizza")
st.caption("Handcrafted Pizzas & Halal Wings | 742 Evergreen Terrace, Springfield, OR")
st.divider()

col_menu, col_chatbot = st.columns([3, 2], gap="large")

# LEFT COLUMN: Dynamic Website Menu
with col_menu:
    st.subheader("📍 Store Information")
    st.markdown("""
    * **Phone:** (555) 839-7499
    * **Hours:** Mon–Thurs: 11:00 AM – 10:00 PM | Fri–Sat: 11:00 AM – 11:30 PM | Sun: 12:00 PM – 9:30 PM
    * **Delivery:** 5-mile radius ($15 minimum order)
    """)
    st.divider()

    st.subheader("📜 Live Store Menu")
    menu_data = fetch_live_menu()
    
    if not menu_data:
        st.info("No items found. Add items using the Admin Panel in the sidebar.")
    else:
        categories = list(dict.fromkeys([item["category"] for item in menu_data]))
        selected_category = st.selectbox("Filter Category", ["All"] + categories)
        
        for category in categories:
            if selected_category in ["All", category]:
                st.markdown(f"#### {category}")
                items = [i for i in menu_data if i["category"] == category]
                for item in items:
                    with st.container():
                        st.markdown(f"**{item['name']}** — `{item['pricing']}`")
                        if item.get("description"):
                            st.caption(item["description"])
                        if item.get("dietary_info") and item["dietary_info"] != "N/A":
                            st.caption(f"🌱 *{item['dietary_info']}*")
                        st.write("")

# RIGHT COLUMN: AI Chatbot Engine
with col_chatbot:
    st.subheader("🤖 AI Store Assistant")
    st.info("Ask about prices, dietary options, or store policies!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ON-DEMAND FETCH: Query DB right at the moment user sends prompt
        current_menu_data = fetch_live_menu()
        live_menu_context = format_menu_for_llm(current_menu_data)

        system_prompt = f"""
You are the official AI Assistant for Bingo & Gogo Pizza.

LIVE DATABASE MENU:
{live_menu_context}

OPERATIONS KNOWLEDGE:
{ops_text}

POLICIES KNOWLEDGE:
{pol_text}

RULES:
1. Answer questions strictly using the LIVE DATABASE MENU, OPERATIONS, and POLICIES data above.
2. If an answer cannot be found, state: "I don't have that detail right now. Please call us directly at (555) 839-7499."
3. Respond helpfully and politely to greetings.
"""

        api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

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
