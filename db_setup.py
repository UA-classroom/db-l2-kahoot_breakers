import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")

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
    connection = get_connection()
    # Implement
    pass


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
