-- Q1. Total revenue, transaksi, dan unit terjual keseluruhan
SELECT
    COUNT(*)              AS total_transaksi,
    SUM(quantity)         AS total_unit_terjual,
    SUM(revenue)          AS total_revenue,
    ROUND(AVG(revenue),0) AS rata_rata_nilai_transaksi
FROM sales;

-- Q2. Kategori produk paling menguntungkan
SELECT
    category,
    SUM(quantity)  AS unit_terjual,
    SUM(revenue)   AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;

-- Q3. 5 produk terlaris berdasarkan revenue
SELECT
    product_name,
    brand,
    SUM(quantity) AS unit_terjual,
    SUM(revenue)  AS total_revenue
FROM sales
GROUP BY product_name, brand
ORDER BY total_revenue DESC
LIMIT 5;

-- Q4. Tren revenue per bulan (analisis musiman)
SELECT
    order_month,
    SUM(revenue) AS revenue_bulanan
FROM sales
GROUP BY order_month
ORDER BY order_month;

-- Q5. Channel penjualan paling efektif
SELECT
    channel,
    COUNT(*)     AS jumlah_transaksi,
    SUM(revenue) AS total_revenue,
    ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM sales), 1) AS persen_revenue
FROM sales
GROUP BY channel
ORDER BY total_revenue DESC;

-- Q6. Kota dengan revenue tertinggi
SELECT
    city,
    SUM(revenue) AS total_revenue
FROM sales
WHERE city <> 'Unknown'
GROUP BY city
ORDER BY total_revenue DESC;

-- Q7. 5 pelanggan paling loyal (total belanja terbesar)
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS jumlah_order,
    SUM(revenue)             AS total_belanja
FROM sales
GROUP BY customer_id
ORDER BY total_belanja DESC
LIMIT 5;

-- Q8. Kontribusi tiap brand terhadap total revenue (window function)
SELECT
    brand,
    SUM(revenue) AS revenue_brand,
    ROUND(
        100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 1
    ) AS persen_kontribusi
FROM sales
GROUP BY brand
ORDER BY revenue_brand DESC;
