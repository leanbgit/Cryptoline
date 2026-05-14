from typing import Any

import requests

from src.config import CoinGeckoConfig


def _auth_header(config: CoinGeckoConfig) -> dict[str, Any]:
    """Build the CoinGecko authentication header for demo or pro API keys."""
    if config.api_plan == "pro":
        return {"x-cg-pro-api-key": config.api_key}

    return {"x-cg-demo-api-key": config.api_key}


def fetch_crypto_markets(
    config: CoinGeckoConfig,
    vs_currency: str = "usd",
    per_page: int = 100,
    page: int = 1,
) -> list[dict[str, Any]]:
    
    """Fetch cryptocurrency market data from the CoinGecko markets endpoint."""
    
    url = f"{config.base_url}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }

    response = requests.get(
        url,
        params=params,
        headers=_auth_header(config),
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        raise ValueError("CoinGecko returned an unexpected response format.")

    return data
