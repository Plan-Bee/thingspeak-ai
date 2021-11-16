import pymysql

import sql_connection_handler as db_handler


def fetch_thingspeak_data(id: int) -> [tuple]:
    conn = db_handler.get_db_connection()
    cur = conn.cursor()

    select_temperature_data = """
    SELECT 
        broodroom_temperature,
        outdoor_temperature,
        timestamp 
    FROM 
        honeypi_data 
    WHERE 
        hive_id = %s
    """

    cur.execute(select_temperature_data, id)
    temperature_data = cur.fetchall()

    return temperature_data


if __name__ == '__main__':
    for broodroom_temperature, outdoor_temperature, timestamp in fetch_thingspeak_data(1):
        print(timestamp, broodroom_temperature, outdoor_temperature)
