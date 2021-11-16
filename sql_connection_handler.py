import logging
import os

import pymysql as pymysql


def get_db_connection() -> pymysql.Connection:
    try:
        conn = pymysql.connect(
            user=os.environ['vServer_SQL_User'],
            password=os.environ['vServer_SQL_Password'],
            host='localhost',
            port=3306,
            database=os.environ['DHBW_Bot_Database']
        )
    except pymysql.Error as e:
        logging.error("SQL Connection Error:%s", e)
        conn = None
    finally:
        return conn
