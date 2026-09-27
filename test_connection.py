import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print("Connecting using:", database_url)

connection = psycopg.connect(database_url)
print("Connected successfully!")

connection.close()
print("Connection closed.")