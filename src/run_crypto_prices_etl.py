import argparse

from src.config import get_coingecko_config, get_database_config
from src.extract.coingecko_client import fetch_crypto_markets
from src.load.postgres_loader import load_crypto_prices
from src.transform.crypto_market import transform_market_data


def run_crypto_prices_etl(per_page: int = 100, page: int = 1) -> int:
    """Run the full crypto prices ETL and return the number of inserted rows."""
    coingecko_config = get_coingecko_config()
    database_config = get_database_config()

    raw_records = fetch_crypto_markets(
        config=coingecko_config,
        per_page=per_page,
        page=page,
    )
    cleaned_records = transform_market_data(raw_records)

    return load_crypto_prices(database_config, cleaned_records)


def main() -> None:
    """Parse command line arguments and start the crypto prices ETL."""
    parser = argparse.ArgumentParser(description="Load CoinGecko market data.")
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    inserted_count = run_crypto_prices_etl(
        per_page=args.per_page,
        page=args.page,
    )
    print(f"Inserted {inserted_count} crypto price records.")


if __name__ == "__main__":
    main()
