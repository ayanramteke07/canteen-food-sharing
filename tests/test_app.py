import os

import psycopg
import pytest
from dotenv import load_dotenv

from app import app

load_dotenv()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Clean the test database before every single test, so tests never
    # depend on leftover data from a previous test run.
    test_database_url = os.getenv("TEST_DATABASE_URL")
    connection = psycopg.connect(test_database_url)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM food_items;")
    connection.commit()
    cursor.close()
    connection.close()

    with app.test_client() as test_client:
        yield test_client


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add_food_and_see_it_on_home_page(client):
    response = client.post(
        "/add",
        data={
            "name": "Test Biryani",
            "description": "A test item for pytest",
            "quantity": "5",
            "pickup_deadline": "2026-09-27 19:00:00",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test Biryani" in response.data


def test_add_food_with_missing_fields_is_rejected(client):
    response = client.post(
        "/add",
        data={
            "name": "",
            "description": "",
            "quantity": "5",
            "pickup_deadline": "2026-09-27 19:00:00",
        },
    )
    assert response.status_code == 200
    assert b"All fields are required." in response.data


def test_add_food_with_invalid_quantity_is_rejected(client):
    response = client.post(
        "/add",
        data={
            "name": "Bad Quantity Item",
            "description": "Should not be added",
            "quantity": "not-a-number",
            "pickup_deadline": "2026-09-27 19:00:00",
        },
    )
    assert response.status_code == 200
    assert b"Quantity must be a whole number." in response.data


def test_api_food_returns_json_list(client):
    client.post(
        "/add",
        data={
            "name": "API Test Item",
            "description": "For testing the JSON route",
            "quantity": "2",
            "pickup_deadline": "2026-09-27 19:00:00",
        },
    )
    response = client.get("/api/food")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(item["name"] == "API Test Item" for item in data)
