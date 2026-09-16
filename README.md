# 💄 Beauty E-Commerce Data Pipeline

Proyek **end-to-end data pipeline** yang mensimulasikan alur kerja seorang
Data Engineer & Data Analyst pada data penjualan e-commerce produk kecantikan.

Data mentah (CSV) diproses melalui pipeline **ETL** (Extract → Transform → Load),
disimpan ke database **SQLite**, dianalisis dengan **SQL**, lalu divisualisasikan
dalam sebuah **dashboard**.

> Dibuat oleh **Maurel Chairinniswah Yasmine** — Computer Science, BINUS University.

---

## 🎯 Tujuan Proyek

1. **Data Engineering** — merancang & membangun pipeline ETL yang andal.
2. **Data Analysis** — menjawab pertanyaan bisnis nyata dengan SQL.
3. **Data Visualization** — menyajikan insight dalam dashboard.

## 🛠️ Tech Stack

Python 3 · SQLite · SQL · Chart.js

## → Cara Menjalankan

```bash
python main.py
```

Menghasilkan database + dashboard di folder `reports/`.

## 🔍 Pertanyaan Bisnis yang Dijawab

1. Total revenue, transaksi, unit terjual
2. Kategori produk paling menguntungkan
3. 5 produk terlaris
4. Tren revenue bulanan
5. Channel penjualan paling efektif
6. Kota revenue tertinggi
7. 5 pelanggan paling loyal
8. Kontribusi brand (window function)

## 💡 Konsep

ETL Pipeline · Data Cleaning · JOIN & Enrichment · Dimensional Modeling · SQL Analitik · Data Visualization
