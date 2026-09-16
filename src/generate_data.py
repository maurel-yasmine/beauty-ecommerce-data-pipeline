"""
====================================================================
 STEP 0 — DATA GENERATOR (Sumber Data)
====================================================================
Membuat dataset penjualan e-commerce beauty yang realistis dalam
format CSV. Di dunia nyata data ini bisa berasal dari database
transaksi, API, atau export dari sistem penjualan.

Menghasilkan 2 file:
  1. data/raw/orders.csv    -> transaksi penjualan (fakta)
  2. data/raw/products.csv  -> katalog produk (dimensi)

Sengaja diberi beberapa "data kotor" (nilai kosong, spasi berlebih,
format tidak konsisten) supaya tahap TRANSFORM punya pekerjaan
membersihkan data — persis seperti data dunia nyata.
====================================================================
"""

import csv
import os
import random
from datetime import datetime, timedelta

# seed -> agar data yang dihasilkan selalu sama (reproducible)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# Katalog produk beauty: id, nama, kategori, brand, harga
PRODUCTS = [
    (1,  "Matte Lipstick Ruby",        "Makeup",    "GlowUp",    120000),
    (2,  "Hydrating Serum 30ml",       "Skincare",  "AquaDew",   210000),
    (3,  "Volume Mascara",             "Makeup",    "GlowUp",     95000),
    (4,  "Sunscreen SPF50 PA++++",     "Skincare",  "SunGuard",  135000),
    (5,  "Rose Eau de Parfum 50ml",    "Fragrance", "Bloom",     350000),
    (6,  "Cushion Foundation",         "Makeup",    "Velvet",    180000),
    (7,  "Vitamin C Brightening Gel",  "Skincare",  "AquaDew",   165000),
    (8,  "Nourishing Hair Mask",       "Haircare",  "SilkPro",   110000),
    (9,  "Micellar Cleansing Water",   "Skincare",  "PureSkin",   88000),
    (10, "Nude Eyeshadow Palette",     "Makeup",    "Velvet",    230000),
    (11, "Citrus Body Mist 100ml",     "Fragrance", "Bloom",     140000),
    (12, "Anti-Frizz Hair Serum",      "Haircare",  "SilkPro",    99000),
    (13, "Clay Pore Mask",             "Skincare",  "PureSkin",  120000),
    (14, "Long-Wear Eyeliner",         "Makeup",    "GlowUp",     75000),
    (15, "Repair Night Cream",         "Skincare",  "AquaDew",   245000),
]

CHANNELS = ["Website", "Mobile App", "Marketplace"]
CITIES = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar", "Semarang"]
PAYMENTS = ["E-Wallet", "Credit Card", "Bank Transfer", "COD"]

def write_products():
    """Tulis katalog produk ke products.csv"""
    path = os.path.join(RAW_DIR, "products.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_name", "category", "brand", "price"])
        for row in PRODUCTS:
            writer.writerow(row)
    print(f"  -> products.csv  ({len(PRODUCTS)} produk)")

def write_orders(n_orders=2000):
    """Tulis n transaksi acak ke orders.csv (sebagian sengaja 'kotor')."""
    path = os.path.join(RAW_DIR, "orders.csv")
    start_date = datetime(2024, 1, 1)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "order_id", "order_date", "product_id", "quantity",
            "channel", "city", "payment_method", "customer_id",
        ])
        for i in range(1, n_orders + 1):
            product = random.choice(PRODUCTS)
            product_id = product[0]
            order_date = start_date + timedelta(days=random.randint(0, 364))
            quantity = random.randint(1, 4)
            channel = random.choice(CHANNELS)
            city = random.choice(CITIES)
            payment = random.choice(PAYMENTS)
            customer_id = random.randint(1000, 1400)

            # ---- Sengaja buat sebagian data "kotor" ----
            if random.random() < 0.03:      
                city = ""
            if random.random() < 0.02:      
                quantity = 0
            if random.random() < 0.10:      
                channel = "  " + channel.upper() + " "

            writer.writerow([
                f"ORD{i:05d}",
                order_date.strftime("%Y-%m-%d"),
                product_id, quantity, channel, city, payment, customer_id,
            ])
    print(f"  -> orders.csv    ({n_orders} transaksi)")

if __name__ == "__main__":
    print("STEP 0: Membuat data mentah (raw) ...")
    write_products()
    write_orders()
    print("Selesai. Data mentah tersimpan di data/raw/")
