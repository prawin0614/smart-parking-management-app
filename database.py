import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="smart-parking-mysql-prawin2026.mysql.database.azure.com",
        user="parkingadmin",
        password="praWin@06",
        database="parking_db",
        port=3306
    )