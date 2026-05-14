from datetime import datetime
from airflow.sdk import dag, task
from src.run_crypto_prices_etl import run_crypto_prices_etl


@dag(
    dag_id="crypto_prices_etl",
    description="Extract cryptocurrency market data from CoinGecko and load it into PostgreSQL.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["crypto", "coingecko", "etl"],
)
def crypto_prices_etl_dag():
    """Define the Airflow workflow that runs the crypto prices ETL."""

    @task
    def load_crypto_prices() -> int:
        """Run the ETL pipeline and return the number of rows inserted."""
        return run_crypto_prices_etl(per_page=100, page=1)

    load_crypto_prices()


crypto_prices_etl_dag()
