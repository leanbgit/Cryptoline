import psycopg2
from psycopg2.extras import execute_values

from src.config import DatabaseConfig


INSERT_CRYPTO_PRICES_SQL = """
    INSERT INTO crypto_prices (
        coin_id,
        symbol,
        name,
        current_price,
        market_cap,
        total_volume,
        price_change_percentage_24h
    )
    VALUES %s
"""


def load_crypto_prices(config: DatabaseConfig, records: list[dict]) -> int:
    """Insert transformed cryptocurrency price records into PostgreSQL."""
    if not records:
        return 0

    values = [
        (
            record["coin_id"],
            record["symbol"],
            record["name"],
            record["current_price"],
            record["market_cap"],
            record["total_volume"],
            record["price_change_percentage_24h"],
        )
        for record in records
    ]

    with psycopg2.connect(
        host=config.host,
        port=config.port,
        dbname=config.database,
        user=config.user,
        password=config.password,
    ) as connection:
        with connection.cursor() as cursor:
            execute_values(cursor, INSERT_CRYPTO_PRICES_SQL, values)

    return len(records)
