import logging
import pymysql as pymysql
from dotenv import dotenv_values


def get_db_connection() -> pymysql.Connection:
    conn = None
    try:
        config = dotenv_values(".env")

        conn = pymysql.connect(
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=int(config['DB_PORT']),
            database=config['DB_NAME']
        )
    except Exception as e:
        logging.error("SQL Connection Error:%s", e)
    finally:
        return conn
