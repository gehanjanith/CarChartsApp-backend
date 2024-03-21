import mysql.connector

db_config = {
    'host': 'localhost',
    'port': '3308',
    'user': 'root',
    'password': '',
    'database': 'posts',
}


def get_db_connection():
    return mysql.connector.connect(**db_config)
