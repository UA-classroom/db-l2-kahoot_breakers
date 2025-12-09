import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

script_dir = Path(__file__).parent

# Default name if none provided
env_file_name = os.getenv("ENV_FILE", "db_info.env")
env_path = script_dir / env_file_name
load_dotenv(dotenv_path=env_path, override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")

print(f"Connecting to database: {DATABASE_NAME}")

# setting up connectionpool
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=12,
    dbname=DATABASE_NAME,
    user="postgres",
    password=PASSWORD,
    host="localhost",
    port="5432",
)

def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return pool.getconn()


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    subscriptions = """
    CREATE TABLE IF NOT EXISTS subscriptions(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL
    )
    """

    languages = """
    CREATE TABLE IF NOT EXISTS languages(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    )
    """

    customer_types = """
        CREATE TABLE IF NOT EXISTS customer_types(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL
    )
    """

    organisations = """
        CREATE TABLE IF NOT EXISTS organisations(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    )
    """

    users = """
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        birthdate DATE NOT NULL,
        signup_date TIMESTAMP NOT NULL DEFAULT NOW(),
        name VARCHAR(255),
        subscriptions_id INT NOT NULL REFERENCES subscriptions(id) ON DELETE RESTRICT,
        language_id INT NOT NULL REFERENCES languages(id) ON DELETE RESTRICT,
        customer_type_id INT NOT NULL REFERENCES customer_types(id) ON DELETE RESTRICT,
        organisation_id INT REFERENCES organisations(id) ON DELETE SET NULL
    )
    """


    connection = get_connection()
    cur = connection.cursor()
    try:
        cur.execute(subscriptions)
        cur.execute(languages)
        cur.execute(customer_types)
        cur.execute(organisations)
        cur.execute(users)
        connection.commit()
        print("Tables created (or already existed).")
    finally:
        cur.close()
        connection.close()
    
    pass


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
