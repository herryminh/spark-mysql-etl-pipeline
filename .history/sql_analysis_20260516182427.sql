SELECT product_category, COUNT(*) AS total_reviews
FROM reviews_clean
GROUP BY product_category
ORDER BY total_reviews DESC
LIMIT 10;