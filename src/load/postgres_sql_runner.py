from pathlib import Path

import psycopg2

from src.config import DatabaseConfig


def execute_sql_file(config: DatabaseConfig, sql_file_path: str) -> None:
    """Execute every SQL statement from a file against PostgreSQL."""
    sql = Path(sql_file_path).read_text(encoding="utf-8")

    with psycopg2.connect(
        host=config.host,
        port=config.port,
        dbname=config.database,
        user=config.user,
        password=config.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
