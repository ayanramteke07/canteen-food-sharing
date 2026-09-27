import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS food_items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    total_quantity INTEGER NOT NULL CHECK (total_quantity > 0),
    remaining_quantity INTEGER NOT NULL CHECK (remaining_quantity >= 0),
    pickup_deadline TIMESTAMP NOT NULL,
    claimed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

connection = psycopg.connect(test_database_url)
cursor = connection.cursor()
cursor.execute(CREATE_TABLE_SQL)
connection.commit()
cursor.close()
connection.close()

print("Test database table 'food_items' created (or already existed).")
