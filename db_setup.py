import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

script_dir = Path(__file__).parent

# Default name if none provided
env_file_name = os.getenv("ENV_FILE", ".env")
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

    your_kahoot = """
        CREATE TABLE IF NOT EXISTS your_kahoot(
        id SERIAL PRIMARY KEY,
        title VARCHAR(80) NOT NULL,
        description VARCHAR(500),
        is_private BOOLEAN,
        language_id INT NOT NULL REFERENCES languages(id) ON DELETE RESTRICT
    )
    """

    time_limits = """
        CREATE TABLE IF NOT EXISTS time_limits(
        id SERIAL PRIMARY KEY,
        length NUMERIC(5,2),
        your_kahoot_id INT UNIQUE REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    images = """
        CREATE TABLE IF NOT EXISTS images(
        id SERIAL PRIMARY KEY,
        link VARCHAR(500),
        your_kahoot_id INT UNIQUE REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    kahoot_owners = """
        CREATE TABLE IF NOT EXISTS kahoot_owners(
        id SERIAL PRIMARY KEY,
        users_id INT REFERENCES users(id) ON DELETE SET NULL,
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL,
        UNIQUE(users_id, your_kahoot_id)
    )
    """

    favorite_kahoots = """
        CREATE TABLE IF NOT EXISTS favorite_kahoots(
        id SERIAL PRIMARY KEY,
        users_id INT REFERENCES users(id) ON DELETE SET NULL,
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL,
        UNIQUE(users_id, your_kahoot_id)
    )
    """

    kahoot_report = """
        CREATE TABLE IF NOT EXISTS kahoot_report(
        id SERIAL PRIMARY KEY,
        total_questions INT NOT NULL,
        total_participants INT NOT NULL,
        correct_answers INT,
        duration INTERVAL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    groups = """
        CREATE TABLE IF NOT EXISTS groups(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description VARCHAR(200)
        )
        """

    user_group_members = """
    CREATE TABLE IF NOT EXISTS user_group_members(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
	group_id INT REFERENCES groups(id) ON DELETE SET NULL,
	UNIQUE(user_id, group_id)
    )
    """

    groups_and_kahoots = """
    CREATE TABLE IF NOT EXISTS groups_and_kahoots(
    id SERIAL PRIMARY KEY,
    group_id INT REFERENCES groups(id) ON DELETE SET NULL,
	your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL,
	UNIQUE(group_id, your_kahoot_id)
    )
    """

    group_messages = """
        CREATE TABLE IF NOT EXISTS group_messages(
        id SERIAL PRIMARY KEY,
        text VARCHAR(400) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        user_id INT REFERENCES users(id) ON DELETE SET NULL,
        group_id INT REFERENCES groups(id) ON DELETE SET NULL
    )
    """

    saved_payment_card = """
        CREATE TABLE IF NOT EXISTS saved_payment_card(
        id SERIAL PRIMARY KEY,
        payment_provider VARCHAR(20),
        payment_method_token VARCHAR(255),
        card_type VARCHAR(50) CHECK (card_type IN ('Visa', 'Mastercard', 'American Express')),
        last_four CHAR(4),
        expiration_month INT,
        expiration_year INT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        user_id INT REFERENCES users(id) ON DELETE SET NULL
    )
    """

    saved_paypal = """
        CREATE TABLE IF NOT EXISTS saved_paypal(
        id SERIAL PRIMARY KEY,
        payment_method_token VARCHAR(255),
        firstname VARCHAR(100),
        lastname VARCHAR(100),
        payment_email VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        user_id INT REFERENCES users(id) ON DELETE SET NULL
    )
    """

    saved_google_pay = """
        CREATE TABLE IF NOT EXISTS saved_google_pay(
        id SERIAL PRIMARY KEY,
        payment_method_token VARCHAR(255),
        firstname VARCHAR(100),
        lastname VARCHAR(100),
        payment_email VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        user_id INT REFERENCES users(id) ON DELETE SET NULL
    )
    """

    transactions = """
        CREATE TABLE IF NOT EXISTS transactions(
        id SERIAL PRIMARY KEY,
        payment_method_token VARCHAR(255),
        amount DECIMAL(10,2),
        currency CHAR(3),
        status VARCHAR(20),
        provider VARCHAR(20),
        transaction_id VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        subscriptions_id INT REFERENCES subscriptions(id) ON DELETE SET NULL,
        saved_payment_card_id INT REFERENCES saved_payment_card(id) ON DELETE SET NULL,
        saved_paypal_id INT REFERENCES saved_paypal(id) ON DELETE SET NULL,
        saved_google_pay_id INT REFERENCES saved_google_pay(id) ON DELETE SET NULL,
        user_id INT REFERENCES users(id) ON DELETE SET NULL
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
