from collections import defaultdict
import json
from pathlib import Path
import re
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "menu.json"

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", str(text).lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")

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
                "popular": True
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
                "popular": True
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
                "popular": False
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
                "popular": False
            }
        ]
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_menu(order_type):
    fields = {
        "dinein": ("dine_in_price", "dine_in_active"),
        "parcel": ("pickup_price", "pickup_active"),
        "online": ("online_price", "online_active")
    }
    if order_type not in fields:
        order_type = "parcel"
    price_field, active_field = fields[order_type]
    categories = defaultdict(list)
    for item in load_menu():
        if not item.get("is_active", True):
            continue
        if not item.get(active_field, True):
            continue
        price = item.get(price_field)
        if price is None or float(price) <= 0:
            continue
        item_copy = dict(item)
        item_copy["slug"] = slugify(item.get("item_name", ""))
        item_copy["price"] = float(price)
        categories[item.get("category", "Other")].append(item_copy)
    return categories

MENU_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{{ title }} | Vrindavan Dhaba</title>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
:root{
--bg:#FDFBF7;
--primary:#4A0E17;
--deep:#33080E;
--amber:#C86A28;
--gold:#D4AF37;
--green:#25D366;
--text:#2C1810;
--muted:#7A6258;
--soft:#FFF5EC;
--goldbg:#FAF5E8;
--shadow:0 4px 18px rgba(74,14,23,.06);
--elevated:0 10px 28px rgba(51,8,14,.16)
}
body{
background:var(--bg);
font-family:'Plus Jakarta Sans',sans-serif;
color:var(--text);
padding-bottom:110px;
-webkit-tap-highlight-color:transparent
}
.hero-banner{
background:linear-gradient(135deg,var(--deep),var(--primary));
color:#fff;
padding:28px 20px 32px;
border-radius:0 0 24px 24px;
position:relative;
box-shadow:var(--elevated)
}
.hero-banner:after{
content:'';
position:absolute;
bottom:0;
left:0;
right:0;
height:3px;
background:linear-gradient(90deg,var(--gold),var(--amber))
}
.brand-header{
font-family:'Cinzel',serif;
font-weight:900;
color:var(--gold);
font-size:1.8rem;
letter-spacing:1.2px;
margin:0;
text-shadow:0 2px 6px rgba(0,0,0,.4)
}
.status-pill{
background:rgba(255,255,255,.12);
backdrop-filter:blur(8px);
border:1px solid rgba(212,175,55,.4);
padding:5px 14px;
border-radius:30px;
font-size:.78rem;
color:#FFF5EC;
display:inline-flex;
align-items:center;
gap:6px;
font-weight:600
}
.mode-container{
margin-top:-22px;
padding:0 12px;
position:relative;
z-index:10
}
.mode-switch{
background:#fff;
border-radius:20px;
padding:6px;
display:flex;
box-shadow:var(--elevated);
border:1.5px solid var(--gold)
}
.mode-btn{
flex:1;
text-align:center;
text-decoration:none;
padding:10px 8px;
border-radius:14px;
font-size:.85rem;
font-weight:700;
color:var(--primary);
display:flex;
align-items:center;
justify-content:center;
gap:6px
}
.mode-btn.active{
background:var(--primary);
color:var(--gold);
box-shadow:0 4px 12px rgba(74,14,23,.3)
}
.search-box{
position:relative;
margin:20px 0 14px
}
.search-box input{
background:#fff;
border:1.5px solid rgba(212,175,55,.5);
border-radius:18px;
padding:12px 16px 12px 44px;
font-size:.92rem;
color:var(--text);
box-shadow:var(--shadow)
}
.search-box input:focus{
border-color:var(--amber);
box-shadow:0 0 0 4px rgba(200,106,40,.18);
outline:none
}
.search-box i{
position:absolute;
left:16px;
top:50%;
transform:translateY(-50%);
color:var(--amber);
font-size:1.05rem
}
.category-scroll-wrapper{
position:sticky;
top:0;
z-index:1020;
background:rgba(253,251,247,.96);
padding:10px 0;
margin:0 -12px 16px;
border-bottom:1px solid rgba(212,175,55,.25);
backdrop-filter:blur(12px)
}
.category-scroll{
display:flex;
gap:8px;
overflow-x:auto;
padding:0 16px;
scrollbar-width:none;
scroll-behavior:smooth
}
.category-scroll::-webkit-scrollbar{display:none}
.cat-chip{
white-space:nowrap;
padding:8px 18px;
border-radius:20px;
background:#fff;
border:1.5px solid rgba(212,175,55,.6);
font-size:.82rem;
font-weight:700;
color:var(--primary);
text-decoration:none;
box-shadow:var(--shadow)
}
.cat-chip.active{
background:var(--amber);
color:#fff;
border-color:var(--amber)
}
.accordion-item{
background:transparent;
border:none;
margin-bottom:16px
}
.accordion-button{
background:#fff;
border:1.5px solid rgba(212,175,55,.5);
border-radius:18px!important;
font-family:'Cinzel',serif;
font-size:1.05rem;
font-weight:800;
color:var(--primary);
box-shadow:var(--shadow);
padding:16px 20px
}
.accordion-button:not(.collapsed){
background:var(--goldbg);
color:var(--primary);
box-shadow:none
}
.cat-count-badge{
background:var(--primary);
color:var(--gold);
font-size:.75rem;
font-weight:800;
padding:4px 10px;
border-radius:12px
}
.accordion-body{padding:12px 0 0}
.food-card{
background:#fff;
border-radius:18px;
padding:14px;
margin-bottom:10px;
border:1px solid rgba(212,175,55,.3);
box-shadow:var(--shadow);
display:flex;
justify-content:space-between;
gap:10px
}
.food-type-icon{
width:16px;
height:16px;
border-radius:4px;
display:inline-flex;
align-items:center;
justify-content:center;
padding:2px;
flex-shrink:0
}
.food-type-icon.veg{border:2px solid #2E7D32}
.food-type-icon.veg:after{
content:'';
width:6px;
height:6px;
background:#2E7D32;
border-radius:50%
}
.popular-tag{
font-size:.68rem;
background:var(--soft);
color:var(--amber);
font-weight:800;
padding:2px 8px;
border-radius:6px;
display:inline-flex;
align-items:center;
gap:3px;
border:1px solid rgba(200,106,40,.3)
}
.food-name{
font-weight:700;
font-size:.98rem;
color:var(--primary);
margin-top:4px
}
.food-desc{
font-size:.8rem;
color:var(--muted);
margin-top:4px;
line-height:1.4
}
.card-action-side{
display:flex;
flex-direction:column;
justify-content:space-between;
align-items:flex-end;
min-width:82px;
flex-shrink:0
}
.price-text{
font-size:1.05rem;
font-weight:800;
color:var(--primary)
}
.add-btn{
background:var(--soft);
border:1.5px solid var(--amber);
color:var(--amber);
font-weight:800;
font-size:.78rem;
padding:6px 16px;
border-radius:12px;
cursor:pointer;
pointer-events:auto;
position:relative;
z-index:5;
min-width:64px
}
.add-btn:active{transform:scale(.95)}
.view-btn{
background:#f3f3f3;
border:1.5px solid #aaa;
color:#777;
font-weight:800;
font-size:.78rem;
padding:6px 16px;
border-radius:12px;
cursor:pointer;
min-width:64px
}
.qty-controls{
display:none;
align-items:center;
background:var(--primary);
color:#fff;
border-radius:12px;
padding:2px;
box-shadow:0 4px 10px rgba(74,14,23,.2)
}
.qty-btn{
background:none;
border:none;
color:var(--gold);
width:28px;
height:28px;
font-weight:800;
display:flex;
align-items:center;
justify-content:center;
cursor:pointer
}
.qty-val{
font-size:.85rem;
font-weight:700;
padding:0 6px;
color:#fff
}
.cart-float-bar{
position:fixed;
bottom:20px;
left:50%;
transform:translateX(-50%);
width:calc(100% - 32px);
max-width:600px;
background:var(--primary);
border:1.5px solid var(--gold);
color:#fff;
border-radius:20px;
padding:12px 20px;
display:none;
justify-content:space-between;
align-items:center;
box-shadow:var(--elevated);
z-index:1030
}
.view-cart-btn{
background:var(--amber);
color:#fff;
border:none;
font-weight:800;
font-size:.85rem;
padding:8px 18px;
border-radius:12px;
cursor:pointer
}
.offcanvas-bottom{
height:auto!important;
max-height:85vh;
border-top-left-radius:28px;
border-top-right-radius:28px;
background:var(--bg);
z-index:1060!important
}
.cart-modal-header{
border-bottom:1px solid rgba(212,175,55,.3);
padding:18px 20px
}
.cart-modal-body{
padding:16px 20px 30px;
overflow-y:auto;
max-height:calc(85vh - 70px)
}
.cart-item-row{
padding:14px 0;
border-bottom:1px dashed rgba(212,175,55,.4)
}
.cart-item-main{
display:flex;
justify-content:space-between;
align-items:center;
gap:10px
}
.cart-note{margin-top:10px}
.cart-note-label{
font-size:.75rem;
font-weight:700;
color:var(--muted);
margin-bottom:5px;
display:block
}
.cart-note-input{
width:100%;
border:1px solid rgba(74,14,23,.15);
border-radius:10px;
padding:8px 10px;
font-size:.8rem;
background:#fff;
color:var(--text);
outline:none
}
.bill-details{
background:#fff;
border:1px solid rgba(212,175,55,.5);
border-radius:16px;
padding:16px;
margin-top:16px
}
.bill-row{
display:flex;
justify-content:space-between;
font-size:.88rem;
margin-bottom:8px;
color:var(--muted)
}
.bill-row.total{
font-size:1.05rem;
font-weight:800;
color:var(--primary);
border-top:1px solid rgba(212,175,55,.3);
padding-top:10px;
margin-top:10px;
margin-bottom:0
}
.btn-call-order{
background:var(--primary);
color:#fff;
border-radius:12px;
font-weight:700;
font-size:.88rem;
padding:12px;
border:none
}
.btn-whatsapp-order{
background:var(--green);
color:#fff;
border-radius:12px;
font-weight:700;
font-size:.88rem;
padding:12px;
border:none;
text-decoration:none;
display:flex;
align-items:center;
justify-content:center;
gap:6px
}
.customer-order-type{
background:rgba(212,175,55,.08);
border:1px solid rgba(212,175,55,.25)
}
.customer-modal-input{
border-radius:12px;
padding:11px 13px;
border:1px solid rgba(74,14,23,.18)
}
.no-results{
display:none;
text-align:center;
padding:40px 20px;
color:var(--muted)
}
</style>
</head>
<body>

<div class="hero-banner text-center">
<div class="d-flex justify-content-between align-items-center mb-2">
<span class="status-pill"><i class="bi bi-clock-fill me-1"></i>Open • 11 AM - 12 PM</span>
<span class="status-pill"><i class="bi bi-star-fill me-1" style="color:var(--gold)"></i>4.9 (9.2k+)</span>
</div>
<h1 class="brand-header">🛕 VRINDAVAN DHABA Testing</h1>
<p class="small text-white-50 m-0 mt-1">Authentic Pure Vegetarian Culinary Experience</p>
</div>

<div class="container" style="max-width:640px">
<div class="mode-container">
<div class="mode-switch">
<a href="/dinein" class="mode-btn {{ 'active' if order_type == 'dinein' else '' }}"><i class="bi bi-shop"></i>Dine In</a>
<a href="/parcel" class="mode-btn {{ 'active' if order_type == 'parcel' else '' }}"><i class="bi bi-bag-check"></i>Parcel</a>
<a href="/online" class="mode-btn {{ 'active' if order_type == 'online' else '' }}"><i class="bi bi-moped"></i>Online</a>
</div>
</div>

<div class="search-box">
<i class="bi bi-search"></i>
<input type="text" id="searchInput" class="form-control" placeholder="Search dish name, dal, paneer..." onkeyup="filterMenu()">
</div>

<div class="category-scroll-wrapper">
<div class="category-scroll" id="categoryScroll">
{% for category in categories.keys() %}
<a href="#cat-{{ loop.index }}" class="cat-chip {{ 'active' if loop.first else '' }}" onclick="setActiveChip(this)">{{ category }}</a>
{% endfor %}
</div>
</div>

<div class="accordion" id="menuAccordion">
{% for category, items in categories.items() %}
<div class="accordion-item category-group" id="cat-{{ loop.index }}">
<h2 class="accordion-header" id="heading-{{ loop.index }}">
<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{{ loop.index }}" aria-expanded="true">
<span class="cat-count-badge me-2">{{ items|length }}</span>
<span class="me-auto">{{ category }}</span>
</button>
</h2>
<div id="collapse-{{ loop.index }}" class="accordion-collapse collapse show">
<div class="accordion-body">
{% for item in items %}
<div class="food-card" data-id="{{ item.slug }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">
<div class="flex-grow-1">
<div class="d-flex align-items-center gap-2">
<span class="food-type-icon veg"></span>
{% if item.popular %}
<span class="popular-tag"><i class="bi bi-fire"></i>Bestseller</span>
{% endif %}
</div>
<div class="food-name">{{ item.item_name }}</div>
<div class="food-desc">{{ item.description or 'Prepared with fresh ingredients and authentic dhaba spices.' }}</div>
</div>
<div class="card-action-side">
<div class="price-text">₹{{ "%.0f"|format(item.price) }}</div>
{% if order_type == "parcel" %}
<button class="add-btn" type="button" data-action="add" data-id="{{ item.slug }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">ADD</button>
<div class="qty-controls" id="qty-ctrl-{{ item.slug }}">
<button class="qty-btn" type="button" data-action="minus" data-id="{{ item.slug }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">−</button>
<span class="qty-val" id="qty-val-{{ item.slug }}">1</span>
<button class="qty-btn" type="button" data-action="plus" data-id="{{ item.slug }}" data-name="{{ item.item_name }}" data-price="{{ item.price }}">+</button>
</div>
{% else %}
<button class="view-btn" type="button" onclick="showOrderingUnavailable()">VIEW</button>
{% endif %}
</div>
</div>
{% endfor %}
</div>
</div>
</div>
{% endfor %}
</div>

<div class="no-results" id="noResults">
<i class="bi bi-search-heart display-4 text-muted"></i>
<h6 class="mt-3">No matching dishes found</h6>
<p class="small">Try searching for something else like 'Paneer' or 'Naan'.</p>
</div>
</div>

<div class="cart-float-bar" id="cartBar">
<div>
<div class="fw-bold" id="cartCount">0 ITEMS SELECTED</div>
<div class="small opacity-75" id="cartTotal">Total: ₹0</div>
</div>
<button class="view-cart-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#cartModal">
VIEW ORDER <i class="bi bi-arrow-right ms-1"></i>
</button>
</div>

<div class="offcanvas offcanvas-bottom" tabindex="-1" id="cartModal">
<div class="cart-modal-header d-flex justify-content-between align-items-center">
<div>
<h5 class="m-0 fw-bold" style="color:var(--primary);font-family:'Cinzel',serif">Your Order Cart</h5>
<small class="text-muted">Order Mode: <b>Parcel</b></small>
</div>
<button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
</div>
<div class="cart-modal-body">
<div id="cartItemsList"></div>
<div class="bill-details">
<div class="bill-row"><span>Items Subtotal</span><span id="billSubtotal">₹0</span></div>
<div class="bill-row"><span>Taxes & Charges already included (5%)</span><span id="billTax">₹0</span></div>
<div class="bill-row total"><span>Grand Total</span><span id="billGrandTotal">₹0</span></div>
</div>
<div class="mt-4 d-flex flex-column gap-2">
<button class="btn btn-call-order w-100" type="button" onclick="showCallOrderModal()">
<i class="bi bi-telephone-fill me-1"></i>Call to Place Order
</button>
<button class="btn btn-whatsapp-order w-100" type="button" onclick="startOrderProcess()">
<i class="bi bi-whatsapp me-1"></i>Send Order on WhatsApp
</button>
<button class="btn btn-sm text-muted mt-1" type="button" onclick="clearCart()">Clear Cart</button>
</div>
</div>
</div>

<div class="modal fade" id="callOrderModal" tabindex="-1">
<div class="modal-dialog modal-dialog-centered">
<div class="modal-content text-center p-4" style="border-radius:20px;border:1.5px solid var(--gold)">
<div class="modal-body p-0">
<i class="bi bi-telephone-outbound-fill display-4 mb-3 d-block" style="color:var(--primary)!important"></i>
<h5 class="fw-bold mb-2" style="color:var(--primary)">Call to Place Your Order</h5>
<p class="text-muted small mb-3">Please call us directly at the number below to confirm your order:</p>
<div class="p-3 mb-3" style="background:var(--goldbg);border-radius:12px;font-weight:800;font-size:1.2rem;color:var(--primary)">📞 8982003335</div>
<p class="small text-muted mb-4">Thanks for ordering from <b>Vrindavan Dhaba</b>!</p>
<a href="tel:+918982003335" class="btn text-white fw-bold w-100 py-2 mb-2" style="background:var(--primary);border-radius:12px">
<i class="bi bi-telephone-fill me-1"></i>Call Now
</a>
<button type="button" class="btn btn-light w-100 py-2" data-bs-dismiss="modal" style="border-radius:12px">Close</button>
</div>
</div>
</div>
</div>

<div class="modal fade" id="customerDetailsModal" tabindex="-1">
<div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
<div class="modal-content" style="border-radius:20px;border:1.5px solid var(--gold)">
<div class="modal-header" style="border-bottom:1px solid rgba(212,175,55,.3)">
<div>
<h5 class="modal-title fw-bold" style="color:var(--primary);font-family:'Cinzel',serif">Complete Your Parcel Order</h5>
<small class="text-muted">Just a few details to confirm your order</small>
</div>
<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
</div>
<div class="modal-body">
<div class="customer-order-type mb-3 p-3 rounded-3">
<div class="small text-muted">Order Type</div>
<div class="fw-bold" style="color:var(--primary)">🥡 Parcel</div>
</div>
<div class="mb-3">
<label for="customerName" class="form-label fw-semibold">Your Name</label>
<input type="text" id="customerName" class="form-control customer-modal-input" placeholder="Enter your name" autocomplete="name">
</div>
<div class="mb-3">
<label for="customerMobile" class="form-label fw-semibold">Mobile Number</label>
<input type="tel" id="customerMobile" class="form-control customer-modal-input" placeholder="10-digit mobile number" maxlength="10" inputmode="numeric" autocomplete="tel">
</div>
<div class="mb-3">
<label for="customerAddress" class="form-label fw-semibold">Delivery Address</label>
<textarea id="customerAddress" class="form-control customer-modal-input" rows="3" placeholder="Enter your complete address" autocomplete="street-address"></textarea>
</div>
<div id="customerDetailsError" class="alert alert-danger py-2 small" style="display:none"></div>
<div class="d-flex gap-2 mt-3">
<button type="button" class="btn btn-light w-50" data-bs-dismiss="modal">Back</button>
<button type="button" class="btn btn-whatsapp-order w-50" onclick="confirmAndSendWhatsAppOrder()">
<i class="bi bi-whatsapp me-1"></i>Send Order
</button>
</div>
</div>
</div>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
let cart={};
const restaurantPhone="918982003335";

function showOrderingUnavailable(){
    alert("Ordering is available only for Parcel orders.");
}

function updateQty(id,name,price,change){
    id=String(id);
    name=String(name);
    price=Number(price);
    change=Number(change);
    if(!id||!name||!Number.isFinite(price)||!Number.isFinite(change))return;
    if(!cart[id])cart[id]={id:id,name:name,price:price,count:0,note:""};
    cart[id].count+=change;
    if(cart[id].count<=0)delete cart[id];
    syncUI(id);
    renderCartBar();
    renderCartModal();
}

function syncUI(id){
    const card=document.querySelector('.food-card[data-id="'+CSS.escape(id)+'"]');
    if(!card)return;
    const addBtn=card.querySelector('.add-btn');
    const qtyCtrl=card.querySelector('.qty-controls');
    const qtyVal=card.querySelector('.qty-val');
    const item=cart[id];
    if(item&&item.count>0){
        if(addBtn)addBtn.style.display='none';
        if(qtyCtrl)qtyCtrl.style.display='flex';
        if(qtyVal)qtyVal.textContent=item.count;
    }else{
        if(addBtn)addBtn.style.display='block';
        if(qtyCtrl)qtyCtrl.style.display='none';
        if(qtyVal)qtyVal.textContent='1';
    }
}

function updateItemNote(id,value){
    if(cart[id])cart[id].note=value;
}

function getCartTotals(){
    let totalItems=0,totalPrice=0;
    Object.values(cart).forEach(item=>{
        totalItems+=item.count;
        totalPrice+=item.count*item.price;
    });
    return{totalItems,totalPrice};
}

function renderCartBar(){
    const bar=document.getElementById('cartBar');
    const cartModal=document.getElementById('cartModal');
    const {totalItems,totalPrice}=getCartTotals();
    const isOpen=cartModal.classList.contains('show');
    if(totalItems>0&&!isOpen){
        bar.style.display='flex';
        document.getElementById('cartCount').textContent=totalItems+' ITEM'+(totalItems!==1?'S':'')+' ADDED';
        document.getElementById('cartTotal').textContent='Total: ₹'+totalPrice.toFixed(0);
    }else{
        bar.style.display='none';
    }
    if(totalItems===0){
        const offcanvas=bootstrap.Offcanvas.getInstance(cartModal);
        if(offcanvas)offcanvas.hide();
    }
}

function renderCartModal(){
    const list=document.getElementById('cartItemsList');
    list.innerHTML='';
    let subtotal=0;
    Object.values(cart).forEach(item=>{
        const itemTotal=item.count*item.price;
        subtotal+=itemTotal;
        const row=document.createElement('div');
        row.className='cart-item-row';
        const main=document.createElement('div');
        main.className='cart-item-main';
        const left=document.createElement('div');
        const itemName=document.createElement('div');
        itemName.className='fw-bold';
        itemName.style.color='var(--primary)';
        itemName.textContent=item.name;
        const itemInfo=document.createElement('small');
        itemInfo.className='text-muted';
        itemInfo.textContent='₹'+item.price.toFixed(0)+' × '+item.count;
        left.append(itemName,itemInfo);
        const right=document.createElement('div');
        right.className='d-flex align-items-center gap-3';
        const total=document.createElement('span');
        total.className='fw-bold';
        total.style.color='var(--primary)';
        total.textContent='₹'+itemTotal.toFixed(0);
        const controls=document.createElement('div');
        controls.className='qty-controls';
        controls.style.display='flex';
        const minus=document.createElement('button');
        minus.type='button';
        minus.className='qty-btn';
        minus.dataset.cartAction='minus';
        minus.dataset.id=item.id;
        minus.textContent='−';
        const qty=document.createElement('span');
        qty.className='qty-val';
        qty.textContent=item.count;
        const plus=document.createElement('button');
        plus.type='button';
        plus.className='qty-btn';
        plus.dataset.cartAction='plus';
        plus.dataset.id=item.id;
        plus.textContent='+';
        controls.append(minus,qty,plus);
        right.append(total,controls);
        main.append(left,right);
        const noteContainer=document.createElement('div');
        noteContainer.className='cart-note';
        const noteLabel=document.createElement('label');
        noteLabel.className='cart-note-label';
        noteLabel.textContent='Note for this item';
        const noteInput=document.createElement('input');
        noteInput.type='text';
        noteInput.className='cart-note-input';
        noteInput.placeholder='e.g. Less spicy, no onion, extra butter...';
        noteInput.maxLength=200;
        noteInput.value=item.note||'';
        noteInput.dataset.noteId=item.id;
        noteContainer.append(noteLabel,noteInput);
        row.append(main,noteContainer);
        list.appendChild(row);
    });
    const gst=subtotal*5/105;
    document.getElementById('billSubtotal').textContent='₹'+subtotal.toFixed(0);
    document.getElementById('billTax').textContent='₹'+gst.toFixed(0);
    document.getElementById('billGrandTotal').textContent='₹'+subtotal.toFixed(0);
}

function clearCart(){
    Object.keys(cart).forEach(id=>{
        delete cart[id];
        syncUI(id);
    });
    renderCartModal();
    renderCartBar();
}

function startOrderProcess(){
    if(!Object.keys(cart).length){
        alert('Please add at least one item to your order.');
        return;
    }
    const cartElement=document.getElementById('cartModal');
    const cartModal=bootstrap.Offcanvas.getInstance(cartElement);
    if(cartModal)cartModal.hide();
    setTimeout(()=>{
        bootstrap.Modal.getOrCreateInstance(document.getElementById('customerDetailsModal')).show();
        setTimeout(()=>document.getElementById('customerName').focus(),400);
    },350);
}

function confirmAndSendWhatsAppOrder(){
    const name=document.getElementById('customerName').value.trim();
    const mobile=document.getElementById('customerMobile').value.trim();
    const address=document.getElementById('customerAddress').value.trim();
    const error=document.getElementById('customerDetailsError');
    error.style.display='none';
    error.textContent='';
    if(!name){
        error.textContent='Please enter your name.';
        error.style.display='block';
        document.getElementById('customerName').focus();
        return;
    }
    if(!/^[0-9]{10}$/.test(mobile)){
        error.textContent='Please enter a valid 10-digit mobile number.';
        error.style.display='block';
        document.getElementById('customerMobile').focus();
        return;
    }
    if(!address){
        error.textContent='Please enter your delivery address.';
        error.style.display='block';
        document.getElementById('customerAddress').focus();
        return;
    }
    sendWhatsAppOrder(name,mobile,address);
}

function showCallOrderModal(){
    if(!Object.keys(cart).length){
        alert('Please add at least one item to your order.');
        return;
    }
    const cartElement=document.getElementById('cartModal');
    const cartModal=bootstrap.Offcanvas.getInstance(cartElement);
    if(cartModal)cartModal.hide();
    setTimeout(()=>{
        bootstrap.Modal.getOrCreateInstance(document.getElementById('callOrderModal')).show();
    },350);
}

function sendWhatsAppOrder(name,mobile,address){
    let message='';

    message+='🛕 *VRINDAVAN DHABA*\\n';
    message+='✨ *PURE VEG • ORDER DETAILS*\\n';
    message+='------------------------\\n\\n';

    message+='🥡 Order Mode: Parcel\\n';
    message+='👤 '+name+' | 📱 '+mobile+'\\n';
    message+='📍 Address: '+address+'\\n';
    

    const now=new Date();
    const date=now.toLocaleDateString('en-IN',{
        day:'2-digit',
        month:'2-digit',
        year:'numeric'
    });

    const time=now.toLocaleTimeString('en-IN',{
        hour:'2-digit',
        minute:'2-digit',
        hour12:true
    });

    message+='🕐 '+date+' '+time+'\\n\\n';

    message+='---------------------------------\\n';
    message+='           *ORDER ITEMS*\\n';
    message+='---------------------------------\\n\\n';

    let subtotal=0;

    Object.values(cart).forEach(function(item){
        const qty=Number(item.count);
        const price=Number(item.price);
        const amount=qty*price;

        subtotal+=amount;

        let itemName=String(item.name)
            .replace(/\\s+/g,' ')
            .trim();

        if(item.note && item.note.trim()!==''){
            itemName+=' ('+
                String(item.note)
                .replace(/\\s+/g,' ')
                .trim()+
                ')';
        }

        message+='* '+itemName+' x '+qty+' = ₹'+amount.toFixed(0)+'\\n';
    });

    const gstIncluded=subtotal*5/105;

    message+='\\n';
    message+='---------------------------------\\n';
    message+='Subtotal: ₹'+subtotal.toFixed(0)+'\\n';
    message+='Taxes & Charges already included (5%): ₹'+gstIncluded.toFixed(0)+'\\n';
    message+='*GRAND TOTAL: ₹'+subtotal.toFixed(0)+'*\\n';
    message+='---------------------------------\\n\\n';

    message+='🙏 Thank you for ordering!\\n';
    message+='📞 Call 8982003335 to confirm\\n';
    message+='Order is NOT placed until confirmed.';

    const whatsappUrl=
        'https://wa.me/'+
        restaurantPhone+
        '?text='+
        encodeURIComponent(message);

    window.open(whatsappUrl,'_blank');

    const modalElement=document.getElementById('customerDetailsModal');
    const modal=bootstrap.Modal.getInstance(modalElement);

    if(modal)modal.hide();
}

function filterMenu(){
    const query=document.getElementById('searchInput').value.toLowerCase().trim();
    const groups=document.querySelectorAll('.category-group');
    let totalVisible=0;
    groups.forEach(group=>{
        const cards=group.querySelectorAll('.food-card');
        let visible=0;
        cards.forEach(card=>{
            const name=(card.dataset.name||'').toLowerCase();
            const show=name.includes(query);
            card.style.display=show?'flex':'none';
            if(show){
                visible++;
                totalVisible++;
            }
        });
        group.style.display=visible?'block':'none';
    });
    document.getElementById('noResults').style.display=totalVisible?'none':'block';
}

function setActiveChip(element){
    document.querySelectorAll('.cat-chip').forEach(chip=>chip.classList.remove('active'));
    element.classList.add('active');
}

document.addEventListener('click',function(e){
    const button=e.target.closest('[data-action],[data-cart-action]');
    if(!button)return;
    e.preventDefault();
    e.stopPropagation();

    if(button.dataset.action){
        const id=button.dataset.id;
        const name=button.dataset.name;
        const price=Number(button.dataset.price);
        if(!id||!name||!Number.isFinite(price))return;
        if(button.dataset.action==='add'){
            updateQty(id,name,price,1);
        }else if(button.dataset.action==='minus'){
            updateQty(id,name,price,-1);
        }else if(button.dataset.action==='plus'){
            updateQty(id,name,price,1);
        }
        return;
    }

    if(button.dataset.cartAction){
        const id=button.dataset.id;
        if(!cart[id])return;
        if(button.dataset.cartAction==='minus'){
            updateQty(id,cart[id].name,cart[id].price,-1);
        }else if(button.dataset.cartAction==='plus'){
            updateQty(id,cart[id].name,cart[id].price,1);
        }
    }
});

document.addEventListener('input',function(e){
    if(e.target.matches('[data-note-id]')){
        updateItemNote(e.target.dataset.noteId,e.target.value);
    }
});

document.addEventListener('DOMContentLoaded',function(){
    const cartModalElement=document.getElementById('cartModal');
    if(cartModalElement){
        cartModalElement.addEventListener('show.bs.offcanvas',function(){
            document.getElementById('cartBar').style.display='none';
            renderCartModal();
        });
        cartModalElement.addEventListener('hidden.bs.offcanvas',function(){
            renderCartBar();
        });
    }

    const mobileInput=document.getElementById('customerMobile');
    if(mobileInput){
        mobileInput.addEventListener('input',function(){
            this.value=this.value.replace(/[^0-9]/g,'').slice(0,10);
        });
    }
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return redirect(url_for("menu_page",order_type="parcel"))

@app.route("/<order_type>")
def menu_page(order_type):
    if order_type not in ["dinein","parcel","online"]:
        order_type="parcel"
    categories=build_menu(order_type)
    titles={
        "dinein":"Dine In Menu",
        "parcel":"Takeaway / Parcel Menu",
        "online":"Online Delivery Menu"
    }
    return render_template_string(
        MENU_TEMPLATE,
        categories=categories,
        order_type=order_type,
        title=titles.get(order_type,"Menu")
    )

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)
