import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import DatabaseError
from psycopg2.pool import SimpleConnectionPool

load_dotenv()

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
    Retrieve a database connection from the connection pool.

    Returns:
        A psycopg2 connection object from the pool.
    """
    return pool.getconn()


def release_connection(conn):
    """
    Return a database connection to the pool.

    Args:
        conn: A psycopg2 connection object to return to the pool.
    """
    pool.putconn(conn)


def create_tables(con):
    """
    This function executes a series of SQL CREATE TABLE statements
    to ensure that all required tables exist in the connected PostgreSQL
    database. If a table already exists, it will not be recreated.

    Args:
        con: An active database connection object.

    Raises:
        psycopg2.IntegrityError: If any constraint violations occur while
            creating the tables.
        psycopg2.DatabaseError: If there is a general error when executing SQL
            statements in the database.
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

    users = """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        birthdate DATE NOT NULL,
        signup_date TIMESTAMP NOT NULL DEFAULT NOW(),
        name VARCHAR(255),
        organisation VARCHAR(50),
        subscriptions_id INT NOT NULL REFERENCES subscriptions(id) ON DELETE RESTRICT,
        language_id INT NOT NULL REFERENCES languages(id) ON DELETE RESTRICT,
        customer_type_id INT NOT NULL REFERENCES customer_types(id) ON DELETE RESTRICT
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

    quiz_with_written_answer = """
    CREATE TABLE IF NOT EXISTS quiz_with_written_answer(
        id SERIAL PRIMARY KEY,
        question VARCHAR(100) NOT NULL,
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    quiz_written_answer = """
    CREATE TABLE IF NOT EXISTS quiz_written_answer(
        id SERIAL PRIMARY KEY,
        answer VARCHAR(100) NOT NULL,
        quiz_with_written_answer_id INT REFERENCES quiz_with_written_answer(id) ON DELETE SET NULL
    )
    """

    quiz_with_true_false = """
    CREATE TABLE IF NOT EXISTS quiz_with_true_false(
        id SERIAL PRIMARY KEY,
        question VARCHAR(100) NOT NULL,
        answer BOOLEAN NOT NULL,
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    presentation_classic = """
    CREATE TABLE IF NOT EXISTS presentation_classic(
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        text VARCHAR(500),
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    survey_open_question = """
    CREATE TABLE IF NOT EXISTS survey_open_question(
        id SERIAL PRIMARY KEY,
        question VARCHAR(100),
        answer_text VARCHAR(250),
        your_kahoot_id INT REFERENCES your_kahoot(id) ON DELETE SET NULL
    )
    """

    try:
        with con:
            with con.cursor() as cur:
                cur.execute(subscriptions)
                cur.execute(languages)
                cur.execute(customer_types)
                cur.execute(users)
                cur.execute(your_kahoot)
                cur.execute(images)
                cur.execute(kahoot_owners)
                cur.execute(favorite_kahoots)
                cur.execute(kahoot_report)
                cur.execute(groups)
                cur.execute(user_group_members)
                cur.execute(groups_and_kahoots)
                cur.execute(group_messages)
                cur.execute(saved_payment_card)
                cur.execute(saved_paypal)
                cur.execute(saved_google_pay)
                cur.execute(transactions)
                cur.execute(quiz_with_written_answer)
                cur.execute(quiz_written_answer)
                cur.execute(quiz_with_true_false)
                cur.execute(presentation_classic)
                cur.execute(survey_open_question)
                print("Tables created (or already existed).")
    except psycopg2.IntegrityError as e:
        print(f"There has been error regarding database rules and constraints. Error message: {e}")
    except DatabaseError as e:
        print(f"There has been error creating tables in database. Error message: {e}")


if __name__ == "__main__":
        try:
            con = get_connection()
            create_tables(con)
        finally:
            con.close()
