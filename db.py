import psycopg2
from db_setup import get_connection
from fastapi import HTTPException
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""

con = get_connection()

def create_subscriptions(con, name):
    query = """
    INSERT INTO subscriptions (name)
    VALUES (%s)
    RETURNING name;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (name,))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to insert the subscription name. Error message: {e}")

def create_languages(con, name):
    query = """
    INSERT INTO languages (name)
    VALUES (%s)
    RETURNING name;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (name,))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to insert the language name. Error message: {e}")

def create_customer_types(con, name):
    query = """
    INSERT INTO customer_types (name)
    VALUES (%s)
    RETURNING name;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (name,))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to insert the customer type name. Error message: {e}")

def create_users(con, username, email, password, birthdate, subscriptions_id, language_id, customer_type_id, name=None, organisation=None):
    query = """
    INSERT INTO users (username, email, password, birthdate, subscriptions_id, language_id, customer_type_id, name, organisation) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, username, email;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (username, email, password, birthdate, subscriptions_id, language_id, customer_type_id, name, organisation,))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to insert the user. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to insert the user. Error message: {e}")

def create_your_kahoot(con, title, language_id, description=None, is_private=False):
    query = """
    INSERT INTO your_kahoot (title, language_id, description, is_private) 
    VALUES (%s, %s, %s, %s)
    RETURNING id, title;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (title, language_id, description, is_private))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the kahoot. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the kahoot. Error message: {e}")

def create_kahoot_owners(con, users_id, your_kahoot_id):
    query = """
    INSERT INTO kahoot_owners (users_id, your_kahoot_id) 
    VALUES (%s, %s)
    RETURNING id, users_id, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (users_id, your_kahoot_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the kahoot ownership. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the kahoot ownership. Error message: {e}")

def create_favorite_kahoots(con, users_id, your_kahoot_id):
    query = """
    INSERT INTO favorite_kahoots (users_id, your_kahoot_id) 
    VALUES (%s, %s)
    RETURNING id, users_id, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (users_id, your_kahoot_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create favorite kahoot. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create favorite kahoot. Error message: {e}")

def create_groups(con, name, description=None):
    query = """
    INSERT INTO groups (name, description) 
    VALUES (%s, %s)
    RETURNING id, name;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (name, description))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group. Error message: {e}")

def create_user_group_members(con, user_id, group_id):
    query = """
    INSERT INTO user_group_members (user_id, group_id) 
    VALUES (%s, %s)
    RETURNING id, user_id, group_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (user_id, group_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group membership. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group membership. Error message: {e}")

def create_written_quiz(con, question, your_kahoot_id):
    query = """
    INSERT INTO quiz_with_written_answer (question, your_kahoot_id) 
    VALUES (%s, %s)
    RETURNING *;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (question, your_kahoot_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")

def create_answer_quiz(con, answer, quiz_with_written_answer_id):
    query = """
    INSERT INTO quiz_written_answer (answer, quiz_with_written_answer_id) 
    VALUES (%s, %s)
    RETURNING *;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (answer, quiz_with_written_answer_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz answer. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz answer. Error message: {e}")

def create_true_false_quiz(con, question, answer, your_kahoot_id):
    query = """
    INSERT INTO quiz_with_true_false (question, answer, your_kahoot_id)
    VALUES (%s, %s, %s)
    RETURNING *;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (question, answer, your_kahoot_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")

def create_presentation_classic(con, your_kahoot_id, title=None, text=None):
    query = """
    INSERT INTO presentation_classic (title, text, your_kahoot_id)
    VALUES (%s, %s, %s)
    RETURNING *;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (title, text, your_kahoot_id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the presenation. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the presentation. Error message: {e}")














print(create_presentation_classic(con, 1, "jaaaaaa", "mkt mkt mk text"))







#print(create_users(con, "HassanM", "aa@dd.se", "hemligt", "1990-01-07", 1, 1, 1, "hassan mehdi", "SEB banken"))


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id
