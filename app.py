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
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", "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"))
"))
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
    "Active Offers: 20% OFF on all Pizzas (Code: BINGO20). Free delivery within 5 km on orders above ₹299. "
    "Store Hours: 11:00 AM - 11:00 PM daily. Phone: (555) 839-7499."
)
POL_TEXT = open(pol_path, "r", encoding="utf-8").read() if os.path.exists(pol_path) else (
    "Separate preparation counters for Veg and Non-Veg pizzas. Orders can be canceled within 5 minutes."
)

# Strip Streamlit default padding & chrome for a full-screen website
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
  body { background: #FFFFFF; color: #1E1E1E; overflow-x: hidden; display: flex; flex-direction: column; min-height: 100vh; }

  /* Top Header */
  .top-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 48px; background: #FFFFFF; gap: 20px; flex-wrap: wrap;
  }
  .logo-wrap { display: flex; align-items: center; gap: 10px; cursor: pointer; }
  .logo-icon { font-size: 40px; line-height: 1; }
  .logo-title { color: #C8102E; font-size: 26px; font-weight: 800; line-height: 1.05; }
  .logo-sub { color: #222; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-align: center; }

  .search-box { flex: 1; max-width: 440px; position: relative; }
  .search-box input {
    width: 100%; padding: 10px 18px 10px 42px; border-radius: 30px;
    border: 1px solid #DCDCDC; font-size: 14px; outline: none; background: #FAFAFA;
  }
  .search-box input:focus { border-color: #C8102E; background: #FFF; }
  .search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #777; }

  .header-actions { display: flex; align-items: center; gap: 16px; }
  .cart-btn { position: relative; background: none; border: none; font-size: 24px; cursor: pointer; padding: 4px; }
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
    background: #C8102E; display: flex; justify-content: center; gap: 42px; padding: 11px 20px; flex-wrap: wrap;
  }
  .nav-bar a {
    color: #FFF; text-decoration: none; font-size: 15px; font-weight: 600;
    padding-bottom: 3px; border-bottom: 2px solid transparent; cursor: pointer; transition: 0.2s;
  }
  .nav-bar a:hover, .nav-bar a.active { border-bottom: 2px solid #FFF; }

  /* Page Visibility Switching */
  .page-view { display: none; flex: 1; }
  .page-view.active { display: block; animation: fadeIn 0.2s ease-in; }
  @keyframes fadeIn { from { opacity: 0.6; } to { opacity: 1; } }

  /* Shared Buttons & Section Containers */
  .btn-primary {
    background: #C8102E; color: #FFF; border: none; padding: 12px 28px;
    border-radius: 30px; font-size: 15px; font-weight: 700; cursor: pointer;
    box-shadow: 0 4px 12px rgba(200,16,46,0.28); text-decoration: none; display: inline-block;
  }
  .btn-primary:hover { background: #A80C24; }
  .section-wrap { max-width: 1180px; margin: 0 auto; padding: 28px 24px 44px; }
  .section-title { text-align: center; font-size: 28px; font-weight: 800; margin-bottom: 8px; color: #1E1E1E; }
  .section-sub { text-align: center; font-size: 14px; color: #666; margin-bottom: 26px; }

  /* Page Banner Header for Inner Pages */
  .inner-banner {
    background: linear-gradient(90deg, #FFFDF9 0%, #F7ECE1 100%);
    padding: 34px 24px; text-align: center; border-bottom: 1px solid #EFE4D8;
  }
  .inner-banner h1 { color: #C8102E; font-size: 36px; font-weight: 800; }
  .inner-banner p { color: #555; font-size: 15px; margin-top: 6px; }

  /* HOME PAGE: Hero */
  .hero {
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(90deg, #FFFDF9 0%, #F7ECE1 100%);
    padding: 36px 64px; gap: 30px; position: relative;
  }
  .hero-left { max-width: 520px; }
  .hero-left h1 { color: #C8102E; font-size: 50px; font-weight: 800; line-height: 1.08; }
  .hero-left h2 { color: #1E1E1E; font-size: 44px; font-weight: 800; line-height: 1.12; margin-bottom: 10px; }
  .hero-left p { color: #444; font-size: 19px; font-weight: 500; margin-bottom: 24px; }
  .hero-right img {
    width: 500px; max-width: 100%; height: 290px; object-fit: cover;
    border-radius: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.12);
  }
  .hero-dots { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; background: #D8C7BE; }
  .dot.active { background: #C8102E; }

  /* Category Circles */
  .categories {
    display: flex; justify-content: center; gap: 48px; padding: 32px 20px 10px; flex-wrap: wrap;
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

  /* Filter Pills on Menu Page */
  .filter-pills { display: flex; justify-content: center; gap: 10px; margin-bottom: 26px; flex-wrap: wrap; }
  .pill-tab {
    padding: 8px 20px; border-radius: 25px; border: 1px solid #DDD;
    background: #FFF; font-size: 13px; font-weight: 600; cursor: pointer; color: #333;
  }
  .pill-tab.active, .pill-tab:hover { background: #C8102E; color: #FFF; border-color: #C8102E; }

  /* Pizza Cards Grid */
  .pizza-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
  @media (max-width: 980px) { .pizza-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 560px) { .pizza-grid { grid-template-columns: 1fr; } }

  .pizza-card {
    background: #FFF; border: 1px solid #ECECEC; border-radius: 16px; padding: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;
  }
  .pizza-card img { width: 100%; height: 155px; object-fit: cover; border-radius: 12px; margin-bottom: 10px; }
  .cat-tag {
    display: inline-block; font-size: 10px; font-weight: 700; color: #C8102E;
    background: #FDEDEC; padding: 2px 8px; border-radius: 10px; margin-bottom: 6px;
  }
  .pizza-name { font-size: 16px; font-weight: 700; color: #1E1E1E; margin-bottom: 4px; }
  .pizza-desc { font-size: 12px; color: #666; margin-bottom: 8px; line-height: 1.4; }
  .pizza-diet { font-size: 11px; color: #1E8449; font-weight: 600; margin-bottom: 10px; }
  .card-bottom { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
  .pizza-price { font-size: 19px; font-weight: 800; color: #C8102E; }
  .btn-add {
    background: #C8102E; color: #FFF; border: none; padding: 7px 15px;
    border-radius: 20px; font-size: 12px; font-weight: 700; cursor: pointer;
  }
  .btn-add:hover { background: #A50C24; }

  /* Offer Banner */
  .offer-banner {
    max-width: 1130px; margin: 0 auto 44px; background: #FCE8E8; border-radius: 16px;
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

  /* OFFERS PAGE: Deal Cards */
  .offers-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  @media (max-width: 860px) { .offers-grid { grid-template-columns: 1fr; } }
  .deal-card {
    background: #FFF9F8; border: 2px dashed #E6B0AA; border-radius: 18px; padding: 26px;
    text-align: center; display: flex; flex-direction: column; justify-content: space-between;
  }
  .deal-badge {
    background: #C8102E; color: #FFF; font-weight: 800; font-size: 13px;
    padding: 5px 14px; border-radius: 20px; display: inline-block; margin-bottom: 12px;
  }
  .deal-card h3 { font-size: 21px; font-weight: 800; color: #1E1E1E; margin-bottom: 8px; }
  .deal-card p { font-size: 13.5px; color: #555; margin-bottom: 16px; line-height: 1.5; }
  .coupon-box {
    background: #FFF; border: 1px solid #CCC; padding: 8px 14px; border-radius: 8px;
    font-weight: 800; color: #C8102E; letter-spacing: 1.5px; margin-bottom: 14px;
  }

  /* ABOUT US PAGE */
  .about-grid { display: grid; grid-template-columns: 1.1fr 1fr; gap: 36px; align-items: center; margin-bottom: 36px; }
  @media (max-width: 860px) { .about-grid { grid-template-columns: 1fr; } }
  .about-grid img { width: 100%; border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
  .values-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  @media (max-width: 860px) { .values-grid { grid-template-columns: 1fr; } }
  .value-card {
    background: #FFFDF9; border: 1px solid #EFE4D8; border-radius: 14px; padding: 22px; text-align: center;
  }
  .value-card .v-icon { font-size: 34px; margin-bottom: 10px; }

  /* CONTACT PAGE */
  .contact-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 32px; }
  @media (max-width: 860px) { .contact-grid { grid-template-columns: 1fr; } }
  .info-box {
    background: #FFF8F6; border: 1px solid #F3D6D2; border-radius: 16px; padding: 26px;
  }
  .info-row { display: flex; gap: 14px; margin-bottom: 18px; align-items: flex-start; }
  .contact-form-box {
    background: #FFF; border: 1px solid #E6E6E6; border-radius: 16px; padding: 26px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
  }

  /* Footer */
  .site-footer {
    background: #1E1E1E; color: #DDD; padding: 28px 48px; margin-top: auto;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;
  }
  .footer-links { display: flex; gap: 20px; flex-wrap: wrap; }
  .footer-links a { color: #FFF; text-decoration: none; font-size: 13px; cursor: pointer; }
  .footer-links a:hover { color: #F5B7B1; }

  /* Floating Chatbot Widget */
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
    height: 260px; overflow-y: auto; padding: 14px; background: #FAFAFA;
    display: flex; flex-direction: column; gap: 10px;
  }
  .msg-row { display: flex; align-items: flex-start; gap: 8px; }
  .msg-row.user { justify-content: flex-end; }
  .bot-avatar {
    width: 32px; height: 32px; border-radius: 50%; background: #EBF5FB;
    display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
  }
  .msg-bubble { padding: 9px 13px; border-radius: 14px; font-size: 12.5px; line-height: 1.45; max-width: 240px; }
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

  /* Modals & Toast */
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
  .form-group input, .form-group select, .form-group textarea {
    width: 100%; padding: 9px 12px; border: 1px solid #CCC; border-radius: 8px; font-size: 13px;
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

<!-- Persistent Top Header -->
<header class="top-header">
  <div class="logo-wrap" onclick="switchPage('home')">
    <div class="logo-icon">🍕</div>
    <div>
      <div class="logo-title">Bingo &amp; Gogo</div>
      <div class="logo-sub">— Pizza Shop —</div>
    </div>
  </div>

  <div class="search-box">
    <span class="search-icon">🔍</span>
    <input type="text" id="searchInput" placeholder="Search for pizzas..." oninput="handleSearch()" />
  </div>

  <div class="header-actions">
    <button class="cart-btn" onclick="openModal('cartModal')">
      🛒 <span class="cart-badge" id="cartBadge">0</span>
    </button>
    <button class="btn-admin" onclick="openModal('adminModal')">⚙️ Store Admin</button>
    <button class="btn-login" onclick="showToast('Welcome to Bingo & Gogo Pizza!')">👤 Login / Register</button>
  </div>
</header>

<!-- Persistent Navigation Bar -->
<nav class="nav-bar">
  <a id="nav-home" class="active" onclick="switchPage('home')">Home</a>
  <a id="nav-menu" onclick="switchPage('menu')">Menu</a>
  <a id="nav-offers" onclick="switchPage('offers')">Offers</a>
  <a id="nav-about" onclick="switchPage('about')">About Us</a>
  <a id="nav-contact" onclick="switchPage('contact')">Contact</a>
</nav>

<!-- ==================== PAGE 1: HOME ==================== -->
<main id="page-home" class="page-view active">
  <section class="hero">
    <div class="hero-left">
      <h1>Bingo &amp; Gogo</h1>
      <h2>Delicious Pizza!</h2>
      <p>Good Food. Great Mood.</p>
      <button class="btn-primary" onclick="switchPage('menu')">Order Now →</button>
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

  <section class="categories">
    <div class="cat-item" onclick="goToMenuCategory('Veg Pizzas')">
      <div class="cat-circle">🌿</div>
      <div class="cat-label">Veg Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Non-Veg Pizzas')">
      <div class="cat-circle">🍗</div>
      <div class="cat-label">Non-Veg Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Cheese Pizzas')">
      <div class="cat-circle">🧀</div>
      <div class="cat-label">Cheese Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Special Pizzas')">
      <div class="cat-circle">⭐</div>
      <div class="cat-label">Special Pizzas</div>
    </div>
  </section>

  <section class="section-wrap">
    <h2 class="section-title">Our Popular Pizzas</h2>
    <p class="section-sub">Customer favorites baked fresh to order</p>
    <div class="pizza-grid" id="homePizzaGrid">
      <p style="grid-column:1/-1; text-align:center; color:#666;">Loading live menu from Supabase...</p>
    </div>
    <div style="text-align:center; margin-top:26px;">
      <button class="btn-primary" onclick="switchPage('menu')">Explore Full Menu →</button>
    </div>
  </section>

  <section class="offer-banner">
    <div class="offer-left">
      <div class="badge-20">20%<br>OFF</div>
      <div class="offer-title">Special Offer!</div>
      <div class="offer-div"></div>
      <div class="offer-text">Get 20% OFF on all Pizzas!</div>
    </div>
    <button class="btn-primary" onclick="switchPage('offers')">Claim Offer →</button>
  </section>
</main>

<!-- ==================== PAGE 2: MENU ==================== -->
<main id="page-menu" class="page-view">
  <div class="inner-banner">
    <h1>🍕 Our Full Live Menu</h1>
    <p>Synced in real time with our kitchen database — filter by category or search your favorite toppings</p>
  </div>
  <section class="section-wrap">
    <div class="filter-pills" id="menuFilterPills">
      <button class="pill-tab active" onclick="setMenuCategory('All')">All Pizzas</button>
      <button class="pill-tab" onclick="setMenuCategory('Veg Pizzas')">🌿 Veg Pizzas</button>
      <button class="pill-tab" onclick="setMenuCategory('Non-Veg Pizzas')">🍗 Non-Veg Pizzas</button>
      <button class="pill-tab" onclick="setMenuCategory('Cheese Pizzas')">🧀 Cheese Pizzas</button>
      <button class="pill-tab" onclick="setMenuCategory('Special Pizzas')">⭐ Special Pizzas</button>
    </div>
    <div class="pizza-grid" id="fullMenuGrid"></div>
  </section>
</main>

<!-- ==================== PAGE 3: OFFERS ==================== -->
<main id="page-offers" class="page-view">
  <div class="inner-banner">
    <h1>🔥 Exclusive Deals &amp; Offers</h1>
    <p>Apply a promo code to your cart with one click and save on your pizza feast</p>
  </div>
  <section class="section-wrap">
    <div class="offers-grid">
      <div class="deal-card">
        <div>
          <span class="deal-badge">FLAT 20% OFF</span>
          <h3>All Pizzas Mega Deal</h3>
          <p>Enjoy 20% instant discount on every Veg, Non-Veg, Cheese, and Special Pizza on our menu.</p>
          <div class="coupon-box">CODE: BINGO20</div>
        </div>
        <button class="btn-primary" onclick="claimPromoAndShop('BINGO20')">Apply &amp; Order Now</button>
      </div>

      <div class="deal-card">
        <div>
          <span class="deal-badge">FREE DELIVERY</span>
          <h3>Zero Delivery Fee</h3>
          <p>Order above ₹299 and get piping hot doorstep delivery within 30 minutes at zero delivery charge.</p>
          <div class="coupon-box">AUTO-APPLIED &gt; ₹299</div>
        </div>
        <button class="btn-primary" onclick="switchPage('menu')">Browse Pizzas</button>
      </div>

      <div class="deal-card">
        <div>
          <span class="deal-badge">WEEKEND FEAST</span>
          <h3>Family Combo Savings</h3>
          <p>Mix any 3 pizzas from our Special or Supreme range and save 20% with code BINGO20 at checkout.</p>
          <div class="coupon-box">CODE: BINGO20</div>
        </div>
        <button class="btn-primary" onclick="claimPromoAndShop('BINGO20')">Start Combo Order</button>
      </div>
    </div>
  </section>
</main>

<!-- ==================== PAGE 4: ABOUT US ==================== -->
<main id="page-about" class="page-view">
  <div class="inner-banner">
    <h1>❤️ About Bingo &amp; Gogo Pizza</h1>
    <p>Good Food. Great Mood. Handcrafted daily with farm-fresh ingredients</p>
  </div>
  <section class="section-wrap">
    <div class="about-grid">
      <div>
        <h2 style="color:#C8102E; font-size:28px; font-weight:800; margin-bottom:14px;">Our Story &amp; Kitchen Philosophy</h2>
        <p style="color:#444; font-size:15px; line-height:1.7; margin-bottom:14px;">
          Founded with a simple belief—that great pizza brings people together—<strong>Bingo &amp; Gogo Pizza Shop</strong> hand-stretches every dough batch fresh each morning and bakes it at high stone-deck temperatures for a crisp, airy crust.
        </p>
        <p style="color:#444; font-size:15px; line-height:1.7; margin-bottom:20px;">
          From classic San Marzano tomato Margherita to our signature Tandoori Paneer Feast, every pizza is topped to order and delivered hot within 30 minutes.
        </p>
        <button class="btn-primary" onclick="switchPage('menu')">Taste Our Menu →</button>
      </div>
      <div>
        <img src="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=700" alt="Freshly Baked Pizza" />
      </div>
    </div>

    <div class="values-grid">
      <div class="value-card">
        <div class="v-icon">🌿</div>
        <h3 style="font-size:17px; margin-bottom:6px;">100% Separate Veg Prep</h3>
        <p style="font-size:13px; color:#555;">Dedicated vegetarian prep counters, cutters, and baking trays for complete peace of mind.</p>
      </div>
      <div class="value-card">
        <div class="v-icon">🧀</div>
        <h3 style="font-size:17px; margin-bottom:6px;">Real Mozzarella &amp; Fresh Dough</h3>
        <p style="font-size:13px; color:#555;">Never frozen dough paired with rich, creamy mozzarella and locally sourced crisp vegetables.</p>
      </div>
      <div class="value-card">
        <div class="v-icon">⚡</div>
        <h3 style="font-size:17px; margin-bottom:6px;">30-Minute Hot Delivery</h3>
        <p style="font-size:13px; color:#555;">Insulated thermal delivery bags ensure your pizza arrives bubbling hot right at your door.</p>
      </div>
    </div>
  </section>
</main>

<!-- ==================== PAGE 5: CONTACT ==================== -->
<main id="page-contact" class="page-view">
  <div class="inner-banner">
    <h1>📞 Contact &amp; Store Location</h1>
    <p>Have a question, party order request, or feedback? Reach out to us anytime</p>
  </div>
  <section class="section-wrap">
    <div class="contact-grid">
      <div class="info-box">
        <h3 style="color:#C8102E; font-size:20px; font-weight:800; margin-bottom:18px;">Visit or Call Us</h3>
        <div class="info-row">
          <span style="font-size:22px;">📍</span>
          <div>
            <strong>Store Address</strong>
            <p style="font-size:13.5px; color:#555;">742 Evergreen Pizza Avenue, Food District</p>
          </div>
        </div>
        <div class="info-row">
          <span style="font-size:22px;">📞</span>
          <div>
            <strong>Phone &amp; Order Support</strong>
            <p style="font-size:13.5px; color:#555;">(555) 839-7499</p>
          </div>
        </div>
        <div class="info-row">
          <span style="font-size:22px;">🕒</span>
          <div>
            <strong>Opening Hours</strong>
            <p style="font-size:13.5px; color:#555;">Monday – Sunday: 11:00 AM – 11:00 PM</p>
          </div>
        </div>
        <div class="info-row">
          <span style="font-size:22px;">🛵</span>
          <div>
            <strong>Delivery Zone</strong>
            <p style="font-size:13.5px; color:#555;">Within 5 km radius (Free delivery above ₹299)</p>
          </div>
        </div>
        <button class="btn-primary" style="margin-top:8px;" onclick="toggleChat(true)">💬 Chat with AI Assistant</button>
      </div>

      <div class="contact-form-box">
        <h3 style="color:#1E1E1E; font-size:20px; font-weight:800; margin-bottom:14px;">Send Us a Message</h3>
        <div class="form-group"><label>Your Name</label><input id="contactName" placeholder="Enter your name" /></div>
        <div class="form-group"><label>Phone or Email</label><input id="contactEmail" placeholder="Enter phone number or email" /></div>
        <div class="form-group"><label>Message / Catering Inquiry</label><textarea id="contactMsg" rows="4" placeholder="How can we help you?"></textarea></div>
        <button class="btn-primary" style="width:100%;" onclick="submitContactForm()">Send Message</button>
      </div>
    </div>
  </section>
</main>

<!-- Persistent Footer -->
<footer class="site-footer">
  <div>
    <strong style="color:#FFF; font-size:16px;">🍕 Bingo &amp; Gogo Pizza Shop</strong>
    <div style="font-size:12px; color:#AAA; margin-top:4px;">Open Daily: 11:00 AM – 11:00 PM | Helpline: (555) 839-7499</div>
  </div>
  <div class="footer-links">
    <a onclick="switchPage('home')">Home</a>
    <a onclick="switchPage('menu')">Menu</a>
    <a onclick="switchPage('offers')">Offers</a>
    <a onclick="switchPage('about')">About Us</a>
    <a onclick="switchPage('contact')">Contact</a>
  </div>
</footer>

<!-- Floating Chatbot Widget (Persistent Across All Pages) -->
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
  let activePage = "home";
  let menuCategory = "All";
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

  // Multi-Page Navigation Controller
  function switchPage(pageName) {
    activePage = pageName;
    document.querySelectorAll(".page-view").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".nav-bar a").forEach(a => a.classList.remove("active"));

    const targetPage = document.getElementById("page-" + pageName);
    const targetNav = document.getElementById("nav-" + pageName);
    if (targetPage) targetPage.classList.add("active");
    if (targetNav) targetNav.classList.add("active");

    window.scrollTo({ top: 0, behavior: "smooth" });
    if (pageName === "menu") renderFullMenu();
  }

  function goToMenuCategory(cat) {
    switchPage("menu");
    setMenuCategory(cat);
  }

  function setMenuCategory(cat) {
    menuCategory = cat;
    document.querySelectorAll("#menuFilterPills .pill-tab").forEach(btn => {
      btn.classList.toggle("active", btn.textContent.includes(cat) || (cat === "All" && btn.textContent.includes("All")));
    });
    renderFullMenu();
  }

  function handleSearch() {
    if (activePage !== "menu") switchPage("menu");
    renderFullMenu();
  }

  // Fetch Live Menu Rows from Supabase
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
        renderHomePopular();
        renderFullMenu();
        renderAdminDeleteList();
      }
    } catch (err) {
      console.error("Supabase fetch error:", err);
    }
    return menuItems;
  }

  function buildPizzaCardHTML(item, showMeta = false) {
    return `
      <div class="pizza-card">
        <div>
          <img src="${item.image_url || 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500'}" alt="${item.name}" />
          ${showMeta ? `<span class="cat-tag">${item.category}</span>` : ''}
          <div class="pizza-name">${item.name}</div>
          <div class="pizza-desc">${item.description || ''}</div>
          ${showMeta && item.dietary_info ? `<div class="pizza-diet">🌱 ${item.dietary_info}</div>` : ''}
        </div>
        <div class="card-bottom">
          <span class="pizza-price">${item.pricing}</span>
          <button class="btn-add" onclick="addToCart(${item.id})">Add to Cart</button>
        </div>
      </div>
    `;
  }

  function renderHomePopular() {
    const grid = document.getElementById("homePizzaGrid");
    if (!menuItems.length) {
      grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:#666;">No pizzas found. Add pizzas via Store Admin.</p>`;
      return;
    }
    // Show first 4 popular pizzas on Home Page
    grid.innerHTML = menuItems.slice(0, 4).map(item => buildPizzaCardHTML(item, false)).join("");
  }

  function renderFullMenu() {
    const grid = document.getElementById("fullMenuGrid");
    if (!grid) return;
    const q = document.getElementById("searchInput").value.toLowerCase().trim();
    const filtered = menuItems.filter(item => {
      const matchCat = menuCategory === "All" || item.category === menuCategory;
      const matchText = !q || item.name.toLowerCase().includes(q) || (item.description || "").toLowerCase().includes(q);
      return matchCat && matchText;
    });

    if (!filtered.length) {
      grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:#666;">No pizzas match your filter.</p>`;
      return;
    }
    grid.innerHTML = filtered.map(item => buildPizzaCardHTML(item, true)).join("");
  }

  function claimPromoAndShop(code) {
    discountApplied = true;
    document.getElementById("promoInput").value = code;
    showToast(`Promo ${code} (20% OFF) activated! Pick your pizzas.`);
    switchPage("menu");
  }

  function submitContactForm() {
    const name = document.getElementById("contactName").value.trim();
    const msg = document.getElementById("contactMsg").value.trim();
    if (!name || !msg) {
      showToast("Please enter your name and message.");
      return;
    }
    document.getElementById("contactName").value = "";
    document.getElementById("contactEmail").value = "";
    document.getElementById("contactMsg").value = "";
    showToast(`Thank you ${name}! Our team will contact you shortly.`);
  }

  // Cart & Promo Logic
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

  // Admin Panel
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

  // Real-Time Chatbot
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

  fetchLiveMenu();
</script>
</body>
</html>
"""

final_html = HTML_WEBSITE.replace("__APP_CONFIG__", config_json)
components.html(final_html, height=1000, scrolling=True)
