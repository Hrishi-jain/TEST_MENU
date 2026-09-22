from flask import Flask, render_template_string
from collections import defaultdict
import json
from pathlib import Path

app = Flask(__name__)
# Use parent, not parent.parent, so Vercel finds /data/menu.json
DATA_FILE = Path(__file__).resolve().parent / "data" / "menu.json"

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

MENU_TEMPLATE = """<!doctype html>
<html><head>
<title>{{ title }}</title><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head><body>
<div class="container mt-3">
<h2>{{ title }}</h2>
{% for category,items in categories.items() %}
<h4>{{ category }} ({{ items|length }})</h4>
<ul>
{% for item in items %}
<li><b>{{ item.item_name }}</b> — ₹{{ item.price }}<br><small>{{ item.description }}</small></li>
{% endfor %}
</ul>
{% endfor %}
</div>
</body></html>"""

def render_menu(order_type, title):
    return render_template_string(
        MENU_TEMPLATE,
        categories=build_menu(order_type),
        order_type=order_type,
        title=title,
        subtitle=title
    )

@app.route("/")
def home():
    return render_menu("dinein", "Dine In Menu")

@app.route("/dinein")
def dinein():
    return render_menu("dinein", "Dine In Menu")

@app.route("/parcel")
def parcel():
    return render_menu("parcel", "Parcel Menu")

@app.route("/online")
def online():
    return render_menu("online", "Online Menu")

if __name__ == "__main__":
    app.run(debug=True)
