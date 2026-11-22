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
    "Active Offers: 20% OFF on all Pizzas (Code: BINGO20). Free delivery within 5 km on orders above ₹299. "
    "Accepted Payments: UPI, Debit/Credit Cards, Net Banking, and Cash on Delivery. "
    "Store Hours: 11:00 AM - 11:00 PM daily. Phone: (555) 839-7499."
)
POL_TEXT = open(pol_path, "r", encoding="utf-8").read() if os.path.exists(pol_path) else (
    "Separate preparation counters for Veg and Non-Veg pizzas. Orders can be canceled within 5 minutes."
)

# Strip Streamlit default padding & chrome
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

  .header-actions { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
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
  .user-pill {
    background: #EAFAF1; color: #1E8449; border: 1px solid #A9DFBF;
    padding: 7px 14px; border-radius: 25px; font-size: 12.5px; font-weight: 700;
    display: flex; align-items: center; gap: 8px;
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

  /* Page Views */
  .page-view { display: none; flex: 1; }
  .page-view.active { display: block; }

  .btn-primary {
    background: #C8102E; color: #FFF; border: none; padding: 12px 28px;
    border-radius: 30px; font-size: 14px; font-weight: 700; cursor: pointer;
    box-shadow: 0 4px 12px rgba(200,16,46,0.28); text-decoration: none; display: inline-block;
  }
  .btn-primary:hover { background: #A80C24; }
  .btn-primary:disabled { background: #999; cursor: not-allowed; box-shadow: none; }

  .section-wrap { max-width: 1180px; margin: 0 auto; padding: 28px 24px 44px; }
  .section-title { text-align: center; font-size: 28px; font-weight: 800; margin-bottom: 8px; color: #1E1E1E; }
  .section-sub { text-align: center; font-size: 14px; color: #666; margin-bottom: 26px; }

  .inner-banner {
    background: linear-gradient(90deg, #FFFDF9 0%, #F7ECE1 100%);
    padding: 34px 24px; text-align: center; border-bottom: 1px solid #EFE4D8;
  }
  .inner-banner h1 { color: #C8102E; font-size: 36px; font-weight: 800; }
  .inner-banner p { color: #555; font-size: 15px; margin-top: 6px; }

  /* Hero */
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

  /* Categories */
  .categories {
    display: flex; justify-content: center; gap: 48px; padding: 32px 20px 10px; flex-wrap: wrap;
  }
  .cat-item { text-align: center; cursor: pointer; transition: transform 0.2s; }
  .cat-item:hover { transform: translateY(-4px); }
  .cat-circle {
    width: 78px; height: 78px; border-radius: 50%; background: #FCEEEE;
    display: flex; align-items: center; justify-content: center; font-size: 34px;
    margin: 0 auto 8px;
  }
  .cat-label { font-size: 14px; font-weight: 700; color: #222; }

  .filter-pills { display: flex; justify-content: center; gap: 10px; margin-bottom: 26px; flex-wrap: wrap; }
  .pill-tab {
    padding: 8px 20px; border-radius: 25px; border: 1px solid #DDD;
    background: #FFF; font-size: 13px; font-weight: 600; cursor: pointer; color: #333;
  }
  .pill-tab.active, .pill-tab:hover { background: #C8102E; color: #FFF; border-color: #C8102E; }

  /* Pizza Cards */
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

  /* Offers, About, Contact Layouts */
  .offers-grid, .values-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  .about-grid, .contact-grid { display: grid; grid-template-columns: 1fr 1.15fr; gap: 32px; align-items: start; }
  @media (max-width: 860px) { .offers-grid, .values-grid, .about-grid, .contact-grid { grid-template-columns: 1fr; } }

  .deal-card {
    background: #FFF9F8; border: 2px dashed #E6B0AA; border-radius: 18px; padding: 26px;
    text-align: center; display: flex; flex-direction: column; justify-content: space-between;
  }
  .deal-badge {
    background: #C8102E; color: #FFF; font-weight: 800; font-size: 13px;
    padding: 5px 14px; border-radius: 20px; display: inline-block; margin-bottom: 12px;
  }
  .coupon-box {
    background: #FFF; border: 1px solid #CCC; padding: 8px 14px; border-radius: 8px;
    font-weight: 800; color: #C8102E; letter-spacing: 1.5px; margin: 12px 0 14px;
  }
  .value-card { background: #FFFDF9; border: 1px solid #EFE4D8; border-radius: 14px; padding: 22px; text-align: center; }
  .info-box { background: #FFF8F6; border: 1px solid #F3D6D2; border-radius: 16px; padding: 26px; }
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

  /* Floating Chatbot */
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
    height: 250px; overflow-y: auto; padding: 14px; background: #FAFAFA;
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

  /* Modals & Payment UI */
  .modal-backdrop {
    position: fixed; inset: 0; background: rgba(0,0,0,0.58); display: none;
    align-items: center; justify-content: center; z-index: 1000;
  }
  .modal-card {
    background: #FFF; width: 560px; max-width: 95vw; border-radius: 16px;
    padding: 24px; max-height: 90vh; overflow-y: auto; position: relative;
  }
  .modal-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
  .modal-head h3 { color: #C8102E; font-size: 20px; font-weight: 800; }
  .tab-bar { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid #EEE; padding-bottom: 10px; flex-wrap: wrap; }
  .tab-btn {
    padding: 7px 14px; border-radius: 20px; border: 1px solid #DDD; background: #FAFAFA;
    font-size: 12.5px; font-weight: 700; cursor: pointer;
  }
  .tab-btn.active { background: #C8102E; color: #FFF; border-color: #C8102E; }

  .form-group { margin-bottom: 11px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 4px; color: #333; }
  .form-group input, .form-group select, .form-group textarea {
    width: 100%; padding: 9px 12px; border: 1px solid #CCC; border-radius: 8px; font-size: 13px; outline: none;
  }
  .form-group input:focus, .form-group select:focus { border-color: #C8102E; }
  .form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

  .qty-btn {
    width: 24px; height: 24px; border-radius: 50%; border: 1px solid #CCC;
    background: #FFF; font-weight: 700; cursor: pointer;
  }

  /* Payment Method Selector Grid */
  .pay-methods-grid {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 9px; margin-bottom: 14px;
  }
  .pay-option {
    border: 2px solid #E5E5E5; border-radius: 12px; padding: 10px 12px;
    cursor: pointer; display: flex; align-items: center; gap: 10px;
    background: #FAFAFA; transition: 0.15s; font-size: 13px; font-weight: 700;
  }
  .pay-option:hover { border-color: #E6B0AA; }
  .pay-option.active {
    border-color: #C8102E; background: #FFF5F5; color: #C8102E;
  }
  .pay-detail-box {
    background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px;
    padding: 14px; margin-bottom: 14px;
  }
  .upi-apps-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 8px 0 12px; }
  .upi-app-chip {
    background: #FFF; border: 1px solid #D1D5DB; border-radius: 20px;
    padding: 5px 12px; font-size: 11.5px; font-weight: 700; cursor: pointer;
  }
  .upi-app-chip:hover { border-color: #C8102E; color: #C8102E; }

  .bank-tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }
  .bank-tile {
    background: #FFF; border: 1px solid #D1D5DB; border-radius: 8px; padding: 8px 4px;
    text-align: center; font-size: 11.5px; font-weight: 700; cursor: pointer;
  }
  .bank-tile.active, .bank-tile:hover { border-color: #C8102E; background: #FFF0F0; color: #C8102E; }

  /* Payment Processing Spinner Overlay */
  .processing-box {
    text-align: center; padding: 32px 16px;
  }
  .spinner {
    width: 44px; height: 44px; border: 4px solid #F3C2C2; border-top-color: #C8102E;
    border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 14px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Status Badges */
  .badge-paid { background: #EAFAF1; color: #1E8449; border: 1px solid #A9DFBF; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 700; }
  .badge-cod { background: #FEF9E7; color: #B7950B; border: 1px solid #F9E79F; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 700; }

  .toast {
    position: fixed; top: 20px; right: 24px; background: #1E8449; color: #FFF;
    padding: 11px 20px; border-radius: 10px; font-size: 13px; font-weight: 600;
    display: none; z-index: 1200; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }
</style>
</head>
<body>

<div id="toast" class="toast"></div>

<!-- Top Header -->
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
    <div id="authHeaderSlot">
      <button class="btn-login" onclick="openModal('authModal')">👤 Login / Register</button>
    </div>
  </div>
</header>

<!-- Navigation Bar -->
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
      <span class="dot active"></span><span class="dot"></span><span class="dot"></span>
    </div>
  </section>

  <section class="categories">
    <div class="cat-item" onclick="goToMenuCategory('Veg Pizzas')">
      <div class="cat-circle">🌿</div><div class="cat-label">Veg Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Non-Veg Pizzas')">
      <div class="cat-circle">🍗</div><div class="cat-label">Non-Veg Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Cheese Pizzas')">
      <div class="cat-circle">🧀</div><div class="cat-label">Cheese Pizzas</div>
    </div>
    <div class="cat-item" onclick="goToMenuCategory('Special Pizzas')">
      <div class="cat-circle">⭐</div><div class="cat-label">Special Pizzas</div>
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
          <p style="font-size:13.5px;color:#555;">Enjoy 20% instant discount on every Veg, Non-Veg, Cheese, and Special Pizza.</p>
          <div class="coupon-box">CODE: BINGO20</div>
        </div>
        <button class="btn-primary" onclick="claimPromoAndShop('BINGO20')">Apply &amp; Order Now</button>
      </div>
      <div class="deal-card">
        <div>
          <span class="deal-badge">FREE DELIVERY</span>
          <h3>Zero Delivery Fee</h3>
          <p style="font-size:13.5px;color:#555;">Order above ₹299 and get doorstep delivery within 30 minutes at zero delivery charge.</p>
          <div class="coupon-box">AUTO-APPLIED &gt; ₹299</div>
        </div>
        <button class="btn-primary" onclick="switchPage('menu')">Browse Pizzas</button>
      </div>
      <div class="deal-card">
        <div>
          <span class="deal-badge">WEEKEND FEAST</span>
          <h3>Family Combo Savings</h3>
          <p style="font-size:13.5px;color:#555;">Mix any 3 pizzas from our Special or Supreme range and save 20% with code BINGO20.</p>
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
          At <strong>Bingo &amp; Gogo Pizza Shop</strong>, every dough batch is hand-stretched fresh each morning and stone-baked for a crisp, airy crust.
        </p>
        <p style="color:#444; font-size:15px; line-height:1.7; margin-bottom:20px;">
          From classic Margherita to our signature Tandoori Paneer Feast, every pizza is topped to order and delivered hot within 30 minutes.
        </p>
        <button class="btn-primary" onclick="switchPage('menu')">Taste Our Menu →</button>
      </div>
      <div>
        <img src="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=700" style="width:100%;border-radius:18px;" alt="Fresh Pizza" />
      </div>
    </div>
    <div class="values-grid">
      <div class="value-card"><div style="font-size:34px;margin-bottom:8px;">🌿</div><h4>100% Separate Veg Prep</h4><p style="font-size:13px;color:#555;margin-top:6px;">Dedicated vegetarian prep counters, cutters, and baking trays.</p></div>
      <div class="value-card"><div style="font-size:34px;margin-bottom:8px;">🧀</div><h4>Real Mozzarella &amp; Fresh Dough</h4><p style="font-size:13px;color:#555;margin-top:6px;">Never frozen dough paired with creamy mozzarella and crisp veggies.</p></div>
      <div class="value-card"><div style="font-size:34px;margin-bottom:8px;">⚡</div><h4>30-Minute Hot Delivery</h4><p style="font-size:13px;color:#555;margin-top:6px;">Insulated thermal delivery bags keep your pizza bubbling hot.</p></div>
    </div>
  </section>
</main>

<!-- ==================== PAGE 5: CONTACT ==================== -->
<main id="page-contact" class="page-view">
  <div class="inner-banner">
    <h1>📞 Contact &amp; Store Location</h1>
    <p>Questions, party orders, or feedback? Send us a direct message saved straight to our Store Admin inbox</p>
  </div>
  <section class="section-wrap">
    <div class="contact-grid">
      <div class="info-box">
        <h3 style="color:#C8102E; font-size:20px; font-weight:800; margin-bottom:18px;">Visit or Call Us</h3>
        <div class="info-row"><span style="font-size:22px;">📍</span><div><strong>Store Address</strong><p style="font-size:13.5px;color:#555;">742 Evergreen Pizza Avenue, Food District</p></div></div>
        <div class="info-row"><span style="font-size:22px;">📞</span><div><strong>Phone &amp; Order Support</strong><p style="font-size:13.5px;color:#555;">(555) 839-7499</p></div></div>
        <div class="info-row"><span style="font-size:22px;">🕒</span><div><strong>Opening Hours</strong><p style="font-size:13.5px;color:#555;">Monday – Sunday: 11:00 AM – 11:00 PM</p></div></div>
        <div class="info-row"><span style="font-size:22px;">🛵</span><div><strong>Delivery Zone</strong><p style="font-size:13.5px;color:#555;">Within 5 km radius (Free delivery above ₹299)</p></div></div>
      </div>

      <div class="contact-form-box">
        <h3 style="color:#1E1E1E; font-size:20px; font-weight:800; margin-bottom:14px;">Send Us a Message</h3>
        <div class="form-group"><label>Your Name *</label><input id="contactName" placeholder="Enter your full name" /></div>
        <div class="form-group"><label>Phone or Email *</label><input id="contactEmail" placeholder="Enter phone number or email" /></div>
        <div class="form-group"><label>Message / Catering Inquiry *</label><textarea id="contactMsg" rows="4" placeholder="Write your message here..."></textarea></div>
        <button class="btn-primary" id="sendMsgBtn" style="width:100%;" onclick="submitContactForm()">Send Message</button>
      </div>
    </div>
  </section>
</main>

<!-- Footer -->
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

<!-- Floating Chatbot Widget -->
<button class="chat-launcher" id="chatLauncher" onclick="toggleChat(true)">🍕 Bingo &amp; Gogo Assistant</button>
<div class="chat-widget" id="chatWidget">
  <div class="chat-header">
    <span>🍕 Bingo &amp; Gogo Assistant</span>
    <div class="chat-controls"><span onclick="toggleChat(false)">—</span><span onclick="toggleChat(false)">✕</span></div>
  </div>
  <div class="chat-body" id="chatBody">
    <div class="msg-row bot"><div class="bot-avatar">🤖</div><div class="msg-bubble">Hello! Welcome to Bingo &amp; Gogo Pizza! How can I help you?</div></div>
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

<!-- ==================== MODAL 1: CART & FULL PAYMENT CHECKOUT ==================== -->
<div class="modal-backdrop" id="cartModal">
  <div class="modal-card">
    <div class="modal-head">
      <h3>🛒 Checkout &amp; Payment</h3>
      <button onclick="closeModal('cartModal')" style="border:none;background:none;font-size:20px;cursor:pointer;">✕</button>
    </div>

    <!-- Processing Spinner View -->
    <div id="paymentProcessingBox" class="processing-box" style="display:none;">
      <div class="spinner"></div>
      <h4 id="processingTitle" style="color:#C8102E;margin-bottom:6px;">Processing Payment...</h4>
      <p id="processingSub" style="font-size:13px;color:#666;">Connecting securely to payment gateway. Please do not close this window.</p>
    </div>

    <!-- Main Cart + Delivery + Payment Form -->
    <div id="cartMainBody">
      <div id="cartItemsList"></div>

      <div id="checkoutSection" style="display:none; margin-top:14px; border-top:1px solid #EEE; padding-top:12px;">
        <div style="display:flex; gap:8px; margin-bottom:10px;">
          <input type="text" id="promoInput" placeholder="Promo code (BINGO20)" style="flex:1;padding:8px;border:1px solid #CCC;border-radius:8px;font-size:13px;" />
          <button class="btn-add" onclick="applyPromo()">Apply</button>
        </div>
        <div id="cartTotalBox" style="font-weight:800; font-size:16px; margin-bottom:14px; color:#1E1E1E;"></div>

        <h4 style="font-size:13.5px; color:#C8102E; margin-bottom:8px;">1. Delivery Details</h4>
        <div class="form-row-2">
          <div class="form-group"><label>Customer Name *</label><input id="orderName" placeholder="Your full name" /></div>
          <div class="form-group"><label>Phone Number *</label><input id="orderPhone" placeholder="10-digit mobile number" /></div>
        </div>
        <div class="form-group"><label>Delivery Address *</label><input id="orderAddress" placeholder="House/Flat No, Street, Landmark" /></div>

        <h4 style="font-size:13.5px; color:#C8102E; margin:14px 0 8px;">2. Select Payment Method</h4>
        <div class="pay-methods-grid">
          <div class="pay-option active" id="payOpt-upi" onclick="selectPaymentMethod('UPI')">
            <span style="font-size:20px;">📱</span><span>UPI (GPay / PhonePe)</span>
          </div>
          <div class="pay-option" id="payOpt-card" onclick="selectPaymentMethod('Debit / Credit Card')">
            <span style="font-size:20px;">💳</span><span>Debit / Credit Card</span>
          </div>
          <div class="pay-option" id="payOpt-netbanking" onclick="selectPaymentMethod('Net Banking')">
            <span style="font-size:20px;">🏦</span><span>Net Banking</span>
          </div>
          <div class="pay-option" id="payOpt-cod" onclick="selectPaymentMethod('Cash on Delivery')">
            <span style="font-size:20px;">💵</span><span>Cash on Delivery</span>
          </div>
        </div>

        <!-- Payment Sub-Panel A: UPI -->
        <div class="pay-detail-box" id="payPanel-upi">
          <div style="display:flex; align-items:center; gap:14px; margin-bottom:10px;">
            <div style="background:#FFF; border:1px solid #DDD; padding:8px; border-radius:10px; text-align:center; min-width:86px;">
              <div style="font-size:32px; line-height:1;">📲</div>
              <div style="font-size:10px; font-weight:700; color:#333; margin-top:4px;">Scan UPI QR</div>
            </div>
            <div style="font-size:12px; color:#444;">
              <strong>Pay instantly via any UPI app</strong>
              <div class="upi-apps-row">
                <span class="upi-app-chip" onclick="fillSampleUpi('okicici')">GPay</span>
                <span class="upi-app-chip" onclick="fillSampleUpi('ybl')">PhonePe</span>
                <span class="upi-app-chip" onclick="fillSampleUpi('paytm')">Paytm</span>
                <span class="upi-app-chip" onclick="fillSampleUpi('upi')">BHIM</span>
              </div>
            </div>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label>Enter Your UPI ID *</label>
            <input id="upiIdInput" placeholder="e.g. yourname@okicici or 9876543210@ybl" />
          </div>
        </div>

        <!-- Payment Sub-Panel B: Debit / Credit Card -->
        <div class="pay-detail-box" id="payPanel-card" style="display:none;">
          <div class="form-group">
            <label>Card Number *</label>
            <input id="cardNumInput" maxlength="19" placeholder="4532 •••• •••• 8890" oninput="formatCardNumber(this)" />
          </div>
          <div class="form-group">
            <label>Name on Card *</label>
            <input id="cardNameInput" placeholder="e.g. RAHUL SHARMA" />
          </div>
          <div class="form-row-2">
            <div class="form-group" style="margin-bottom:0;">
              <label>Expiry (MM/YY) *</label>
              <input id="cardExpInput" maxlength="5" placeholder="08/29" oninput="formatCardExpiry(this)" />
            </div>
            <div class="form-group" style="margin-bottom:0;">
              <label>CVV *</label>
              <input id="cardCvvInput" type="password" maxlength="4" placeholder="•••" />
            </div>
          </div>
        </div>

        <!-- Payment Sub-Panel C: Net Banking -->
        <div class="pay-detail-box" id="payPanel-netbanking" style="display:none;">
          <label style="display:block;font-size:12px;font-weight:700;margin-bottom:6px;">Popular Indian Banks</label>
          <div class="bank-tiles">
            <div class="bank-tile active" onclick="pickBank('HDFC Bank', this)">HDFC</div>
            <div class="bank-tile" onclick="pickBank('State Bank of India', this)">SBI</div>
            <div class="bank-tile" onclick="pickBank('ICICI Bank', this)">ICICI</div>
            <div class="bank-tile" onclick="pickBank('Axis Bank', this)">Axis</div>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label>Or Select Another Bank *</label>
            <select id="netBankSelect">
              <option value="HDFC Bank">HDFC Bank</option>
              <option value="State Bank of India">State Bank of India (SBI)</option>
              <option value="ICICI Bank">ICICI Bank</option>
              <option value="Axis Bank">Axis Bank</option>
              <option value="Kotak Mahindra Bank">Kotak Mahindra Bank</option>
              <option value="Punjab National Bank">Punjab National Bank (PNB)</option>
              <option value="Bank of Baroda">Bank of Baroda</option>
              <option value="Yes Bank">Yes Bank</option>
            </select>
          </div>
        </div>

        <!-- Payment Sub-Panel D: Cash on Delivery -->
        <div class="pay-detail-box" id="payPanel-cod" style="display:none;">
          <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:28px;">🛵</span>
            <div style="font-size:12.5px; color:#333;">
              <strong>Pay at Doorstep on Delivery</strong>
              <p style="color:#666; margin-top:2px;">Pay in cash or scan our delivery partner's QR code when your hot pizza arrives.</p>
            </div>
          </div>
        </div>

        <button class="btn-primary" id="placeOrderBtn" style="width:100%; text-align:center;" onclick="placeOrder()">Pay &amp; Place Order</button>
      </div>
    </div>
  </div>
</div>

<!-- ==================== MODAL 2: ORDER & PAYMENT RECEIPT ==================== -->
<div class="modal-backdrop" id="receiptModal">
  <div class="modal-card" style="text-align:center;">
    <div style="font-size:48px; margin-bottom:6px;">✅</div>
    <h3 style="color:#1E8449; font-size:22px; font-weight:800; margin-bottom:4px;">Order Confirmed!</h3>
    <p style="font-size:13px; color:#666; margin-bottom:16px;">Your pizza is now in our stone-deck oven</p>
    <div id="receiptDetailsBox" style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:12px; padding:16px; text-align:left; font-size:13px; line-height:1.8; margin-bottom:16px;"></div>
    <button class="btn-primary" style="width:100%;" onclick="closeModal('receiptModal')">Done</button>
  </div>
</div>

<!-- ==================== MODAL 3: LOGIN / REGISTER ==================== -->
<div class="modal-backdrop" id="authModal">
  <div class="modal-card">
    <div class="modal-head">
      <h3>👤 Customer Account</h3>
      <button onclick="closeModal('authModal')" style="border:none;background:none;font-size:20px;cursor:pointer;">✕</button>
    </div>
    <div class="tab-bar">
      <button class="tab-btn active" id="tabLoginBtn" onclick="switchAuthTab('login')">Login</button>
      <button class="tab-btn" id="tabRegBtn" onclick="switchAuthTab('register')">Register New Account</button>
    </div>

    <div id="loginFormBox">
      <div class="form-group"><label>Email Address *</label><input type="email" id="loginEmail" placeholder="you@example.com" /></div>
      <div class="form-group"><label>Password *</label><input type="password" id="loginPassword" placeholder="Enter your password" /></div>
      <button class="btn-primary" style="width:100%;" onclick="loginCustomer()">Login</button>
    </div>

    <div id="registerFormBox" style="display:none;">
      <div class="form-group"><label>Full Name *</label><input id="regName" placeholder="e.g. Rahul Sharma" /></div>
      <div class="form-group"><label>Email Address *</label><input type="email" id="regEmail" placeholder="you@example.com" /></div>
      <div class="form-group"><label>Phone Number *</label><input id="regPhone" placeholder="e.g. 9876543210" /></div>
      <div class="form-group"><label>Create Password *</label><input type="password" id="regPassword" placeholder="Choose a password" /></div>
      <button class="btn-primary" style="width:100%;" onclick="registerCustomer()">Create Account</button>
    </div>
  </div>
</div>

<!-- ==================== MODAL 4: STORE ADMIN (MENU + ORDERS + INBOX) ==================== -->
<div class="modal-backdrop" id="adminModal">
  <div class="modal-card" style="width:650px;">
    <div class="modal-head">
      <h3>⚙️ Store Admin Control Center</h3>
      <button onclick="closeModal('adminModal')" style="border:none;background:none;font-size:20px;cursor:pointer;">✕</button>
    </div>

    <div id="adminLoginBox">
      <div class="form-group">
        <label>Admin Password</label>
        <input type="password" id="adminPwdInput" placeholder="Enter admin password (default: bingo123)" onkeydown="if(event.key==='Enter') unlockAdmin()" />
      </div>
      <button class="btn-primary" style="width:100%;" onclick="unlockAdmin()">Unlock Admin Panel</button>
    </div>

    <div id="adminPanelBox" style="display:none;">
      <div class="tab-bar">
        <button class="tab-btn active" id="admTabMenu" onclick="switchAdminTab('menu')">🍕 Menu (SQL)</button>
        <button class="tab-btn" id="admTabOrders" onclick="switchAdminTab('orders')">🛵 Live Orders &amp; Payments</button>
        <button class="tab-btn" id="admTabMsgs" onclick="switchAdminTab('msgs')">📩 Customer Messages</button>
      </div>

      <!-- Admin Tab 1: Menu -->
      <div id="admViewMenu">
        <h4 style="margin-bottom:8px; color:#1E8449;">➕ Add New Pizza</h4>
        <div class="form-group">
          <label>Category</label>
          <select id="newCat"><option>Veg Pizzas</option><option>Non-Veg Pizzas</option><option>Cheese Pizzas</option><option>Special Pizzas</option></select>
        </div>
        <div class="form-group"><label>Pizza Name</label><input id="newName" placeholder="e.g. Paneer Makhani Pizza" /></div>
        <div class="form-group"><label>Price (₹)</label><input id="newPrice" placeholder="e.g. ₹269" /></div>
        <div class="form-group"><label>Description</label><input id="newDesc" placeholder="Toppings & crust details" /></div>
        <div class="form-group"><label>Image URL</label><input id="newImg" value="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500" /></div>
        <button class="btn-primary" style="width:100%; margin-bottom:16px;" onclick="addPizzaToDB()">Save Pizza to Supabase</button>

        <h4 style="margin-bottom:8px; color:#C8102E;">🗑️ Existing Menu Items</h4>
        <div id="adminDeleteList"></div>
      </div>

      <!-- Admin Tab 2: Live Orders -->
      <div id="admViewOrders" style="display:none;">
        <div id="adminOrdersList"><p style="color:#666;font-size:13px;">Loading live orders...</p></div>
      </div>

      <!-- Admin Tab 3: Customer Messages -->
      <div id="admViewMsgs" style="display:none;">
        <div id="adminMsgsList"><p style="color:#666;font-size:13px;">Loading customer inquiries...</p></div>
      </div>
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
  let selectedPaymentMethod = "UPI";
  let currentUser = null;
  let lastOrderId = null;
  let chatHistory = [];

  const SB_HEADERS = {
    "apikey": CFG.SUPABASE_KEY,
    "Authorization": `Bearer ${CFG.SUPABASE_KEY}`,
    "Content-Type": "application/json"
  };

  function showToast(msg, isError = false) {
    const t = document.getElementById("toast");
    t.style.background = isError ? "#C8102E" : "#1E8449";
    t.textContent = msg;
    t.style.display = "block";
    setTimeout(() => { t.style.display = "none"; }, 3500);
  }

  // ==================== NAVIGATION ====================
  function switchPage(pageName) {
    activePage = pageName;
    document.querySelectorAll(".page-view").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".nav-bar a").forEach(a => a.classList.remove("active"));
    document.getElementById("page-" + pageName)?.classList.add("active");
    document.getElementById("nav-" + pageName)?.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (pageName === "menu") renderFullMenu();
  }

  function goToMenuCategory(cat) { switchPage("menu"); setMenuCategory(cat); }
  function setMenuCategory(cat) {
    menuCategory = cat;
    document.querySelectorAll("#menuFilterPills .pill-tab").forEach(btn => {
      btn.classList.toggle("active", btn.textContent.includes(cat) || (cat === "All" && btn.textContent.includes("All")));
    });
    renderFullMenu();
  }
  function handleSearch() { if (activePage !== "menu") switchPage("menu"); renderFullMenu(); }

  // ==================== LIVE MENU FETCH ====================
  async function fetchLiveMenu() {
    try {
      const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/menu_items?select=*&order=id.asc`, { headers: SB_HEADERS });
      if (res.ok) {
        menuItems = await res.json();
        renderHomePopular();
        renderFullMenu();
        renderAdminDeleteList();
      }
    } catch (e) { console.error(e); }
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
      </div>`;
  }

  function renderHomePopular() {
    const grid = document.getElementById("homePizzaGrid");
    grid.innerHTML = menuItems.length
      ? menuItems.slice(0, 4).map(i => buildPizzaCardHTML(i, false)).join("")
      : `<p style="grid-column:1/-1;text-align:center;color:#666;">No pizzas found.</p>`;
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
    grid.innerHTML = filtered.length
      ? filtered.map(i => buildPizzaCardHTML(i, true)).join("")
      : `<p style="grid-column:1/-1;text-align:center;color:#666;">No pizzas match your filter.</p>`;
  }

  // ==================== CART & PAYMENT SELECTION ====================
  function parsePrice(str) {
    const num = parseFloat(String(str).replace(/[^0-9.]/g, ""));
    return isNaN(num) ? 0 : num;
  }

  function getCartFinalTotal() {
    const subtotal = cart.reduce((sum, e) => sum + parsePrice(e.item.pricing) * e.qty, 0);
    return discountApplied ? Math.round(subtotal * 0.8) : subtotal;
  }

  function updateCartBadge() {
    const totalCount = cart.reduce((sum, entry) => sum + entry.qty, 0);
    document.getElementById("cartBadge").textContent = totalCount;
  }

  function addToCart(id) {
    const found = menuItems.find(i => i.id === id);
    if (!found) return;
    const existing = cart.find(c => c.item.id === id);
    if (existing) existing.qty += 1;
    else cart.push({ item: found, qty: 1 });
    updateCartBadge();
    showToast(`Added ${found.name} to cart!`);
  }

  function changeQty(idx, delta) {
    cart[idx].qty += delta;
    if (cart[idx].qty <= 0) cart.splice(idx, 1);
    updateCartBadge();
    renderCart();
  }

  function claimPromoAndShop(code) {
    discountApplied = true;
    document.getElementById("promoInput").value = code;
    showToast(`Promo ${code} (20% OFF) activated!`);
    switchPage("menu");
  }

  function applyPromo() {
    const code = document.getElementById("promoInput").value.trim().toUpperCase();
    if (code === "BINGO20") {
      discountApplied = true;
      renderCart();
      showToast("20% OFF Promo Applied!");
    } else {
      showToast("Enter BINGO20 for 20% OFF", true);
    }
  }

  function selectPaymentMethod(method) {
    selectedPaymentMethod = method;
    const map = {
      "UPI": "upi",
      "Debit / Credit Card": "card",
      "Net Banking": "netbanking",
      "Cash on Delivery": "cod"
    };
    Object.values(map).forEach(key => {
      document.getElementById("payOpt-" + key).classList.remove("active");
      document.getElementById("payPanel-" + key).style.display = "none";
    });
    const activeKey = map[method];
    document.getElementById("payOpt-" + activeKey).classList.add("active");
    document.getElementById("payPanel-" + activeKey).style.display = "block";
    updatePayButtonText();
  }

  function updatePayButtonText() {
    const btn = document.getElementById("placeOrderBtn");
    if (!btn) return;
    const total = getCartFinalTotal();
    btn.textContent = (selectedPaymentMethod === "Cash on Delivery")
      ? `Confirm COD Order (₹${total})`
      : `Pay ₹${total} via ${selectedPaymentMethod}`;
  }

  function fillSampleUpi(handle) {
    const phone = document.getElementById("orderPhone").value.trim() || "9876543210";
    document.getElementById("upiIdInput").value = `${phone}@${handle}`;
  }

  function formatCardNumber(input) {
    const digits = input.value.replace(/\D/g, "").slice(0, 16);
    input.value = digits.replace(/(.{4})/g, "$1 ").trim();
  }

  function formatCardExpiry(input) {
    const digits = input.value.replace(/\D/g, "").slice(0, 4);
    input.value = digits.length >= 3 ? `${digits.slice(0, 2)}/${digits.slice(2)}` : digits;
  }

  function pickBank(bankName, el) {
    document.querySelectorAll(".bank-tile").forEach(t => t.classList.remove("active"));
    el.classList.add("active");
    document.getElementById("netBankSelect").value = bankName;
  }

  function renderCart() {
    const list = document.getElementById("cartItemsList");
    const checkoutSec = document.getElementById("checkoutSection");
    const totalBox = document.getElementById("cartTotalBox");
    document.getElementById("paymentProcessingBox").style.display = "none";
    document.getElementById("cartMainBody").style.display = "block";

    if (!cart.length) {
      list.innerHTML = `<p style="color:#666;font-size:13.5px;padding:12px 0;">Your cart is empty. Add pizzas from the Menu to order!</p>`;
      checkoutSec.style.display = "none";
      return;
    }

    checkoutSec.style.display = "block";
    if (currentUser) {
      if (!document.getElementById("orderName").value) document.getElementById("orderName").value = currentUser.full_name;
      if (!document.getElementById("orderPhone").value) document.getElementById("orderPhone").value = currentUser.phone;
    }

    let subtotal = 0;
    list.innerHTML = cart.map((entry, idx) => {
      const unitPrice = parsePrice(entry.item.pricing);
      subtotal += unitPrice * entry.qty;
      return `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #EEE;font-size:13px;">
          <div><strong>${entry.item.name}</strong><div style="color:#777;font-size:11.5px;">₹${unitPrice} each</div></div>
          <div style="display:flex;align-items:center;gap:8px;">
            <button class="qty-btn" onclick="changeQty(${idx}, -1)">–</button>
            <span><b>${entry.qty}</b></span>
            <button class="qty-btn" onclick="changeQty(${idx}, 1)">+</button>
            <span style="min-width:52px;text-align:right;font-weight:700;">₹${unitPrice * entry.qty}</span>
          </div>
        </div>`;
    }).join("");

    const finalTotal = getCartFinalTotal();
    totalBox.innerHTML = discountApplied
      ? `Subtotal: ₹${subtotal} → <span style="color:#1E8449;">20% OFF Total: ₹${finalTotal}</span>`
      : `Grand Total: ₹${finalTotal}`;
    updatePayButtonText();
  }

  function validatePaymentInputs() {
    if (selectedPaymentMethod === "UPI") {
      const upi = document.getElementById("upiIdInput").value.trim();
      if (!upi || !upi.includes("@")) {
        showToast("Please enter a valid UPI ID (e.g., name@okicici).", true);
        return null;
      }
      return `UPI (${upi})`;
    }
    if (selectedPaymentMethod === "Debit / Credit Card") {
      const num = document.getElementById("cardNumInput").value.replace(/\s/g, "");
      const holder = document.getElementById("cardNameInput").value.trim();
      const exp = document.getElementById("cardExpInput").value.trim();
      const cvv = document.getElementById("cardCvvInput").value.trim();
      if (num.length < 13 || !holder || exp.length < 4 || cvv.length < 3) {
        showToast("Please enter complete Card Number, Name, Expiry, and CVV.", true);
        return null;
      }
      return `Card (•••• ${num.slice(-4)})`;
    }
    if (selectedPaymentMethod === "Net Banking") {
      const bank = document.getElementById("netBankSelect").value;
      return `Net Banking (${bank})`;
    }
    return "Cash on Delivery";
  }

  async function placeOrder() {
    if (!cart.length) return;
    const cName = document.getElementById("orderName").value.trim();
    const cPhone = document.getElementById("orderPhone").value.trim();
    const cAddr = document.getElementById("orderAddress").value.trim();
    if (!cName || !cPhone || !cAddr) {
      showToast("Please fill in Name, Phone, and Delivery Address.", true);
      return;
    }

    const paymentLabel = validatePaymentInputs();
    if (!paymentLabel) return;

    const finalTotal = getCartFinalTotal();
    const itemsSummary = cart.map(e => `${e.qty}x ${e.item.name}`).join(", ");
    const orderCode = "BG-" + Math.floor(1000 + Math.random() * 9000);
    const isCOD = (selectedPaymentMethod === "Cash on Delivery");
    const txnId = isCOD
      ? "COD-" + Math.floor(100000 + Math.random() * 900000)
      : "TXN-" + Date.now().toString().slice(-8);
    const paymentStatus = isCOD ? "Pending (COD)" : "Paid";

    // Show interactive payment processing animation
    document.getElementById("cartMainBody").style.display = "none";
    document.getElementById("paymentProcessingBox").style.display = "block";
    document.getElementById("processingTitle").textContent = isCOD
      ? "Confirming Cash on Delivery Order..."
      : `Authorizing ₹${finalTotal} via ${selectedPaymentMethod}...`;

    await new Promise(r => setTimeout(r, isCOD ? 700 : 1500));

    const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/orders`, {
      method: "POST",
      headers: { ...SB_HEADERS, "Prefer": "return=minimal" },
      body: JSON.stringify({
        order_code: orderCode,
        customer_name: cName,
        customer_phone: cPhone,
        delivery_address: cAddr,
        items_summary: itemsSummary,
        total_amount: finalTotal,
        status: "Preparing in Oven",
        payment_method: paymentLabel,
        payment_status: paymentStatus,
        transaction_id: txnId
      })
    });

    if (res.ok) {
      lastOrderId = orderCode;
      cart = [];
      discountApplied = false;
      updateCartBadge();
      closeModal("cartModal");

      // Show Digital Payment Receipt Modal
      document.getElementById("receiptDetailsBox").innerHTML = `
        <div><strong>Order ID:</strong> ${orderCode}</div>
        <div><strong>Transaction ID:</strong> ${txnId}</div>
        <div><strong>Payment Method:</strong> ${paymentLabel}</div>
        <div><strong>Payment Status:</strong> <span class="${isCOD ? 'badge-cod' : 'badge-paid'}">${paymentStatus}</span></div>
        <div><strong>Amount:</strong> ₹${finalTotal}</div>
        <div><strong>Items:</strong> ${itemsSummary}</div>
        <div><strong>Deliver To:</strong> ${cName} (${cAddr})</div>
      `;
      openModal("receiptModal");
      appendChat("bot", `🎉 Order **${orderCode}** confirmed! Paid ₹${finalTotal} via **${paymentLabel}** (${paymentStatus}). Txn ID: \`${txnId}\`.`);
    } else {
      document.getElementById("paymentProcessingBox").style.display = "none";
      document.getElementById("cartMainBody").style.display = "block";
      showToast("Database error: Please run the Step 1 SQL to add payment columns.", true);
    }
  }

  // ==================== LOGIN / REGISTER ====================
  function switchAuthTab(mode) {
    document.getElementById("tabLoginBtn").classList.toggle("active", mode === "login");
    document.getElementById("tabRegBtn").classList.toggle("active", mode === "register");
    document.getElementById("loginFormBox").style.display = mode === "login" ? "block" : "none";
    document.getElementById("registerFormBox").style.display = mode === "register" ? "block" : "none";
  }

  function updateAuthUI() {
    const slot = document.getElementById("authHeaderSlot");
    if (currentUser) {
      slot.innerHTML = `
        <div class="user-pill">
          <span>👤 Hi, ${currentUser.full_name.split(" ")[0]}</span>
          <a href="#" onclick="logoutCustomer();return false;" style="color:#C8102E;font-size:11px;text-decoration:none;">Logout</a>
        </div>`;
      document.getElementById("contactName").value = currentUser.full_name;
      document.getElementById("contactEmail").value = currentUser.email;
    } else {
      slot.innerHTML = `<button class="btn-login" onclick="openModal('authModal')">👤 Login / Register</button>`;
    }
  }

  async function registerCustomer() {
    const full_name = document.getElementById("regName").value.trim();
    const email = document.getElementById("regEmail").value.trim().toLowerCase();
    const phone = document.getElementById("regPhone").value.trim();
    const password = document.getElementById("regPassword").value;
    if (!full_name || !email || !phone || !password) {
      showToast("All registration fields are required.", true);
      return;
    }

    const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/customers`, {
      method: "POST",
      headers: { ...SB_HEADERS, "Prefer": "return=representation" },
      body: JSON.stringify({ full_name, email, phone, password })
    });
    if (res.ok) {
      const rows = await res.json();
      currentUser = rows[0] || { full_name, email, phone };
      updateAuthUI();
      closeModal("authModal");
      showToast(`Welcome ${full_name}! Account created.`);
    } else {
      showToast("Registration failed (email may already exist).", true);
    }
  }

  async function loginCustomer() {
    const email = document.getElementById("loginEmail").value.trim().toLowerCase();
    const password = document.getElementById("loginPassword").value;
    if (!email || !password) {
      showToast("Enter email and password.", true);
      return;
    }
    const res = await fetch(
      `${CFG.SUPABASE_URL}/rest/v1/customers?email=eq.${encodeURIComponent(email)}&password=eq.${encodeURIComponent(password)}&select=*`,
      { headers: SB_HEADERS }
    );
    const rows = await res.json();
    if (rows && rows.length > 0) {
      currentUser = rows[0];
      updateAuthUI();
      closeModal("authModal");
      showToast(`Welcome back, ${currentUser.full_name}!`);
    } else {
      showToast("Invalid email or password.", true);
    }
  }

  function logoutCustomer() {
    currentUser = null;
    updateAuthUI();
    showToast("Logged out.");
  }

  // ==================== CONTACT -> SEND MESSAGE ====================
  async function submitContactForm() {
    const sender_name = document.getElementById("contactName").value.trim();
    const contact_info = document.getElementById("contactEmail").value.trim();
    const message = document.getElementById("contactMsg").value.trim();
    if (!sender_name || !contact_info || !message) {
      showToast("Please fill in Name, Phone/Email, and Message.", true);
      return;
    }
    const btn = document.getElementById("sendMsgBtn");
    btn.disabled = true; btn.textContent = "Sending...";
    try {
      const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/contact_messages`, {
        method: "POST",
        headers: { ...SB_HEADERS, "Prefer": "return=minimal" },
        body: JSON.stringify({ sender_name, contact_info, message })
      });
      if (res.ok) {
        document.getElementById("contactMsg").value = "";
        showToast("Message sent! Viewable in Store Admin → Customer Messages.");
      } else {
        showToast("Failed to send message.", true);
      }
    } finally {
      btn.disabled = false; btn.textContent = "Send Message";
    }
  }

  // ==================== STORE ADMIN ====================
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
      loadAdminOrders();
      loadAdminMessages();
    } else {
      showToast("Incorrect Admin Password.", true);
    }
  }

  function switchAdminTab(tab) {
    ["menu", "orders", "msgs"].forEach(t => {
      document.getElementById("admTab" + t.charAt(0).toUpperCase() + t.slice(1)).classList.toggle("active", t === tab);
      document.getElementById("admView" + t.charAt(0).toUpperCase() + t.slice(1)).style.display = (t === tab) ? "block" : "none";
    });
    if (tab === "orders") loadAdminOrders();
    if (tab === "msgs") loadAdminMessages();
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
      headers: { ...SB_HEADERS, "Prefer": "return=minimal" },
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
      </div>`).join("");
  }

  async function deletePizzaFromDB(id) {
    await fetch(`${CFG.SUPABASE_URL}/rest/v1/menu_items?id=eq.${id}`, { method: "DELETE", headers: SB_HEADERS });
    await fetchLiveMenu();
    showToast("Pizza deleted from database!");
  }

  async function loadAdminOrders() {
    const box = document.getElementById("adminOrdersList");
    const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/orders?select=*&order=id.desc`, { headers: SB_HEADERS });
    if (!res.ok) { box.innerHTML = "<p>Could not load orders.</p>"; return; }
    const orders = await res.json();
    if (!orders.length) { box.innerHTML = "<p style='font-size:13px;color:#666;'>No orders placed yet.</p>"; return; }

    box.innerHTML = orders.map(o => {
      const isPaid = (o.payment_status === "Paid");
      return `
      <div style="border:1px solid #EEE;border-radius:10px;padding:12px;margin-bottom:10px;font-size:12.5px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <strong>${o.order_code} — ${o.customer_name} (${o.customer_phone})</strong>
          <span style="color:#C8102E;font-weight:800;font-size:14px;">₹${o.total_amount}</span>
        </div>
        <div style="margin:5px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <span class="${isPaid ? 'badge-paid' : 'badge-cod'}">${o.payment_status || 'Pending'}</span>
          <span style="font-weight:600;color:#333;">${o.payment_method || 'Cash on Delivery'}</span>
          ${o.transaction_id ? `<span style="color:#777;font-size:11px;">(${o.transaction_id})</span>` : ''}
        </div>
        <div style="color:#444;margin:4px 0;">Items: ${o.items_summary}</div>
        <div style="color:#666;margin-bottom:8px;">Address: ${o.delivery_address}</div>
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <span>Order Status:</span>
          <select onchange="updateOrderStatus(${o.id}, this.value)" style="padding:4px 8px;border-radius:6px;border:1px solid #CCC;font-size:12px;">
            <option ${o.status==='Preparing in Oven'?'selected':''}>Preparing in Oven</option>
            <option ${o.status==='Out for Delivery'?'selected':''}>Out for Delivery</option>
            <option ${o.status==='Delivered'?'selected':''}>Delivered</option>
          </select>
          ${!isPaid ? `<button class="btn-add" style="background:#1E8449;" onclick="markOrderPaid(${o.id})">Mark COD Paid</button>` : ''}
        </div>
      </div>`;
    }).join("");
  }

  async function updateOrderStatus(orderId, newStatus) {
    await fetch(`${CFG.SUPABASE_URL}/rest/v1/orders?id=eq.${orderId}`, {
      method: "PATCH",
      headers: SB_HEADERS,
      body: JSON.stringify({ status: newStatus })
    });
    showToast(`Order status updated to: ${newStatus}`);
  }

  async function markOrderPaid(orderId) {
    await fetch(`${CFG.SUPABASE_URL}/rest/v1/orders?id=eq.${orderId}`, {
      method: "PATCH",
      headers: SB_HEADERS,
      body: JSON.stringify({ payment_status: "Paid" })
    });
    loadAdminOrders();
    showToast("Payment marked as Paid!");
  }

  async function loadAdminMessages() {
    const box = document.getElementById("adminMsgsList");
    const res = await fetch(`${CFG.SUPABASE_URL}/rest/v1/contact_messages?select=*&order=id.desc`, { headers: SB_HEADERS });
    if (!res.ok) { box.innerHTML = "<p>Could not load messages.</p>"; return; }
    const msgs = await res.json();
    if (!msgs.length) { box.innerHTML = "<p style='font-size:13px;color:#666;'>No customer messages yet.</p>"; return; }

    box.innerHTML = msgs.map(m => `
      <div style="border:1px solid #EEE;border-radius:10px;padding:10px;margin-bottom:10px;font-size:12.5px;">
        <strong>${m.sender_name}</strong> <span style="color:#777;">(${m.contact_info})</span>
        <p style="margin-top:4px;color:#222;">${m.message}</p>
      </div>`).join("");
  }

  // ==================== REAL-TIME CHATBOT ====================
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

    const [freshMenu, ordersRes] = await Promise.all([
      fetchLiveMenu(),
      fetch(`${CFG.SUPABASE_URL}/rest/v1/orders?select=order_code,customer_name,items_summary,total_amount,status,payment_method,payment_status,transaction_id&order=id.desc&limit=10`, { headers: SB_HEADERS })
    ]);
    const recentOrders = ordersRes.ok ? await ordersRes.json() : [];
    const menuContext = freshMenu.map(i => `- ${i.name} (${i.category}): ${i.pricing} — ${i.description || ''}`).join("\n");
    const ordersContext = recentOrders.map(o => `- ${o.order_code} (${o.customer_name}): ${o.items_summary} | ₹${o.total_amount} | Payment: ${o.payment_method} (${o.payment_status}, ${o.transaction_id || ''}) | Delivery Status: ${o.status}`).join("\n");

    const systemPrompt = `You are the friendly AI Assistant for Bingo & Gogo Pizza Shop.
LIVE MENU FROM SUPABASE:
${menuContext}

RECENT LIVE ORDERS:
${ordersContext || "No recent orders"}
CURRENT SESSION ORDER ID: ${lastOrderId || "None"}

OPERATIONS & OFFERS:
${CFG.OPS_TEXT}

POLICIES:
${CFG.POL_TEXT}

RULES:
1. Answer concisely using ONLY the live menu, live orders, offers, and policies above.
2. Format prices in Rupees (₹).
3. If asked to track an order, look up the matching Order ID in RECENT LIVE ORDERS and share both its delivery status and payment status.`;

    try {
      const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": `Bearer ${CFG.GROQ_API_KEY}`, "Content-Type": "application/json" },
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
