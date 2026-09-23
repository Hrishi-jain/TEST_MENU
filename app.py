from flask import Flask, render_template_string
from collections import defaultdict
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "menu.json"


def load_menu():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_menu(order_type):
    fields = {
        "dinein": ("dine_in_price", "dine_in_active"),
        "parcel": ("pickup_price", "pickup_active"),
        "online": ("online_price", "online_active")
    }
    price_field, active_field = fields[order_type]
    categories = defaultdict(list)
    for item in load_menu():
        if not item.get("is_active", True) or not item.get(active_field, True):
            continue
        price = item.get(price_field)
        if price is None or float(price) <= 0:
            continue
        categories[item.get("category", "Other")].append({
            "item_name": item.get("item_name", ""),
            "category": item.get("category", "Other"),
            "description": item.get("description", ""),
            "price": price
        })
    return categories


MENU_TEMPLATE = """
<!doctype html>
<html><head>
<title>{{ title }}</title><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#fff8ef}.header{background:#8B0000;color:white;padding:20px;text-align:center;border-radius:0 0 20px 20px}
.category-btn{font-size:20px;font-weight:bold;color:#8B0000;background:#fff}.category-btn:not(.collapsed){background:#8B0000;color:white}
.accordion-button:focus{box-shadow:none}.count-box{width:34px;height:34px;border-radius:50%;background:#8B0000;color:white;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:bold;flex-shrink:0}
.item{background:white;margin:8px 0;padding:12px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,.1);display:flex;justify-content:space-between;align-items:center;gap:15px}
.price{font-weight:bold;color:#8B0000;white-space:nowrap}.desc{font-size:12px;color:#777;margin-top:3px}
.spice-note{display:inline-block;margin-top:4px;font-size:12px;color:#8B0000;font-weight:500;background:#fff3e0;padding:2px 8px;border-radius:12px;border:1px solid #f0d2a8}
.menu-switch{display:flex;gap:8px;overflow-x:auto;padding-bottom:5px}.menu-switch a{flex:1;min-width:100px;text-align:center;text-decoration:none;border:1px solid #8B0000;border-radius:10px;padding:9px;color:#8B0000;background:white;font-weight:bold}.menu-switch a.active{background:#8B0000;color:white}
</style></head><body>
<div class="header"><h2>🍛 Welcome to Dhaba</h2><h5>{{ subtitle }}</h5></div>
<div class="container mt-3">
<div class="menu-switch">
<a href="/dinein" class="{{ 'active' if order_type=='dinein' else '' }}">🍽 Dine In</a>
<a href="/parcel" class="{{ 'active' if order_type=='parcel' else '' }}">🥡 Parcel</a>
<a href="/online" class="{{ 'active' if order_type=='online' else '' }}">🛵 Online</a>
</div>
<div class="accordion mt-3" id="menuAccordion">
{% for category,items in categories.items() %}
<div class="accordion-item mb-3"><h2 class="accordion-header">
<button class="accordion-button collapsed category-btn" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{loop.index}}">
<span class="count-box">{{items|length}}</span><span class="ms-3">{{category}}</span></button></h2>
<div id="collapse{{loop.index}}" class="accordion-collapse collapse" data-bs-parent="#menuAccordion"><div class="accordion-body">
{% for item in items %}<div class="item"><div><b>{{item.item_name}}</b>
{% if item.category in ['Paneer Se Paneer Tak','Sabji Kuchh Hatke','Starters','Chinese','Soup','Sabiziyaan'] %}<div class="spice-note">🌶 Spice: Normal • Medium • High</div>{% endif %}
<div class="desc">{{item.description or ''}}</div></div><div class="price">₹{{item.price}}</div></div>{% endfor %}
</div></div></div>
{% endfor %}</div></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>
"""


def render_menu(order_type, title):
    return render_template_string(MENU_TEMPLATE, categories=build_menu(order_type), order_type=order_type, title=title, subtitle=title)


@app.route("/")
def home(): return render_menu("dinein", "Dine In Menu")
@app.route("/dinein")
def dinein(): return render_menu("dinein", "Dine In Menu")
@app.route("/parcel")
def parcel(): return render_menu("parcel", "Parcel Menu")
@app.route("/online")
def online(): return render_menu("online", "Online Menu")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
