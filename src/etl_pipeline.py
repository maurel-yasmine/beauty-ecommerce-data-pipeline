import csv
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "beauty_shop.db")

# 1) EXTRACT — membaca data mentah dari CSV
def extract():
    print("EXTRACT: membaca data mentah dari CSV ...")
    with open(os.path.join(RAW_DIR, "orders.csv"), encoding="utf-8") as f:
        orders = list(csv.DictReader(f))
    with open(os.path.join(RAW_DIR, "products.csv"), encoding="utf-8") as f:
        products = list(csv.DictReader(f))
    print(f"  -> orders: {len(orders)} baris | products: {len(products)} baris")
    return orders, products

# 2) TRANSFORM — membersihkan & memperdalam data
def transform(orders, products):
    print("TRANSFORM: membersihkan & memperdalam data ...")
    before = len(orders)

    # lookup produk untuk JOIN
    product_lookup = {p["product_id"]: p for p in products}

    clean_rows = []
    for row in orders:
        # rapikan channel: hapus spasi & samakan huruf
        row["channel"] = row["channel"].strip().title()

        # buang transaksi tidak valid (quantity <= 0)
        quantity = int(row["quantity"])
        if quantity <= 0:
            continue

        # isi kota kosong dengan 'Unknown'
        city = row["city"].strip()
        row["city"] = city if city else "Unknown"

        # validasi tanggal
        try:
            order_date = datetime.strptime(row["order_date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            continue

        # ENRICH: gabungkan (JOIN) dengan data produk
        product = product_lookup.get(row["product_id"])
        if product is None:
            continue

        price = float(product["price"])
        revenue = price * quantity                      # kolom turunan
        order_month = order_date.strftime("%Y-%m")      # bulan untuk tren

        clean_rows.append({
            "order_id": row["order_id"],
            "order_date": row["order_date"],
            "order_month": order_month,
            "product_id": int(row["product_id"]),
            "product_name": product["product_name"],
            "category": product["category"],
            "brand": product["brand"],
            "quantity": quantity,
            "price": price,
            "revenue": revenue,
            "channel": row["channel"],
            "city": row["city"],
            "payment_method": row["payment_method"],
            "customer_id": int(row["customer_id"]),
        })

    after = len(clean_rows)
    print(f"  -> {before - after} baris kotor dibuang, {after} baris bersih siap dimuat")
    return clean_rows

# 3) LOAD — memuat data bersih ke database SQLite
def load(clean_rows, products):
    print("LOAD: memuat data ke database SQLite ...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # tabel dimensi: produk
    cur.execute("""
        CREATE TABLE products (
            product_id   INTEGER PRIMARY KEY,
            product_name TEXT,
            category     TEXT,
            brand        TEXT,
            price        REAL
        );
    """)
    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
        [(int(p["product_id"]), p["product_name"], p["category"],
          p["brand"], float(p["price"])) for p in products],
    )

    # tabel fakta: penjualan
    cur.execute("""
        CREATE TABLE sales (
            order_id       TEXT,
            order_date     TEXT,
            order_month    TEXT,
            product_id     INTEGER,
            product_name   TEXT,
            category       TEXT,
            brand          TEXT,
            quantity       INTEGER,
            price          REAL,
            revenue        REAL,
            channel        TEXT,
            city           TEXT,
            payment_method TEXT,
            customer_id    INTEGER
        );
    """)
    cur.executemany(
        """INSERT INTO sales VALUES
           (:order_id, :order_date, :order_month, :product_id, :product_name,
            :category, :brand, :quantity, :price, :revenue, :channel, :city,
            :payment_method, :customer_id)""",
        clean_rows,
    )

    # indeks agar query lebih cepat
    cur.execute("CREATE INDEX idx_sales_category ON sales(category);")
    cur.execute("CREATE INDEX idx_sales_month ON sales(order_month);")
    conn.commit()

    n = cur.execute("SELECT COUNT(*) FROM sales;").fetchone()[0]
    conn.close()
    print(f"  -> Database dibuat: {DB_PATH}")
    print(f"  -> Tabel 'sales' berisi {n} baris")
    print("")

def run_pipeline():
    print("=" * 60)
    print(" MENJALANKAN ETL PIPELINE — Beauty E-Commerce")
    print("=" * 60)
    orders, products = extract()
    clean = transform(orders, products)
    load(clean, products)
    print("PIPELINE SELESAI. Database siap untuk dianalisis.")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
