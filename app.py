from collections import defaultdict
import json
from pathlib import Path
from flask import Flask, render_template_string

app = Flask(__name__)

# Base directory setup for local and serverless deployments (Vercel)
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "menu.json"


def load_menu():
    if not DATA_FILE.exists():
        return [
            {
                "item_name": "Paneer Butter Masala",
                "category": "Paneer Se Paneer Tak",
                "description": "Rich tomato, cashew & butter gravy with soft cottage cheese cubes.",
                "dine_in_price": 280,
                "pickup_price": 290,
                "online_price": 310,
                "dine_in_active": True,
                "pickup_active": True,
                "online_active": True,
                "is_active": True,
                "is_veg": True,
                "popular": True,
            },
            {
                "item_name": "Dal Makhani Handi",
                "category": "Sabiziyaan",
                "description": "Slow-cooked black lentils simmered overnight with butter & cream.",
                "dine_in_price": 240,
                "pickup_price": 250,
                "online_price": 270,
                "dine_in_active": True,
                "pickup_active": True,
                "online_active": True,
                "is_active": True,
                "is_veg": True,
                "popular": True,
            },
            {
                "item_name": "Crispy Veg Manchurian",
                "category": "Starters",
                "description": "Crispy vegetable dumplings tossed in spicy Indo-Chinese sauces.",
                "dine_in_price": 210,
                "pickup_price": 220,
                "online_price": 240,
                "dine_in_active": True,
                "pickup_active": True,
                "online_active": True,
                "is_active": True,
                "is_veg": True,
                "popular": False,
            },
            {
                "item_name": "Butter Naan",
                "category": "Roti & Naan",
                "description": "Traditional clay-oven tandoori naan brushed with fresh butter.",
                "dine_in_price": 50,
                "pickup_price": 50,
                "online_price": 60,
                "dine_in_active": True,
                "pickup_active": True,
                "online_active": True,
                "is_active": True,
                "is_veg": True,
                "popular": False,
            },
        ]
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_menu(order_type):
    fields = {
        "dinein": ("dine_in_price", "dine_in_active"),
        "parcel": ("pickup_price", "pickup_active"),
        "online": ("online_price", "online_active"),
    }
    price_field, active_field = fields[order_type]
    categories = defaultdict(list)

    for item in load_menu():
        if not item.get("is_active", True) or not item.get(active_field, True):
            continue
        price = item.get(price_field)
        if price is None or float(price) <= 0:
            continue
        categories[item.get("category", "Other")].append(
            {
                "item_name": item.get("item_name", ""),
                "category": item.get("category", "Other"),
                "description": item.get("description", ""),
                "price": float(price),
                "is_veg": item.get("is_veg", True),
                "popular": item.get("popular", False),
            }
        )
    return categories


