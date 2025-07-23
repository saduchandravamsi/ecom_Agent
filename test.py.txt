import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password='vamsi@124216',  # <<< This is important! Use the literal password here, not os.getenv!
        database=os.getenv('MYSQL_DATABASE')
    )
    print("Successfully connected to MySQL!")
    conn.close()
except Exception as e:
    print("MySQL connection failed:", e)
