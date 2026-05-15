CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    price_change_percentage_24h NUMERIC,
    extracted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_crypto_prices_extraction_date
    ON crypto_prices (coin_id, extracted_at DESC);