MENU_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ title }} | Vrindavan Dhaba</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    
    <!-- Fonts & CSS Libraries -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <style>
        :root {
            /* Royal Indian Dining Theme (Burgundy, Gold, Amber, Warm Sand) */
            --bg-warm-sand: #FDFBF7;
            --primary-burgundy: #4A0E17;
            --deep-burgundy: #33080E;
            --accent-amber: #C86A28;
            --metallic-gold: #D4AF37;
            
            /* Derived Tints & Elements */
            --card-bg: #FFFFFF;
            --text-main: #2C1810;
            --text-muted: #7A6258;
            --soft-amber-bg: #FFF5EC;
            --soft-gold-bg: #FAF5E8;
            --shadow-subtle: 0 4px 18px rgba(74, 14, 23, 0.06);
            --shadow-elevated: 0 10px 28px rgba(51, 8, 14, 0.16);
        }

        body {
            background-color: var(--bg-warm-sand);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-main);
            padding-bottom: 110px;
            -webkit-tap-highlight-color: transparent;
        }

        /* Hero Header (Imperial Burgundy & Gold Theme) */
        .hero-banner {
            background: linear-gradient(135deg, var(--deep-burgundy) 0%, var(--primary-burgundy) 100%);
            color: #FFFFFF;
            padding: 28px 20px 32px;
            border-radius: 0 0 24px 24px;
            position: relative;
            box-shadow: var(--shadow-elevated);
        }
        .hero-banner::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--metallic-gold) 0%, var(--accent-amber) 100%);
        }
        .brand-header {
            font-family: 'Cinzel', serif;
            font-weight: 900;
            color: var(--metallic-gold);
            font-size: 1.8rem;
            letter-spacing: 1.2px;
            margin: 0;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
        }
        .status-pill {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(212, 175, 55, 0.4);
            padding: 5px 14px;
            border-radius: 30px;
            font-size: 0.78rem;
            color: #FFF5EC;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
        }

        /* Mode Selector Switch */
        .mode-container {
            margin-top: -22px;
            padding: 0 12px;
            position: relative;
            z-index: 10;
        }
        .mode-switch {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 6px;
            display: flex;
            box-shadow: var(--shadow-elevated);
            border: 1.5px solid var(--metallic-gold);
        }
        .mode-btn {
            flex: 1;
            text-align: center;
            text-decoration: none;
            padding: 10px 8px;
            border-radius: 14px;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--primary-burgundy);
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .mode-btn.active {
            background: var(--primary-burgundy);
            color: var(--metallic-gold);
            box-shadow: 0 4px 12px rgba(74, 14, 23, 0.3);
        }

        /* Search Input */
        .search-box {
            position: relative;
            margin: 20px 0 14px;
        }
        .search-box input {
            background: #FFFFFF;
            border: 1.5px solid rgba(212, 175, 55, 0.5);
            border-radius: 18px;
            padding: 12px 16px 12px 44px;
            font-size: 0.92rem;
            color: var(--text-main);
            box-shadow: var(--shadow-subtle);
            transition: all 0.2s ease;
        }
        .search-box input::placeholder {
            color: var(--text-muted);
            opacity: 0.7;
        }
        .search-box input:focus {
            border-color: var(--accent-amber);
            box-shadow: 0 0 0 4px rgba(200, 106, 40, 0.18);
            outline: none;
        }
        .search-box i {
            position: absolute;
            left: 16px; top: 50%;
            transform: translateY(-50%);
            color: var(--accent-amber);
            font-size: 1.05rem;
        }

        /* Category Horizontal Scroll */
        .category-scroll-wrapper {
            position: sticky;
            top: 0;
            z-index: 1020;
            background: rgba(253, 251, 247, 0.96);
            padding: 10px 0;
            margin: 0 -12px 16px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.25);
            backdrop-filter: blur(12px);
        }
        .category-scroll {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 0 16px;
            scrollbar-width: none;
            scroll-behavior: smooth;
        }
        .category-scroll::-webkit-scrollbar { display: none; }
        .cat-chip {
            white-space: nowrap;
            padding: 8px 18px;
            border-radius: 20px;
            background: #FFFFFF;
            border: 1.5px solid rgba(212, 175, 55, 0.6);
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--primary-burgundy);
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-subtle);
        }
        .cat-chip.active {
            background: var(--accent-amber);
            color: #FFFFFF;
            border-color: var(--accent-amber);
        }

        /* Accordion Customization */
        .accordion-item {
            background: transparent;
            border: none;
            margin-bottom: 16px;
        }
        .accordion-button {
            background: #FFFFFF;
            border: 1.5px solid rgba(212, 175, 55, 0.5);
            border-radius: 18px !important;
            font-family: 'Cinzel', serif;
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--primary-burgundy);
            box-shadow: var(--shadow-subtle);
            padding: 16px 20px;
        }
        .accordion-button:not(.collapsed) {
            background: var(--soft-gold-bg);
            color: var(--primary-burgundy);
            box-shadow: none;
        }

        .cat-count-badge {
            background: var(--primary-burgundy);
            color: var(--metallic-gold);
            font-size: 0.75rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 12px;
        }

        .accordion-body {
            padding: 12px 0 0 0;
        }

        /* Food Cards */
        .food-card {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(212, 175, 55, 0.3);
            box-shadow: var(--shadow-subtle);
            display: flex;
            justify-content: space-between;
            gap: 14px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        /* Food Veg/Non-Veg Indicators */
        .food-type-icon {
            width: 16px; height: 16px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center; justify-content: center;
            padding: 2px;
            flex-shrink: 0;
        }
        .food-type-icon.veg { border: 2px solid #2E7D32; }
        .food-type-icon.veg::after {
            content: '';
            width: 6px; height: 6px;
            background: #2E7D32;
            border-radius: 50%;
        }
        .food-type-icon.nonveg { border: 2px solid #C62828; }
        .food-type-icon.nonveg::after {
            content: '';
            width: 0; height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 7px solid #C62828;
        }

        .popular-tag {
            font-size: 0.68rem;
            background: var(--soft-amber-bg);
            color: var(--accent-amber);
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            border: 1px solid rgba(200, 106, 40, 0.3);
        }

        .food-name {
            font-weight: 700;
            font-size: 0.98rem;
            color: var(--primary-burgundy);
            margin-top: 4px;
        }
        .food-desc {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 4px;
            line-height: 1.4;
        }

        .card-action-side {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: flex-end;
            min-width: 90px;
        }
        .price-text {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--primary-burgundy);
        }

        /* Controls */
        .add-btn {
            background: var(--soft-amber-bg);
            border: 1.5px solid var(--accent-amber);
            color: var(--accent-amber);
            font-weight: 800;
            font-size: 0.82rem;
            padding: 6px 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .add-btn:active {
            transform: scale(0.95);
        }

        .qty-controls {
            display: none;
            align-items: center;
            background: var(--primary-burgundy);
            color: white;
            border-radius: 12px;
            padding: 2px;
            box-shadow: 0 4px 10px rgba(74, 14, 23, 0.2);
        }
        .qty-btn {
            background: none;
            border: none;
            color: var(--metallic-gold);
            width: 28px; height: 28px;
            font-weight: 800;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer;
        }
        .qty-val {
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0 6px;
            color: #FFFFFF;
        }

        /* Floating Cart Bottom Bar */
        .cart-float-bar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 32px);
            max-width: 600px;
            background: var(--primary-burgundy);
            border: 1.5px solid var(--metallic-gold);
            color: white;
            border-radius: 20px;
            padding: 12px 20px;
            display: none;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-elevated);
            z-index: 1030;
        }
        .view-cart-btn {
            background: var(--accent-amber);
            color: #FFFFFF;
            border: none;
            font-weight: 800;
            font-size: 0.85rem;
            padding: 8px 18px;
            border-radius: 12px;
            cursor: pointer;
        }

        /* Slide-up Cart Offcanvas Drawer */
        .offcanvas-bottom {
            height: auto !important;
            max-height: 85vh;
            border-top-left-radius: 28px;
            border-top-right-radius: 28px;
            background: var(--bg-warm-sand);
            z-index: 1060 !important;
        }
        .cart-modal-header {
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
            padding: 18px 20px;
        }
        .cart-modal-body {
            padding: 16px 20px 30px;
            overflow-y: auto;
            max-height: calc(85vh - 70px);
        }
        .cart-item-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px dashed rgba(212, 175, 55, 0.4);
        }
        .bill-details {
            background: #FFFFFF;
            border: 1px solid rgba(212, 175, 55, 0.5);
            border-radius: 16px;
            padding: 16px;
            margin-top: 16px;
        }
        .bill-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.88rem;
            margin-bottom: 8px;
            color: var(--text-muted);
        }
        .bill-row.total {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--primary-burgundy);
            border-top: 1px solid rgba(212, 175, 55, 0.3);
            padding-top: 10px;
            margin-top: 10px;
            margin-bottom: 0;
        }
        .no-results {
            display: none;
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

<!-- Hero Banner -->
<div class="hero-banner text-center">
    <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="status-pill"><i class="bi bi-clock-fill me-1"></i> Open • 11 AM - 01 AM</span>
        <span class="status-pill"><i class="bi bi-star-fill me-1" style="color: var(--metallic-gold);"></i> 4.9 (8.2k+)</span>
    </div>
    <h1 class="brand-header">🛕 VRINDAVAN DHABA</h1>
    <p class="small text-white-50 m-0 mt-1">Authentic Pure Vegetarian Culinary Experience</p>
</div>

<div class="container" style="max-width: 640px;">

    <!-- Order Mode Switcher -->
    <div class="mode-container">
        <div class="mode-switch">
            <a href="/dinein" class="mode-btn {{ 'active' if order_type=='dinein' else '' }}">
                <i class="bi bi-shop"></i> Dine In
            </a>
            <a href="/parcel" class="mode-btn {{ 'active' if order_type=='parcel' else '' }}">
                <i class="bi bi-bag-check"></i> Parcel
            </a>
            <a href="/online" class="mode-btn {{ 'active' if order_type=='online' else '' }}">
                <i class="bi bi-moped"></i> Online
            </a>
        </div>
    </div>

    <!-- Search Box -->
    <div class="search-box">
        <i class="bi bi-search"></i>
        <input type="text" id="searchInput" class="form-control" placeholder="Search dish name, dal, paneer..." onkeyup="filterMenu()">
    </div>

    <!-- Sticky Category Navigation -->
    <div class="category-scroll-wrapper">
        <div class="category-scroll" id="categoryScroll">
            {% for category in categories.keys() %}
            <a href="#cat-{{ loop.index }}" class="cat-chip {{ 'active' if loop.first else '' }}" onclick="setActiveChip(this)">{{ category }}</a>
            {% endfor %}
        </div>
    </div>

    <!-- Menu Items -->
    <div class="accordion" id="menuAccordion">
        {% for category, items in categories.items() %}
        <div class="accordion-item category-group" id="cat-{{ loop.index }}">
            <h2 class="accordion-header" id="heading-{{ loop.index }}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{{ loop.index }}" aria-expanded="true" aria-controls="collapse-{{ loop.index }}">
                    <span class="cat-count-badge me-2">{{ items|length }}</span>
                    <span class="me-auto">{{ category }}</span>
                </button>
            </h2>
            <div id="collapse-{{ loop.index }}" class="accordion-collapse collapse show" aria-labelledby="heading-{{ loop.index }}">
                <div class="accordion-body">
                    {% for item in items %}
                    <div class="food-card" data-id="{{ item.item_name | lower | replace(' ', '-') }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center gap-2">
                                <span class="food-type-icon {{ 'veg' if item.is_veg else 'nonveg' }}"></span>
                                {% if item.popular %}
                                <span class="popular-tag"><i class="bi bi-fire"></i> Bestseller</span>
                                {% endif %}
                            </div>
                            <div class="food-name">{{ item.item_name }}</div>
                            <div class="food-desc">{{ item.description or 'Prepared with fresh ingredients and authentic dhaba spices.' }}</div>
                        </div>

                        <div class="card-action-side">
                            <div class="price-text">₹{{ "%.0f"|format(item.price) }}</div>
                            
                            <button class="add-btn" onclick="updateQty('{{ item.item_name | lower | replace(' ', '-') }}', '{{ item.item_name }}', {{ item.price }}, 1)">ADD</button>
                            <div class="qty-controls" id="qty-ctrl-{{ item.item_name | lower | replace(' ', '-') }}">
                                <button class="qty-btn" onclick="updateQty('{{ item.item_name | lower | replace(' ', '-') }}', '{{ item.item_name }}', {{ item.price }}, -1)">-</button>
                                <span class="qty-val" id="qty-val-{{ item.item_name | lower | replace(' ', '-') }}">1</span>
                                <button class="qty-btn" onclick="updateQty('{{ item.item_name | lower | replace(' ', '-') }}', '{{ item.item_name }}', {{ item.price }}, 1)">+</button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Empty Search Results State -->
    <div class="no-results" id="noResults">
        <i class="bi bi-search-heart display-4 text-muted"></i>
        <h6 class="mt-3 font-semibold">No matching dishes found</h6>
        <p class="small">Try searching for something else like 'Paneer' or 'Naan'.</p>
    </div>

</div>

<!-- Floating Cart Bottom Bar -->
<div class="cart-float-bar" id="cartBar">
    <div>
        <div class="fw-bold" id="cartCount">0 ITEMS SELECTED</div>
        <div class="small opacity-75" id="cartTotal">Total: ₹0</div>
    </div>
    <button class="view-cart-btn" data-bs-toggle="offcanvas" data-bs-target="#cartModal">VIEW ORDER <i class="bi bi-arrow-right ms-1"></i></button>
</div>

<!-- Slide-Up View Cart Drawer -->
<div class="offcanvas offcanvas-bottom" tabindex="-1" id="cartModal">
    <div class="cart-modal-header d-flex justify-content-between align-items-center">
        <div>
            <h5 class="m-0 fw-bold" style="color: var(--primary-burgundy); font-family: 'Cinzel', serif;">Your Order Cart</h5>
            <small class="text-muted">Order Mode: <b class="text-capitalize">{{ order_type }}</b></small>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
    </div>
    <div class="cart-modal-body">
        <div id="cartItemsList">
            <!-- Dynamically populated via JS -->
        </div>

        <div class="bill-details">
            <div class="bill-row">
                <span>Items Subtotal</span>
                <span id="billSubtotal">₹0</span>
            </div>
            <div class="bill-row">
                <span>Taxes & Charges (5%)</span>
                <span id="billTax">₹0</span>
            </div>
            <div class="bill-row total">
                <span>Grand Total</span>
                <span id="billGrandTotal">₹0</span>
            </div>
        </div>

        <div class="mt-4 d-flex gap-2">
            <button class="btn btn-outline-secondary flex-grow-1 py-2 fw-semibold" onclick="clearCart()" style="border-radius: 12px; border-color: rgba(212, 175, 55, 0.6);">Clear Cart</button>
            <button class="btn text-white py-2 fw-bold" style="background: var(--primary-burgundy); border-radius: 12px; flex:2;" onclick="placeOrder()">Place Order <i class="bi bi-check-circle-fill ms-1"></i></button>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<script>
    let cart = {};

    function setActiveChip(element) {
        document.querySelectorAll('.cat-chip').forEach(chip => chip.classList.remove('active'));
        element.classList.add('active');
    }

    function updateQty(id, name, price, change) {
        if (!cart[id]) {
            cart[id] = { id: id, name: name, price: price, count: 0 };
        }

        cart[id].count += change;

        if (cart[id].count <= 0) {
            delete cart[id];
        }

        syncUI(id);
        renderCartBar();
        renderCartModal();
    }

    function syncUI(id) {
        const card = document.querySelector(`.food-card[data-id="${id}"]`);
        const qtyCtrl = document.getElementById(`qty-ctrl-${id}`);
        const qtyVal = document.getElementById(`qty-val-${id}`);
        
        if (!card) return;

        const addBtn = card.querySelector('.add-btn');

        if (cart[id] && cart[id].count > 0) {
            addBtn.style.display = 'none';
            qtyCtrl.style.display = 'flex';
            qtyVal.innerText = cart[id].count;
        } else {
            addBtn.style.display = 'block';
            qtyCtrl.style.display = 'none';
        }
    }

    function renderCartBar() {
        let totalItems = 0;
        let totalPrice = 0;

        for (let key in cart) {
            totalItems += cart[key].count;
            totalPrice += cart[key].count * cart[key].price;
        }

        const bar = document.getElementById('cartBar');
        const cartModal = document.getElementById('cartModal');
        const isOpen = cartModal.classList.contains('show');

        if (totalItems > 0 && !isOpen) {
            bar.style.display = 'flex';
            document.getElementById('cartCount').innerText = `${totalItems} ITEM${totalItems > 1 ? 'S' : ''} ADDED`;
            document.getElementById('cartTotal').innerText = `Total: ₹${totalPrice.toFixed(0)}`;
        } else {
            bar.style.display = 'none';
            if (totalItems === 0) {
                const bsOffcanvas = bootstrap.Offcanvas.getInstance(cartModal);
                if(bsOffcanvas) bsOffcanvas.hide();
            }
        }
    }

    function renderCartModal() {
        const listContainer = document.getElementById('cartItemsList');
        listContainer.innerHTML = '';

        let subtotal = 0;

        for (let id in cart) {
            const item = cart[id];
            const itemTotal = item.count * item.price;
            subtotal += itemTotal;

            const row = document.createElement('div');
            row.className = 'cart-item-row';
            row.innerHTML = `
                <div>
                    <div class="fw-bold" style="color: var(--primary-burgundy);">${item.name}</div>
                    <small class="text-muted">₹${item.price} x ${item.count}</small>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="fw-bold" style="color: var(--primary-burgundy);">₹${itemTotal}</span>
                    <div class="qty-controls" style="display: flex;">
                        <button class="qty-btn" onclick="updateQty('${item.id}', '${item.name}', ${item.price}, -1)">-</button>
                        <span class="qty-val">${item.count}</span>
                        <button class="qty-btn" onclick="updateQty('${item.id}', '${item.name}', ${item.price}, 1)">+</button>
                    </div>
                </div>
            `;
            listContainer.appendChild(row);
        }

        const tax = subtotal * 0.05;
        const grandTotal = subtotal + tax;

        document.getElementById('billSubtotal').innerText = `₹${subtotal.toFixed(0)}`;
        document.getElementById('billTax').innerText = `₹${tax.toFixed(0)}`;
        document.getElementById('billGrandTotal').innerText = `₹${grandTotal.toFixed(0)}`;
    }

    function clearCart() {
        for (let id in cart) {
            delete cart[id];
            syncUI(id);
        }
        renderCartBar();
    }

    function placeOrder() {
        alert('Do Call 9713009097 To Place Order successfully! Thank you for ordering at Vrindavan Dhaba.');
        clearCart();
    }

    function filterMenu() {
        let query = document.getElementById('searchInput').value.toLowerCase().trim();
        let cards = document.querySelectorAll('.food-card');
        let groups = document.querySelectorAll('.category-group');
        let anyVisible = false;

        cards.forEach(card => {
            let name = card.getAttribute('data-name').toLowerCase();
            if (name.includes(query)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        groups.forEach(group => {
            let collapseEl = group.querySelector('.accordion-collapse');
            let bsCollapse = bootstrap.Collapse.getInstance(collapseEl);
            if (!bsCollapse) {
                bsCollapse = new bootstrap.Collapse(collapseEl, { toggle: false });
            }

            let visibleCards = group.querySelectorAll('.food-card[style*="display: flex"]');
            if (query !== '') {
                if (visibleCards.length === 0) {
                    group.style.display = 'none';
                } else {
                    group.style.display = 'block';
                    bsCollapse.show();
                    anyVisible = true;
                }
            } else {
                group.style.display = 'block';
                anyVisible = true;
            }
        });

        document.getElementById('noResults').style.display = (query !== '' && !anyVisible) ? 'block' : 'none';
    }

    document.addEventListener('DOMContentLoaded', () => {
        const cartModal = document.getElementById('cartModal');
        const cartBar = document.getElementById('cartBar');

        cartModal.addEventListener('show.bs.offcanvas', () => {
            cartBar.style.display = 'none';
        });

        cartModal.addEventListener('hidden.bs.offcanvas', () => {
            renderCartBar();
        });
    });
</script>

</body>
</html>"""


def render_menu(order_type, title):
    return render_template_string(
        MENU_TEMPLATE,
        categories=build_menu(order_type),
        order_type=order_type,
        title=title,
    )


@app.route("/")
def home():
    return render_menu("dinein", "Dine In")


@app.route("/dinein")
def dinein():
    return render_menu("dinein", "Dine In")


@app.route("/parcel")
def parcel():
    return render_menu("parcel", "Parcel")


@app.route("/online")
def online():
    return render_menu("online", "Online")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5022, debug=True)
