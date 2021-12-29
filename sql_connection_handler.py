import logging
import pymysql
import os
from dotenv import load_dotenv


def get_db_connection() -> pymysql.Connection:
	"""
	Opens a pymysql connection and returns the connection object
	:return: The pymysql.Connection
	"""
	conn = None
	try:
		load_dotenv(".env")

		conn = pymysql.connect(
			user=os.environ.get('DB_USER'),
			password=os.environ.get('DB_PASSWORD'),
			host=os.environ.get('DB_HOST'),
			port=int(os.environ.get('DB_PORT')),
			database=os.environ.get('DB_NAME')
		)
	except Exception as e:
		logging.error("SQL Connection Error:%s", e)

	return conn
