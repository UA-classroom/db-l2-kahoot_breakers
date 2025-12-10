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

def read_all_users(con):
    query = """
    SELECT * FROM users;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")

def read_all_kahoots(con):
    query = """
    SELECT * FROM your_kahoot;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the kahoots. Error message: {e}")

def read_all_groups(con):
    query = """
    SELECT * FROM groups;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the groups. Error message: {e}")

def read_users_joined_kahoot(con):
    # This query is complicated but necessary.
    # I have my users table that is on the left side, and want to join it to the your_kahoot table,
    # to see all the kahoots a user have. The problem is in your_kahoot table there is no foreign key stored
    # for the users, beacuse there is an intermediate table that store the relationship.
    # Therefore to reach your_kahoot we need to left join 3 tables.
    # And lastly user.id and your_kahoot.id is renamed with alias because both tables use id as a primary key name.
    query = """
    SELECT 
        users.id AS user_id,
        users.username,
        users.email,
        your_kahoot.id AS kahoot_id,
        your_kahoot.title,
        your_kahoot.description,
        your_kahoot.is_private
    FROM users
    LEFT JOIN kahoot_owners
        ON users.id = kahoot_owners.users_id
    LEFT JOIN your_kahoot
        ON kahoot_owners.your_kahoot_id = your_kahoot.id
    ORDER BY users.id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")

def read_users_favorite_kahoot(con):
    # We have users table that is on the left side, and want to join it to favorite_kahoot,
    # to see all the favorite kahoots a user have. The problem is that favorite_kahoot only stores the relationship
    # and not other data, therefore we still need to tripple join it with your_kahoot where data is stored.
    # We use alias for id because both table have the same name for id.
    # We use order by because otherwise the order will be different every time the function is called.
    query = """
    SELECT 
        users.id AS user_id,
        users.username,
        users.name,
        users.email,
        users.organisation,
        your_kahoot.id AS kahoot_id,
        your_kahoot.title,
        your_kahoot.description,
        your_kahoot.is_private
    FROM users
    LEFT JOIN favorite_kahoots
        ON users.id = favorite_kahoots.users_id
    LEFT JOIN your_kahoot
        ON favorite_kahoots.your_kahoot_id = your_kahoot.id
    ORDER BY users.id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")

def read_users_groups(con):
    # We have our users table that is on the left side, and want to join it to the groups table,
    # to see which group a user belongs to. The problem is in the groups table there is no foreign key stored,
    # thats why we need to tripple join it with the intermediate table where the relationship is stored.
    query = """
    SELECT 
        users.id AS user_id,
        users.username,
        users.name,
        users.birthdate,
        users.email,
        groups.id AS group_id,
        groups.name AS group_name,
        groups.description AS group_description
    FROM users
    LEFT JOIN user_group_members
        ON users.id = user_group_members.user_id
    LEFT JOIN groups
        ON user_group_members.group_id = groups.id
    ORDER BY users.id ASC;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")

def read_individual_user(con, primary_key_id):
    query = """
    SELECT id, username, email, birthdate, signup_date, name, organisation FROM users WHERE id = %s;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (primary_key_id,))
                result = cur.fetchone()
                # error handling if no user is found with provided primary key
                if result is None:
                    raise HTTPException(status_code=400, detail="No user found with provided primary key id.")
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")










print(read_individual_user(con, 3))






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
