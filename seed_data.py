import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

INSERT_SQL = """
INSERT INTO food_items (name, description, total_quantity, remaining_quantity, pickup_deadline)
VALUES (%s, %s, %s, %s, %s);
"""

starter_items = [
    ("Vegetable Samosas", "Freshly made samosas from lunch service, mildly spiced.", 20, 20, "2026-09-27 18:00:00"),
    ("Paneer Sandwiches", "Grilled sandwiches, extra from the counter.", 10, 10, "2026-09-27 18:30:00"),
]

connection = psycopg.connect(database_url)
cursor = connection.cursor()

for item in starter_items:
    cursor.execute(INSERT_SQL, item)

connection.commit()
cursor.close()
connection.close()

print(f"Inserted {len(starter_items)} starter food items.")