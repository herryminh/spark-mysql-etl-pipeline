-- =========================
-- 1. Total Reviews
-- =========================
SELECT COUNT(*) AS total_reviews
FROM reviews_clean;

-- =========================
-- 2. Average Rating
-- =========================
SELECT AVG(star_rating) AS avg_rating
FROM reviews_clean;

-- =========================
-- 3. Top Product Categories
-- =========================
SELECT product_category,
COUNT(*) AS total_reviews
FROM reviews_clean
GROUP BY product_category
ORDER BY total_reviews DESC
LIMIT 10;

-- =========================
-- 4. Longest Reviews
-- =========================
SELECT review_headline,
review_length
FROM reviews_clean
ORDER BY review_length DESC
LIMIT 5;

-- =========================
-- 5. Verified Purchases
-- =========================
SELECT verified_purchase,
COUNT(*) AS total
FROM reviews_clean
GROUP BY verified_purchase;
