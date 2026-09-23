from collections import defaultdict
import json
from pathlib import Path
from flask import Flask, render_template_string

app = Flask(__name__)
DATA_FILE = Path(__file__).resolve().parent / "data" / "menu.json"


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
    
    <!-- Design Assets -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <style>
        :root {
            --primary-burgundy: #6B000B;
            --dark-burgundy: #420006;
            --accent-gold: #E5C158;
            --light-gold: #FFF9E6;
            --surface-bg: #F8F5EE;
            --card-border: #EFE8D8;
            --text-dark: #1E1E1E;
            --text-muted: #6C757D;
            --shadow-sm: 0 4px 12px rgba(0,0,0,0.03);
            --shadow-md: 0 8px 24px rgba(107, 0, 11, 0.08);
        }

        body {
            background-color: var(--surface-bg);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-dark);
            padding-bottom: 110px;
            -webkit-tap-highlight-color: transparent;
        }

        /* Hero Header */
        .hero-banner {
            background: linear-gradient(160deg, var(--dark-burgundy) 0%, var(--primary-burgundy) 100%);
            color: white;
            padding: 24px 18px 36px;
            border-radius: 0 0 30px 30px;
            position: relative;
            box-shadow: 0 10px 30px rgba(66, 0, 6, 0.3);
        }
        .hero-banner::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
        }
        .brand-header {
            font-family: 'Cinzel', serif;
            font-weight: 800;
            color: var(--accent-gold);
            font-size: 1.65rem;
            letter-spacing: 1px;
            margin: 0;
            text-shadow: 0 2px 6px rgba(0,0,0,0.5);
        }
        .status-pill {
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(229,193,88,0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            color: #FFF;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        /* Order Mode Switcher */
        .mode-container {
            margin-top: -22px;
            padding: 0 16px;
        }
        .mode-switch {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 5px;
            display: flex;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--card-border);
        }
        .mode-btn {
            flex: 1;
            text-align: center;
            text-decoration: none;
            padding: 10px 6px;
            border-radius: 14px;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-muted);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .mode-btn.active {
            background: linear-gradient(135deg, var(--primary-burgundy), var(--dark-burgundy));
            color: var(--accent-gold);
            box-shadow: 0 4px 14px rgba(107, 0, 11, 0.25);
        }

        /* Search Input */
        .search-box {
            position: relative;
            margin: 18px 0 12px;
        }
        .search-box input {
            background: #FFF;
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 12px 16px 12px 42px;
            font-size: 0.92rem;
            box-shadow: var(--shadow-sm);
        }
        .search-box input:focus {
            border-color: var(--accent-gold);
            box-shadow: 0 0 0 3px rgba(229,193,88,0.25);
            outline: none;
        }
        .search-box i {
            position: absolute;
            left: 15px; top: 50%;
            transform: translateY(-50%);
            color: #888;
        }

        /* Category Horizontal Scroll */
        .category-scroll-wrapper {
            position: sticky;
            top: 0;
            z-index: 1020;
            background: var(--surface-bg);
            padding: 10px 0;
            margin: 0 -12px 16px;
            border-bottom: 1px solid rgba(0,0,0,0.05);
            backdrop-filter: blur(10px);
        }
        .category-scroll {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 0 16px;
            scrollbar-width: none;
        }
        .category-scroll::-webkit-scrollbar { display: none; }
        .cat-chip {
            white-space: nowrap;
            padding: 8px 16px;
            border-radius: 20px;
            background: #FFF;
            border: 1px solid var(--card-border);
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-dark);
            text-decoration: none;
            transition: all 0.2s;
            box-shadow: var(--shadow-sm);
        }
        .cat-chip.active {
            background: var(--primary-burgundy);
            color: #FFF;
            border-color: var(--primary-burgundy);
        }

        /* Menu Items */
        .category-title {
            font-family: 'Cinzel', serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary-burgundy);
            margin: 24px 0 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .category-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--card-border);
        }

        .food-card {
            background: #FFF;
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 14px;
            border: 1px solid var(--card-border);
            box-shadow: var(--shadow-sm);
            display: flex;
            justify-content: space-between;
            gap: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .veg-icon {
            width: 16px; height: 16px;
            border: 2px solid #2E7D32;
            padding: 2px;
            display: inline-flex;
            align-items: center; justify-content: center;
            border-radius: 3px;
        }
        .veg-icon::after {
            content: '';
            width: 6px; height: 6px;
            background: #2E7D32;
            border-radius: 50%;
        }

        .popular-tag {
            font-size: 0.68rem;
            background: var(--light-gold);
            color: #8A6D00;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }

        .food-name {
            font-weight: 700;
            font-size: 1rem;
            color: #111;
            margin-top: 4px;
        }
        .food-desc {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 4px;
            line-height: 1.35;
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

        .add-btn {
            background: var(--light-gold);
            border: 1px solid var(--accent-gold);
            color: var(--primary-burgundy);
            font-weight: 700;
            font-size: 0.82rem;
            padding: 6px 18px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .add-btn:hover {
            background: var(--accent-gold);
            color: #000;
        }

        .qty-controls {
            display: none;
            align-items: center;
            background: var(--primary-burgundy);
            color: white;
            border-radius: 12px;
            padding: 3px;
        }
        .qty-btn {
            background: none;
            border: none;
            color: white;
            width: 26px; height: 26px;
            font-weight: 700;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer;
        }
        .qty-val {
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0 6px;
        }

        /* Floating Cart Bottom Bar */
        .cart-float-bar {
            position: fixed;
            bottom: 16px;
            left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 32px);
            max-width: 600px;
            background: linear-gradient(135deg, var(--dark-burgundy), var(--primary-burgundy));
            border: 1px solid var(--accent-gold);
            color: white;
            border-radius: 20px;
            padding: 12px 20px;
            display: none;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1030;
            transition: opacity 0.2s ease, transform 0.2s ease;
        }
        .view-cart-btn {
            background: var(--accent-gold);
            color: var(--dark-burgundy);
            border: none;
            font-weight: 800;
            font-size: 0.85rem;
            padding: 8px 16px;
            border-radius: 12px;
            cursor: pointer;
        }

        /* Slide-up Cart Offcanvas Drawer */
        .offcanvas-bottom {
            height: auto !important;
            max-height: 85vh;
            border-top-left-radius: 28px;
            border-top-right-radius: 28px;
            background: #FFF;
            z-index: 1060 !important;
        }
        .offcanvas-backdrop {
            z-index: 1050 !important;
        }
        .cart-modal-header {
            border-bottom: 1px solid var(--card-border);
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
            border-bottom: 1px dashed var(--card-border);
        }
        .bill-details {
            background: var(--surface-bg);
            border-radius: 16px;
            padding: 14px;
            margin-top: 16px;
        }
        .bill-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.88rem;
            margin-bottom: 6px;
            color: #555;
        }
        .bill-row.total {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--primary-burgundy);
            border-top: 1px solid var(--card-border);
            padding-top: 8px;
            margin-top: 8px;
        }
    </style>
</head>
<body>

<!-- Hero Banner -->
<div class="hero-banner text-center">
    <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="status-pill"><i class="bi bi-clock-fill text-warning"></i> Open • 11 AM - 11 PM</span>
        <span class="status-pill"><i class="bi bi-star-fill text-warning"></i> 4.8 (1.2k+)</span>
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

    <!-- Live Search -->
    <div class="search-box">
        <i class="bi bi-search"></i>
        <input type="text" id="searchInput" class="form-control" placeholder="Search dish name, dal, paneer..." onkeyup="filterMenu()">
    </div>

    <!-- Sticky Category Nav -->
    <div class="category-scroll-wrapper">
        <div class="category-scroll" id="categoryScroll">
            {% for category in categories.keys() %}
            <a href="#cat-{{ loop.index }}" class="cat-chip {{ 'active' if loop.first else '' }}">{{ category }}</a>
            {% endfor %}
        </div>
    </div>

    <!-- Menu Items -->
    <div id="menuContainer">
        {% for category, items in categories.items() %}
        <div class="category-group" id="cat-{{ loop.index }}">
            <div class="category-title">
                <span>{{ category }}</span>
                <span class="badge bg-light text-dark fs-6 font-monospace" style="border:1px solid #ddd;">{{ items|length }}</span>
            </div>

            {% for item in items %}
            <div class="food-card" data-id="{{ item.item_name | lower | replace(' ', '-') }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center gap-2">
                        <span class="veg-icon"></span>
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
        {% endfor %}
    </div>

</div>

<!-- Floating Cart Bottom Bar -->
<div class="cart-float-bar" id="cartBar">
    <div>
        <div class="fw-bold" id="cartCount">0 ITEMS SELECTED</div>
        <div class="small opacity-75" id="cartTotal">Total: ₹0</div>
    </div>
    <button class="view-cart-btn" data-bs-toggle="offcanvas" data-bs-target="#cartModal">VIEW ORDER <i class="bi bi-arrow-right"></i></button>
</div>

<!-- Slide-Up View Cart Drawer / Modal -->
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
                <span>Taxes & Service Charge (5%)</span>
                <span id="billTax">₹0</span>
            </div>
            <div class="bill-row total">
                <span>Grand Total</span>
                <span id="billGrandTotal">₹0</span>
            </div>
        </div>

        <div class="mt-4 d-flex gap-2">
            <button class="btn btn-outline-secondary flex-grow-1 py-2 fw-semibold" onclick="clearCart()" style="border-radius: 12px;">Clear Cart</button>
            <button class="btn text-white py-2 fw-bold" style="background: var(--primary-burgundy); border-radius: 12px; flex:2;" onclick="placeOrder()">Place Order <i class="bi bi-check-circle-fill ms-1"></i></button>
        </div>
    </div>
</div>

<!-- Bootstrap 5 JS Bundle -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<script>
    // Cart Data Object
    let cart = {};

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
                    <div class="fw-bold">${item.name}</div>
                    <small class="text-muted">₹${item.price} x ${item.count}</small>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="fw-bold text-dark">₹${itemTotal}</span>
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
        alert('🎉 Order successfully placed! Thank you for ordering at Vrindavan Dhaba.');
        clearCart();
    }

    function filterMenu() {
        let query = document.getElementById('searchInput').value.toLowerCase();
        let cards = document.querySelectorAll('.food-card');
        let groups = document.querySelectorAll('.category-group');

        cards.forEach(card => {
            let name = card.getAttribute('data-name').toLowerCase();
            if (name.includes(query)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        groups.forEach(group => {
            let visibleCards = group.querySelectorAll('.food-card[style*="display: flex"]');
            if (query !== '' && visibleCards.length === 0) {
                group.style.display = 'none';
            } else {
                group.style.display = 'block';
            }
        });
    }

    // Hide/Show bottom bar when cart offcanvas opens/closes
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
    app.run(host="0.0.0.0", port=5002, debug=True)
