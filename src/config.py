from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


@dataclass(frozen=True)
class CoinGeckoConfig:
    api_key: str
    api_plan: str
    base_url: str


def get_database_config() -> DatabaseConfig:
    """Read PostgreSQL connection settings from environment variables."""
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "cryptoline_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def get_coingecko_config() -> CoinGeckoConfig:
    """Read CoinGecko API settings and choose the correct API base URL."""
    api_plan = os.getenv("COINGECKO_API_PLAN", "demo").lower()
    api_key = (
        os.getenv("COINGECKO_API_KEY")
        or os.getenv("CG_DEMO_API_KEY")
        or os.getenv("CG_PRO_API_KEY")
    )

    if not api_key:
        raise ValueError(
            "Missing CoinGecko API key. Add COINGECKO_API_KEY to your .env file."
        )

    if api_plan == "pro":
        base_url = "https://pro-api.coingecko.com/api/v3"
    else:
        base_url = "https://api.coingecko.com/api/v3"

    return CoinGeckoConfig(api_key=api_key, api_plan=api_plan, base_url=base_url)
