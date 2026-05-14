from datetime import datetime
from airflow.sdk import dag, task
from src.extract.coingecko_client import fetch_crypto_markets
from src.config import get_coingecko_config, get_database_config
from src.transform.crypto_market import transform_market_data
from src.load.postgres_loader import load_crypto_prices



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
    def extract_crypto_data():
        """Extracts crypto data using coingecko"""
        config = get_coingecko_config()
        return fetch_crypto_markets(config)
    @task()
    def transform_crypto_data(raw_data):
        """Transforms data and keeps only relevant information"""
        return transform_market_data(raw_data)
    @task()
    def load_crypto_data(refined_data):
        """Loads the refined and clean data into Postgres"""
        dbconfig = get_database_config()
        return load_crypto_prices(dbconfig, refined_data)
    
    raw_data = extract_crypto_data()
    refined_data = transform_crypto_data(raw_data)
    load_crypto_data(refined_data)

crypto_prices_etl_dag()
