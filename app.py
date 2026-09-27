import os

import psycopg
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request
from psycopg.rows import dict_row

load_dotenv()

app = Flask(__name__)
COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]
def get_database_url():
    if app.config.get("TESTING"):
        return os.getenv("TEST_DATABASE_URL")
    return os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(get_database_url(), row_factory=dict_row)


@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM food_items ORDER BY id;")
    food_items = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", food_items=food_items, commit=COMMIT)


@app.route("/add", methods=["GET", "POST"])
def add_food():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        quantity_raw = request.form.get("quantity", "")
        pickup_deadline = request.form.get("pickup_deadline", "").strip()

        if not name or not description or not pickup_deadline:
            return render_template("add_food.html", error="All fields are required.")

        try:
            quantity = int(quantity_raw)
        except ValueError:
            return render_template("add_food.html", error="Quantity must be a whole number.")

        if quantity < 1:
            return render_template("add_food.html", error="Quantity must be at least 1.")

        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO food_items
                (name, description, total_quantity, remaining_quantity, pickup_deadline)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (name, description, quantity, quantity, pickup_deadline),
            )
            connection.commit()
        except psycopg.errors.DatatypeMismatch:
            connection.rollback()
            return render_template(
                "add_food.html",
                error="Pickup deadline must be a valid date and time, e.g. 2026-09-27 18:00:00.",
            )
        finally:
            cursor.close()
            connection.close()

        return redirect("/")

    return render_template("add_food.html", error=None)


@app.route("/claim/<int:item_id>", methods=["POST"])
def claim_food(item_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Prevent claiming more portions than are available.
    # This single SQL statement only updates the row if remaining_quantity > 0,
    # so it's safe even if two people click "claim" at almost the same time.
    cursor.execute(
        """
        UPDATE food_items
        SET remaining_quantity = remaining_quantity - 1,
            claimed = (remaining_quantity - 1 = 0)
        WHERE id = %s AND remaining_quantity > 0;
        """,
        (item_id,),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/")


@app.route("/api/food")
def api_food():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM food_items ORDER BY id;")
    food_items = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert date/time values to plain text so jsonify can handle them.
    for item in food_items:
        item["pickup_deadline"] = item["pickup_deadline"].isoformat()
        item["created_at"] = item["created_at"].isoformat()

    return jsonify(food_items)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
