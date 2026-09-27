# Canteen Food Sharing and Surplus Management System

A Flask web application that lets college canteen staff list surplus food after service hours, so students and authorized users can view and claim available portions before a pickup deadline — reducing food wastage.

**Live application:** https://canteen-food-sharing.onrender.com

## Features

- Home page displaying available surplus food, with quantity, description, and pickup deadline
- Form for canteen staff to add new surplus food listings
- Claim button for users to reserve a portion, with server-side prevention of over-claiming
- `/health` endpoint for uptime/monitoring checks
- `/api/food` JSON endpoint for programmatic access to current listings
- Clean, responsive, canteen-themed interface

## Technology Stack

- **Backend:** Python 3.14, Flask 3.1
- **Database:** PostgreSQL 17, accessed via Psycopg 3
- **Frontend:** HTML, Jinja templates, CSS
- **Testing:** pytest, using an isolated test database
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Deployment:** Render (Docker-based Web Service + managed PostgreSQL)

## Architecture

Browser sends a request to the Flask app (`app.py`), which reads from and writes to a PostgreSQL database, then renders the response back to the browser.

Food listings and claims are stored persistently in a PostgreSQL `food_items` table. Environment-specific configuration (database credentials, secrets) is provided via environment variables, never hardcoded in source code.

In production, the app runs inside a Docker container on Render, using Gunicorn as the WSGI server, and connects to a separate managed PostgreSQL instance also hosted on Render.

## Local Setup

1. Clone this repository.
2. Create and activate a Python 3.14 virtual environment: