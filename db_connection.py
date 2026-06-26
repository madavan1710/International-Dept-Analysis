# db_connection.py

import psycopg2

def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="international_debt_analysis",
        user="postgres",
        password="1127"    )

    return conn

# test_connection.py

from db_connection import get_connection

# Connection with PostgreSQL database
conn = get_connection()

print("Connected Successfully!")

conn.close()