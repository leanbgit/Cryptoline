-- A view for the latest prices to use for other queries
CREATE OR REPLACE VIEW latest_crypto_prices AS
WITH ranked_prices AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY coin_id
        ORDER BY extracted_at DESC
        ) AS row_number
    FROM crypto_prices
)
SELECT
    coin_id,
    symbol,
    name,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h,
    extracted_at
FROM ranked_prices
WHERE row_number = 1;

-- Top 10 cryptos by market cap
CREATE OR REPLACE VIEW top_10_crypto_by_market_cap AS
SELECT
    coin_id,
    symbol,
    name,
    market_cap,
    current_price,
    extracted_at
FROM latest_crypto_prices
ORDER BY market_cap DESC NULLS LAST
LIMIT 10;

-- Top 10 cryptos by volume
CREATE OR REPLACE VIEW top_10_crypto_by_volume AS
SELECT
    coin_id,
    symbol,
    name,
    total_volume,
    current_price,
    extracted_at
FROM latest_crypto_prices
ORDER BY total_volume DESC NULLS LAST
LIMIT 10;

-- Top 10 gainers in last 24 hs
CREATE OR REPLACE VIEW top_10_crypto_gainers_24h AS
SELECT
    coin_id,
    symbol,
    name,
    price_change_percentage_24h,
    current_price,
    extracted_at
FROM latest_crypto_prices
ORDER BY price_change_percentage_24h DESC NULLS LAST
LIMIT 10;

-- Top 10 losers in last 24 hs
CREATE OR REPLACE VIEW top_10_crypto_losers_24h AS
SELECT
    coin_id,
    symbol,
    name,
    price_change_percentage_24h,
    current_price,
    extracted_at
FROM latest_crypto_prices
ORDER BY price_change_percentage_24h ASC NULLS LAST
LIMIT 10;
