from src import generate_data
from src import etl_pipeline
from src import run_analysis

if __name__ == "__main__":
    print("
### 1/3 — GENERATE DATA ###")
    generate_data.write_products()
    generate_data.write_orders()

    print("
### 2/3 — ETL PIPELINE ###")
    etl_pipeline.run_pipeline()

    print("
### 3/3 — ANALISIS & DASHBOARD ###")
    run_analysis.main()

    print("SEMUA SELESAI! Cek folder reports/ untuk melihat dashboard.")
