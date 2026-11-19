import os
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bingo & Gogo Pizza Shop",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Credentials from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", "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"))
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "bingo123")

if not GROQ_API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Missing credentials! Add GROQ_API_KEY, SUPABASE_URL, and SUPABASE_KEY in Streamlit Cloud → Settings → Secrets.")
    st.stop()

# Load Optional Markdown Policy Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ops_path = os.path.join(BASE_DIR, "operations.md")
pol_path = os.path.join(BASE_DIR, "policies.md")
OPS_TEXT = open(ops_path, "r", encoding="utf-8").read() if os.path.exists(ops_path) else (
    "Active Offer: 20% OFF on all Pizzas (Code: BINGO20). Store Hours: 11:00 AM - 11:00 PM daily. "
    "Free delivery within 5 km on orders above ₹299. Phone: (555) 839-7499."
)
POL_TEXT = open(pol_path, "r", encoding="utf-8").read() if os.path.exists(pol_path) else (
    "Separate preparation counters for Veg and Non-Veg pizzas. Orders can be canceled within 5 minutes."
)

# Remove Streamlit's default header, toolbar, and margins so the website fills 100% of the screen
st.markdown("""
<style>
    #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        overflow-x: hidden;
    }
    iframe {
        display: block;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

config_json = json.dumps({
    "GROQ_API_KEY": GROQ_API_KEY,
    "SUPABASE_URL": SUPABASE_URL.rstrip("/"),
    "SUPABASE_KEY": SUPABASE_KEY,
    "ADMIN_PASSWORD": ADMIN_PASSWORD,
    "OPS_TEXT": OPS_TEXT,
    "POL_TEXT": POL_TEXT
})

HTML_WEBSITE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Bingo & Gogo Pizza Shop</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
  window.APP_CONFIG = __APP_CONFIG__;
</script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }
  body { background: #FFFFFF; color: #1E1E1E; overflow-x: hidden; }

  /* Top Header */
  .top-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 48px; background: #FFFFFF; gap: 20px; flex-wrap: wrap;
  }
  .logo-wrap { display: flex; align-items: center; gap: 10px; cursor: pointer; }
  .logo-icon { font-size: 40px; line-height: 1; }
  .logo-title { color: #C8102E; font-size: 26px; font-weight: 800; line-height: 1.05; }
  .logo-sub { color: #222; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-align: center; }

  .search-box {
    flex: 1; max-width: 440px; position: relative;
  }
  .search-box input {
    width: 100%; padding: 10px 18px 10px 42px; border-radius: 30px;
    border: 1px solid #DCDCDC; font-size: 14px; outline: none; background: #FAFAFA;
  }
  .search-box input:focus { border-color: #C8102E; background: #FFF; }
  .search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #777; }

  .header-actions { display: flex; align-items: center; gap: 16px; }
  .cart-btn {
    position: relative; background: none; border: none; font-size: 24px; cursor: pointer; padding: 4px;
  }
  .cart-badge {
    position: absolute; top: -4px; right: -6px; background: #C8102E; color: #FFF;
    font-size: 11px; font-weight: 700; width: 20px; height: 20px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }
  .btn-admin {
    background: #FFF0F0; color: #C8102E; border: 1px solid #F3C2C2;
    padding: 8px 15px; border-radius: 25px; font-size: 13px; font-weight: 600; cursor: pointer;
  }
  .btn-login {
    background: #C8102E; color: #FFF; border: none; padding: 9px 20px;
    border-radius: 25px; font-size: 13px; font-weight: 600; cursor: pointer;
  }

  /* Red Navigation Bar */
  .nav-bar {
    background: #C8102E; display: flex; justify-content: center; gap: 42px; padding: 11px 20px;
  }
  .nav-bar a {
    color: #FFF; text-decoration: none; font-size: 15px; font-weight: 600; padding-bottom: 2px;
  }
  .nav-bar a.active { border-bottom: 2px solid #FFF; }

  /* Hero Section */
  .hero {
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(90deg, #FFFDF9 0%, #F7ECE1 100%);
    padding: 36px 64px; gap: 30px; position: relative;
  }
  .hero-left { max-width: 520px; }
  .hero-left h1 { color: #C8102E; font-size: 50px; font-weight: 800; line-height: 1.08; }
  .hero-left h2 { color: #1E1E1E; font-size: 44px; font-weight: 800; line-height: 1.12; margin-bottom: 10px; }
  .hero-left p { color: #444; font-size: 19px; font-weight: 500; margin-bottom: 24px; }
  .btn-primary {
    background: #C8102E; color: #FFF; border: none; padding: 12px 28px;
    border-radius: 30px; font-size: 15px; font-weight: 700; cursor: pointer;
    box-shadow: 0 4px 12px rgba(200,16,46,0.28); text-decoration: none; display: inline-block;
  }
  .btn-primary:hover { background: #A80C24; }
  .hero-right img {
    width: 500px; max-width: 100%; height: 290px; object-fit: cover;
    border-radius: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.12);
  }
  .hero-dots {
    position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px;
  }
  .dot { width: 10px; height: 10px; border-radius: 50%; background: #D8C7BE; }
  .dot.active { background: #C8102E; }

  /* Category Circles */
  .categories {
    display: flex; justify-content: center; gap: 56px; padding: 32px 20px 14px; flex-wrap: wrap;
  }
  .cat-item { text-align: center; cursor: pointer; transition: transform 0.2s; }
  .cat-item:hover { transform: translateY(-4px); }
  .cat-circle {
    width: 78px; height: 78px; border-radius: 50%; background: #FCEEEE;
    display: flex; align-items: center; justify-content: center; font-size: 34px;
    margin: 0 auto 8px; border: 2px solid transparent;
  }
  .cat-item.active .cat-circle { border-color: #C8102E; background: #FADBD8; }
  .cat-label { font-size: 14px; font-weight: 700; color: #222; }

  /* Popular Pizzas Section */
  .section-wrap { max-width: 1180px; margin: 0 auto; padding: 16px 24px 36px; }
  .section-title { text-align: center; font-size: 26px; font-weight: 800; margin-bottom: 22px; color: #1E1E1E; }
  .pizza-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px;
  }
  @media (max-width: 980px) { .pizza-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 560px) { .pizza-grid { grid-template-columns: 1fr; } }

  .pizza-card {
    background: #FFF; border: 1px solid #ECECEC; border-radius: 16px; padding: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;
  }
  .pizza-card img {
    width: 100%; height: 155px; object-fit: cover; border-radius: 12px; margin-bottom: 12px;
  }
  .pizza-name { font-size: 16px; font-weight: 700; color: #1E1E1E; margin-bottom: 4px; }
  .pizza-desc { font-size: 12px; color: #666; margin-bottom: 12px; line-height: 1.4; }
  .card-bottom { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
  .pizza-price { font-size: 19px; font-weight: 800; color: #C8102E; }
  .btn-add {
    background: #C8102E; color: #FFF; border: none; padding: 7px 15px;
    border-radius: 20px; font-size: 12px; font-weight: 700; cursor: pointer;
  }
  .btn-add:hover { background: #A50C24; }

  /* Offer Banner */
  .offer-banner {
    max-width: 1130px; margin: 0 auto 50px; background: #FCE8E8; border-radius: 16px;
    padding: 16px 32px; display: flex; align-items: center; justify-content: space-between;
    border: 1px solid #F5C6CB; flex-wrap: wrap; gap: 16px;
  }
  .offer-left { display: flex; align-items: center; gap: 18px; }
  .badge-20 {
    background: #C8102E; color: #FFF; font-weight: 800; font-size: 14px;
    width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; text-align: center; line-height: 1.1;
  }
  .offer-title { color: #C8102E; font-size: 24px; font-weight: 800; }
  .offer-div { width: 2px; height: 30px; background: #DFB3B3; }
  .offer-text { font-size: 16px; font-weight: 600; color: #222; }

  /* Floating Chatbot Widget (Matches Mockup Bottom-Right) */
  .chat-widget {
    position: fixed; bottom: 20px; right: 24px; width: 340px; background: #FFF;
    border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    border: 1px solid #E5E5E5; z-index: 999; overflow: hidden;
  }
  .chat-header {
    background: #C8102E; color: #FFF; padding: 12px 16px; display: flex;
    align-items: center; justify-content: space-between; font-weight: 700; font-size: 14px;
  }
  .chat-controls span { cursor: pointer; margin-left: 12px; font-size: 15px; }
  .chat-body {
    height: 270px; overflow-y: auto; padding: 14px; background: #FAFAFA;
    display: flex; flex-direction: column; gap: 10px;
  }
  .msg-row { display: flex; align-items: flex-start; gap: 8px; }
  .msg-row.user { justify-content: flex-end; }
  .bot-avatar {
    width: 32px; height: 32px; border-radius: 50%; background: #EBF5FB;
    display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
  }
  .msg-bubble {
    padding: 9px 13px; border-radius: 14px; font-size: 12.5px; line-height: 1.45; max-width: 240px;
  }
  .msg-row.bot .msg-bubble { background: #FFF; border: 1px solid #E6E6E6; color: #222; }
  .msg-row.user .msg-bubble { background: #C8102E; color: #FFF; }

  .quick-chips {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 6px;
    padding: 8px 12px; background: #FAFAFA; border-top: 1px solid #EEE;
  }
  .chip {
    background: #FFF; border: 1px solid #D98880; color: #922B21; border-radius: 20px;
    padding: 4px 12px; font-size: 11.5px; font-weight: 600; cursor: pointer;
  }
  .chip:hover { background: #FDEDEC; }

  .chat-input-wrap {
    display: flex; align-items: center; padding: 10px 12px; background: #FFF;
    border-top: 1px solid #EAEAEA; gap: 8px;
  }
  .chat-input-wrap input {
    flex: 1; border: 1px solid #DDD; border-radius: 20px; padding: 8px 14px; font-size: 12.5px; outline: none;
  }
  .send-btn {
    width: 34px; height: 34px; border-radius: 50%; background: #C8102E; color: #FFF;
    border: none; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center;
  }
  .chat-launcher {
    position: fixed; bottom: 20px; right: 24px; background: #C8102E; color: #FFF;
    border: none; border-radius: 30px; padding: 12px 20px; font-weight: 700;
    box-shadow: 0 6px 20px rgba(200,16,46,0.35); cursor: pointer; display: none; z-index: 999;
  }

  /* Modals (Cart & Admin) */
  .modal-backdrop {
    position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: none;
    align-items: center; justify-content: center; z-index: 1000;
  }
  .modal-card {
    background: #FFF; width: 440px; max-width: 92vw; border-radius: 16px;
    padding: 24px; max-height: 85vh; overflow-y: auto;
  }
  .modal-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  .modal-head h3 { color: #C8102E; font-size: 20px; font-weight: 800; }
  .form-group { margin-bottom: 12px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 4px; }
  .form-group input, .form-group select {
    width: 100%; padding: 8px 12px; border: 1px solid #CCC; border-radius: 8px; font-size: 13px;
  }
  .toast {
    position: fixed; top: 20px; right: 24px; background: #1E8449; color: #FFF;
    padding: 10px 18px; border-radius: 10px; font-size: 13px; font-weight: 600;
    display: none; z-index: 1100; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
</style>
</head>
<body>

<div id="toast" class="toast"></div>

<!-- Top Header -->
<header class="top-header">
  <div class="logo-wrap" onclick="filterCategory('All')">
    <div class="logo-icon">🍕</div>
    <div>
      <div class="logo-title">Bingo &amp; Gogo</div>
      <div class="logo-sub">— Pizza Shop —</div>
    </div>
  </div>

  <div class="search-box">
    <span class="search-icon">🔍</span>
    <input type="text" id="searchInput" placeholder="Search for pizzas..." oninput="renderMenu()" />
  </div>

  <div class="header-actions">
    <button class="cart-btn" onclick="openModal('cartModal')">
      🛒 <span class="cart-badge" id="cartBadge">0</span>
    </button>
    <button class="btn-admin" onclick="openModal('adminModal')">⚙️ Store Admin</button>
    <button class="btn-login" onclick="showToast('Welcome to Bingo & Gogo Pizza!')">👤 Login / Register</button>
  </div>
</header>

<!-- Navigation Bar -->
<nav class="nav-bar">
  <a href="#" class="active" onclick="filterCategory('All')">Home</a>
  <a href="#popularSection">Menu</a>
  <a href="#offerSection">Offers</a>
  <a href="#offerSection">About Us</a>
  <a href="#offerSection">Contact</a>
</nav>

<!-- Hero Banner -->
<section class="hero">
  <div class="hero-left">
    <h1>Bingo &amp; Gogo</h1>
    <h2>Delicious Pizza!</h2>
    <p>Good Food. Great Mood.</p>
    <a href="#popularSection" class="btn-primary">Order Now →</a>
  </div>
  <div class="hero-right">
    <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800" alt="Delicious Pizza" />
  </div>
  <div class="hero-dots">
    <span class="dot active"></span>
    <span class="dot"></span>
    <span class="dot"></span>
  </div>
</section>

<!-- Category Icons -->
<section class="categories">
  <div class="cat-item" id="cat-Veg Pizzas" onclick="toggleCategory('Veg Pizzas')">
    <div class="cat-circle">🌿</div>
    <div class="cat-label">Veg Pizzas</div>
  </div>
  <div class="cat-item" id="cat-Non-Veg Pizzas" onclick="toggleCategory('Non-Veg Pizzas')">
    <div class="cat-circle">🍗</div>
    <div class="cat-label">Non-Veg Pizzas</div>
  </div>
  <div class="cat-item" id="cat-Cheese Pizzas" onclick="toggleCategory('Cheese Pizzas')">
    <div class="cat-circle">🧀</div>
    <div class="cat-label">Cheese Pizzas</div>
  </div>
  <div class="cat-item" id="cat-Special Pizzas" onclick="toggleCategory('Special Pizzas')">
    <div class="cat-circle">⭐</div>
    <div class="cat-label">Special Pizzas</div>
  </div>
</section>

<!-- Live Menu Grid -->
<section class="section-wrap" id="popularSection">
  <h2 class="section-title">Our Popular Pizzas</h2>
  <div class="pizza-grid" id="pizzaGrid">
    <p style="grid-column:1/-1; text-align:center; color:#666;">Loading live menu from Supabase...</p>
  </div>
</section>

<!-- Promotional Offer Strip -->
<section class="offer-banner" id="offerSection">
  <div class="offer-left">
    <div class="badge-20">20%<br>OFF</div>
    <div class="offer-title">Special Offer!</div>
    <div class="offer-div"></div>
    <div class="offer-text">Get 20% OFF on all Pizzas!</div>
  </div>
  <a href="#popularSection" class="btn-primary">Order Now →</a>
</section>

<!-- Floating Chatbot Widget -->
<button class="chat-launcher" id="chatLauncher" onclick="toggleChat(true)">🍕 Bingo &amp; Gogo Assistant</button>

<div class="chat-widget" id="chatWidget">
  <div class="chat-header">
    <span>🍕 Bingo &amp; Gogo Assistant</span>
    <div class="chat-controls">
      <span onclick="toggleChat(false)">—</span>
      <span onclick="toggleChat(false)">✕</span>
    </div>
  </div>
  <div class="chat-body" id="chatBody">
    <div class="msg-row bot">
      <div class="bot-avatar">🤖</div>
      <div class="msg-bubble">Hello! Welcome to Bingo &amp; Gogo Pizza! How can I help you?</div>
    </div>
  </div>
  <div class="quick-chips">
    <button class="chip" onclick="sendQuick('Show Menu')">Show Menu</button>
    <button class="chip" onclick="sendQuick('Check Offers')">Check Offers</button>
    <button class="chip" onclick="sendQuick('Track Order')">Track Order</button>
  </div>
  <div class="chat-input-wrap">
    <input type="text" id="chatInput" placeholder="Type a message..." onkeydown="if(event.key==='Enter') sendMessage()" />
    <button class="send-btn" onclick="sendMessage()">➤</button>
  </div>
</div>

<!-- Cart Modal -->
<div class="modal-backdrop" id="cartModal">
  <div class="modal-card">
    <div class="modal-head">
      <h3>🛒 Your Cart</h3>
      <button onclick="closeModal('cartModal')" style="border:none;background:none;font-size:20px;cursor:pointer;">✕</button>
    </div>
    <div id="cartItemsList"></div>
    <div style="margin-top:14px; display:flex; gap:8px;">
      <input type="text" id="promoInput" placeholder="Promo code (e.g. BINGO20)" style="flex:1;padding:8px;border:1px solid #CCC;border-radius:8px;" />
      <button class="btn-add" onclick="applyPromo()">Apply</button>
    </div>
    <div id="cartTotalBox" style="margin-top:14px; font-weight:700; font-size:16px;"></div>
    <button class="btn-primary" style="width:100%; margin-top:14px; text-align:center;" onclick="placeOrder()">Place Order</button>
  </div>
</div>

<!-- Zero-Code SQL Admin Modal -->
<div class="modal-backdrop" id="adminModal">
  <div class="modal-card">
    <div class="modal-head">
      <h3>⚙️ Store Admin (Live SQL)</h3>
      <button onclick="closeModal('adminModal')" style="border:none;background:none;font-size:20px;cursor:pointer;">✕</button>
    </div>
    <div id="adminLoginBox">
      <div class="form-group">
        <label>Admin Password</label>
        <input type="password" id="adminPwdInput" placeholder="Enter admin password" />
      </div>
      <button class="btn-primary" style="width:100%;" onclick="unlockAdmin()">Unlock Database</button>
    </div>
    <div id="adminPanelBox" style="display:none;">
      <h4 style="margin-bottom:10px; color:#1E8449;">➕ Add New Pizza to Supabase</h4>
      <div class="form-group">
        <label>Category</label>
        <select id="newCat">
          <option>Veg Pizzas</option>
          <option>Non-Veg Pizzas</option>
          <option>Cheese Pizzas</option>
          <option>Special Pizzas</option>
        </select>
      </div>
      <div class="form-group"><label>Pizza Name</label><input id="newName" placeholder="e.g. Paneer Makhani Pizza" /></div>
      <div class="form-group"><label>Price (₹)</label><input id="newPrice" placeholder="e.g. ₹269" /></div>
      <div class="form-group"><label>Description</label><input id="newDesc" placeholder="Toppings & crust details" /></div>
      <div class="form-group"><label>Image URL</label><input id="newImg" value="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500" /></div>
      <button class="btn-primary" style="width:100%; margin-bottom:18px;" onclick="addPizzaToDB()">Save to SQL Database</button>

      <h4 style="margin-bottom:8px; color:#C8102E;">🗑️ Delete Pizza from Supabase</h4>
      <div id="adminDeleteList"></div>
    </div>
  </div>
</div>

<script>
  const CFG = window.APP_CONFIG;
  let menuItems = [];
  let activeCategory = "All";
  let cart = [];
  let discountApplied = false;
  let lastOrderId = null;
  let chatHistory = [];

  function showToast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.style.display = "block";
    setTimeout(() => { t.style.display = "none"; }, 3000);
  }

  // Fetch live menu rows directly from Supabase REST API
  async function fetchLiveMenu() {
    try {
      const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/menu_items?select=*&order=id.asc`, {
        headers: {
          "apikey": CFG.SUPABASE_KEY,
          "Authorization": `Bearer ${CFG.SUPABASE_KEY}`
        }
      });
      if (res.ok) {
        menuItems = await res.json();
        renderMenu();
        renderAdminDeleteList();
      }
    } catch (err) {
      console.error("Supabase fetch error:", err);
    }
    return menuItems;
  }

  function toggleCategory(cat) {
    activeCategory = (activeCategory === cat) ? "All" : cat;
    document.querySelectorAll(".cat-item").forEach(el => el.classList.remove("active"));
    if (activeCategory !== "All") {
      const activeEl = document.getElementById("cat-" + activeCategory);
      if (activeEl) activeEl.classList.add("active");
    }
    renderMenu();
  }

  function filterCategory(cat) {
    activeCategory = cat;
    document.querySelectorAll(".cat-item").forEach(el => el.classList.remove("active"));
    renderMenu();
  }

  function renderMenu() {
    const grid = document.getElementById("pizzaGrid");
    const q = document.getElementById("searchInput").value.toLowerCase().trim();
    const filtered = menuItems.filter(item => {
      const matchCat = activeCategory === "All" || item.category === activeCategory;
      const matchText = !q || item.name.toLowerCase().includes(q) || (item.description || "").toLowerCase().includes(q);
      return matchCat && matchText;
    });

    if (!filtered.length) {
      grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:#666;">No pizzas found. Check Supabase RLS permissions or add pizzas via Store Admin.</p>`;
      return;
    }

    grid.innerHTML = filtered.map(item => `
      <div class="pizza-card">
        <div>
          <img src="${item.image_url || 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500'}" alt="${item.name}" />
          <div class="pizza-name">${item.name}</div>
          <div class="pizza-desc">${item.description || ''}</div>
        </div>
        <div class="card-bottom">
          <span class="pizza-price">${item.pricing}</span>
          <button class="btn-add" onclick="addToCart(${item.id})">Add to Cart</button>
        </div>
      </div>
    `).join("");
  }

  function parsePrice(str) {
    const num = parseFloat(String(str).replace(/[^0-9.]/g, ""));
    return isNaN(num) ? 0 : num;
  }

  function addToCart(id) {
    const found = menuItems.find(i => i.id === id);
    if (found) {
      cart.push(found);
      document.getElementById("cartBadge").textContent = cart.length;
      showToast(`Added ${found.name} to cart!`);
    }
  }

  function renderCart() {
    const list = document.getElementById("cartItemsList");
    const totalBox = document.getElementById("cartTotalBox");
    if (!cart.length) {
      list.innerHTML = `<p style="color:#666;font-size:13px;">Your cart is empty.</p>`;
      totalBox.textContent = "";
      return;
    }
    let subtotal = 0;
    list.innerHTML = cart.map((item, idx) => {
      subtotal += parsePrice(item.pricing);
      return `<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #EEE;font-size:13px;">
        <span>${item.name}</span>
        <span><b>${item.pricing}</b> <a href="#" onclick="removeCart(${idx});return false;" style="color:#C8102E;margin-left:6px;">✕</a></span>
      </div>`;
    }).join("");
    const finalTotal = discountApplied ? Math.round(subtotal * 0.8) : subtotal;
    totalBox.innerHTML = discountApplied
      ? `Subtotal: ₹${subtotal} → <span style="color:#1E8449;">20% OFF Applied: ₹${finalTotal}</span>`
      : `Total: ₹${finalTotal}`;
  }

  function removeCart(idx) {
    cart.splice(idx, 1);
    document.getElementById("cartBadge").textContent = cart.length;
    renderCart();
  }

  function applyPromo() {
    const code = document.getElementById("promoInput").value.trim().toUpperCase();
    if (code === "BINGO20") {
      discountApplied = true;
      renderCart();
      showToast("20% OFF Promo Applied!");
    } else {
      showToast("Use code BINGO20 for 20% OFF");
    }
  }

  function placeOrder() {
    if (!cart.length) return;
    lastOrderId = "BG-" + Math.floor(1000 + Math.random() * 9000);
    cart = [];
    discountApplied = false;
    document.getElementById("cartBadge").textContent = "0";
    closeModal("cartModal");
    showToast(`Order ${lastOrderId} confirmed! Baking fresh now.`);
  }

  function openModal(id) {
    if (id === "cartModal") renderCart();
    document.getElementById(id).style.display = "flex";
  }
  function closeModal(id) { document.getElementById(id).style.display = "none"; }

  function unlockAdmin() {
    if (document.getElementById("adminPwdInput").value === CFG.ADMIN_PASSWORD) {
      document.getElementById("adminLoginBox").style.display = "none";
      document.getElementById("adminPanelBox").style.display = "block";
      renderAdminDeleteList();
    } else {
      showToast("Incorrect Admin Password");
    }
  }

  async function addPizzaToDB() {
    const payload = {
      category: document.getElementById("newCat").value,
      name: document.getElementById("newName").value.trim(),
      pricing: document.getElementById("newPrice").value.trim(),
      description: document.getElementById("newDesc").value.trim(),
      image_url: document.getElementById("newImg").value.trim(),
      dietary_info: "Freshly Prepared"
    };
    if (!payload.name || !payload.pricing) return;

    const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/menu_items`, {
      method: "POST",
      headers: {
        "apikey": CFG.SUPABASE_KEY,
        "Authorization": `Bearer ${CFG.SUPABASE_KEY}`,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
      },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      document.getElementById("newName").value = "";
      document.getElementById("newPrice").value = "";
      document.getElementById("newDesc").value = "";
      await fetchLiveMenu();
      showToast(`Added ${payload.name} to Supabase!`);
    }
  }

  function renderAdminDeleteList() {
    const box = document.getElementById("adminDeleteList");
    if (!box) return;
    box.innerHTML = menuItems.map(item => `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #EEE;font-size:13px;">
        <span>${item.name} (${item.pricing})</span>
        <button class="btn-add" onclick="deletePizzaFromDB(${item.id})">Delete</button>
      </div>
    `).join("");
  }

  async function deletePizzaFromDB(id) {
    await fetch(`${CFG.SUPABASE_URL}/rest/v1/menu_items?id=eq.${id}`, {
      method: "DELETE",
      headers: {
        "apikey": CFG.SUPABASE_KEY,
        "Authorization": `Bearer ${CFG.SUPABASE_KEY}`
      }
    });
    await fetchLiveMenu();
    showToast("Deleted from Supabase!");
  }

  function toggleChat(show) {
    document.getElementById("chatWidget").style.display = show ? "block" : "none";
    document.getElementById("chatLauncher").style.display = show ? "none" : "block";
  }

  function appendChat(role, text) {
    const body = document.getElementById("chatBody");
    const row = document.createElement("div");
    row.className = `msg-row ${role}`;
    row.innerHTML = role === "bot"
      ? `<div class="bot-avatar">🤖</div><div class="msg-bubble">${text.replace(/\n/g, "<br>")}</div>`
      : `<div class="msg-bubble">${text}</div>`;
    body.appendChild(row);
    body.scrollTop = body.scrollHeight;
  }

  function sendQuick(text) {
    document.getElementById("chatInput").value = text;
    sendMessage();
  }

  async function sendMessage() {
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    appendChat("user", text);
    chatHistory.push({ role: "user", content: text });

    // Query fresh Supabase data right at the moment the message is sent
    const freshMenu = await fetchLiveMenu();
    const menuContext = freshMenu.map(i => `- ${i.name} (${i.category}): ${i.pricing} — ${i.description || ''}`).join("\n");

    const systemPrompt = `You are the friendly AI Assistant for Bingo & Gogo Pizza Shop.
LIVE MENU FROM SUPABASE:
${menuContext}

OPERATIONS & OFFERS:
${CFG.OPS_TEXT}

POLICIES:
${CFG.POL_TEXT}

ACTIVE CUSTOMER ORDER ID: ${lastOrderId || "None placed yet in this session"}

RULES:
1. Answer concisely using ONLY the live menu, offers, and policies above.
2. Always format prices in Rupees (₹).
3. If asked to track an order and an Active Order ID exists, confirm it is being freshly baked and will arrive within 30 minutes.`;

    try {
      const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${CFG.GROQ_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "openai/gpt-oss-20b",
          messages: [{ role: "system", content: systemPrompt }, ...chatHistory],
          temperature: 0.2
        })
      });
      const data = await res.json();
      const reply = data.choices?.[0]?.message?.content || "Please call us at (555) 839-7499 for assistance.";
      chatHistory.push({ role: "assistant", content: reply });
      appendChat("bot", reply);
    } catch (e) {
      appendChat("bot", "Unable to reach AI right now. Please try again.");
    }
  }

  // Initial load from Supabase
  fetchLiveMenu();
</script>
</body>
</html>
"""

final_html = HTML_WEBSITE.replace("__APP_CONFIG__", config_json)
components.html(final_html, height=1000, scrolling=True)
