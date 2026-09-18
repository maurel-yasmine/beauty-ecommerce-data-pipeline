import json
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "beauty_shop.db")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def query(conn, sql):
    return conn.execute(sql).fetchall()

def rupiah(n):
    return f"Rp {int(n):,}".replace(",", ".")

def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit("Database belum ada. Jalankan dulu: python src/etl_pipeline.py")

    conn = sqlite3.connect(DB_PATH)

    summary = query(conn, "SELECT COUNT(*), SUM(quantity), SUM(revenue) FROM sales;")[0]
    by_category = query(conn, "SELECT category, SUM(revenue) FROM sales GROUP BY category ORDER BY SUM(revenue) DESC;")
    top_products = query(conn, "SELECT product_name, SUM(revenue) FROM sales GROUP BY product_name ORDER BY SUM(revenue) DESC LIMIT 5;")
    monthly = query(conn, "SELECT order_month, SUM(revenue) FROM sales GROUP BY order_month ORDER BY order_month;")
    by_channel = query(conn, "SELECT channel, SUM(revenue) FROM sales GROUP BY channel ORDER BY SUM(revenue) DESC;")

    conn.close()

    print("RINGKASAN INSIGHT - Beauty E-Commerce")
    print("Total transaksi   :", f"{summary[0]:,}")
    print("Total unit terjual:", f"{summary[1]:,}")
    print("Total revenue     :", rupiah(summary[2]))
    print("Revenue per kategori:")
    for cat, rev in by_category:
        print("  -", cat, ":", rupiah(rev))
    print("INSIGHT UTAMA:")
    print("  * Kategori terbesar :", by_category[0][0])
    print("  * Channel terkuat   :", by_channel[0][0])
    print("  * Produk terlaris   :", top_products[0][0])

    html = _build_dashboard_html(summary, by_category, top_products, monthly, by_channel)
    out_path = os.path.join(REPORT_DIR, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard tersimpan di:", out_path)

def _build_dashboard_html(summary, by_category, top_products, monthly, by_channel):
    data = {
        "cat_labels": [r[0] for r in by_category],
        "cat_values": [r[1] for r in by_category],
        "prod_labels": [r[0] for r in top_products],
        "prod_values": [r[1] for r in top_products],
        "month_labels": [r[0] for r in monthly],
        "month_values": [r[1] for r in monthly],
        "chan_labels": [r[0] for r in by_channel],
        "chan_values": [r[1] for r in by_channel],
    }
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Beauty E-Commerce Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body {{ font-family: system-ui, sans-serif; background:#faf5f8; color:#333; margin:0; padding:24px; }}
  h1 {{ text-align:center; color:#c2557f; }}
  .kpis {{ display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin:24px 0; }}
  .kpi {{ background:#fff; border-radius:14px; padding:18px 28px; box-shadow:0 4px 14px rgba(0,0,0,.06); text-align:center;
         opacity:0; transform:translateY(16px); animation:rise .6s ease forwards; }}
  .kpi:nth-child(2){{ animation-delay:.12s; }}
  .kpi:nth-child(3){{ animation-delay:.24s; }}
  .kpi .num {{ font-size:1.6rem; font-weight:800; color:#c2557f; }}
  .kpi .lbl {{ color:#888; font-size:.85rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:20px; max-width:1100px; margin:0 auto; }}
  .card {{ background:#fff; border-radius:14px; padding:20px; box-shadow:0 4px 14px rgba(0,0,0,.06);
          opacity:0; transform:translateY(16px); animation:rise .6s ease forwards; transition:transform .2s, box-shadow .2s; }}
  .card:hover {{ transform:translateY(-4px); box-shadow:0 8px 22px rgba(194,85,127,.18); }}
  .card:nth-child(2){{ animation-delay:.1s; }}
  .card:nth-child(3){{ animation-delay:.2s; }}
  .card:nth-child(4){{ animation-delay:.3s; }}
  @keyframes rise {{ to {{ opacity:1; transform:none; }} }}
  @media(max-width:700px){{ body{{padding:14px;}} h1{{font-size:1.3rem;}} }}
</style>
</head>
<body>
  <h1>Beauty E-Commerce - Sales Dashboard</h1>
  <div class="kpis">
    <div class="kpi"><div class="num">{summary[0]:,}</div><div class="lbl">Total Transaksi</div></div>
    <div class="kpi"><div class="num">{summary[1]:,}</div><div class="lbl">Unit Terjual</div></div>
    <div class="kpi"><div class="num">{rupiah(summary[2])}</div><div class="lbl">Total Revenue</div></div>
  </div>
  <div class="grid">
    <div class="card"><canvas id="catChart"></canvas></div>
    <div class="card"><canvas id="prodChart"></canvas></div>
    <div class="card"><canvas id="monthChart"></canvas></div>
    <div class="card"><canvas id="chanChart"></canvas></div>
  </div>
<script>
const D = {json.dumps(data)};
const pink = "#d16ba5", blue = "#86a8e7", teal = "#5ffbf1";
Chart.defaults.animation = {{ duration: 1100, easing: 'easeOutQuart' }};
Chart.defaults.responsive = true;
new Chart(catChart, {{ type:'bar', data:{{ labels:D.cat_labels, datasets:[{{ label:'Revenue', data:D.cat_values, backgroundColor:pink }}] }}, options:{{ plugins:{{ title:{{ display:true, text:'Revenue per Kategori' }}, legend:{{display:false}} }} }} }});
new Chart(prodChart, {{ type:'bar', data:{{ labels:D.prod_labels, datasets:[{{ label:'Revenue', data:D.prod_values, backgroundColor:blue }}] }}, options:{{ indexAxis:'y', plugins:{{ title:{{ display:true, text:'5 Produk Terlaris' }}, legend:{{display:false}} }} }} }});
new Chart(monthChart, {{ type:'line', data:{{ labels:D.month_labels, datasets:[{{ label:'Revenue', data:D.month_values, borderColor:pink, backgroundColor:pink, tension:.3, fill:false }}] }}, options:{{ plugins:{{ title:{{ display:true, text:'Tren Revenue Bulanan' }}, legend:{{display:false}} }} }} }});
new Chart(chanChart, {{ type:'doughnut', data:{{ labels:D.chan_labels, datasets:[{{ data:D.chan_values, backgroundColor:[pink,blue,teal] }}] }}, options:{{ plugins:{{ title:{{ display:true, text:'Proporsi Revenue per Channel' }} }} }} }});
</script>
</body>
</html>"""

if __name__ == "__main__":
    main()
