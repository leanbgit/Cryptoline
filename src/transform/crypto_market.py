from typing import Any


def transform_market_data(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the CoinGecko fields needed by the crypto_prices table."""
    cleaned_records = []

    for record in records:
        cleaned_records.append(
            {
                "coin_id": record.get("id"),
                "symbol": record.get("symbol"),
                "name": record.get("name"),
                "current_price": record.get("current_price"),
                "market_cap": record.get("market_cap"),
                "total_volume": record.get("total_volume"),
                "price_change_percentage_24h": record.get(
                    "price_change_percentage_24h"
                ),
            }
        )

    return cleaned_records
