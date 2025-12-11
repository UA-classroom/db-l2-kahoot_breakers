import psycopg2
from fastapi import HTTPException
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

# from db_setup import (
#     get_connection,  # TODO REMOVE THIS BEFORE SENDING IN, for testing in this file
# )

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

# con = get_connection()  # Don't create connection at module level

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

# 5 Update
# 5 Delete
# 1 partial update (ändra e-mail tex)

# # INPUTS
# # Test inputs for database creation functions

def test_inputs():
    subscriptions_tests = [
        "Premium",
        "Basic", 
        "Premium",
        "FREE-UPPERCASE",
        "  trimmed-sub  ",
    ]

    for name in subscriptions_tests:
        create_subscriptions(con, name)  # con is your actual connection variable

    # create_languages inputs
    languages_tests = [
        "English",      # → Inserts new language "English"
        "Swedish",      # → Inserts new language "Swedish"
        # "English",      # → Raises UniqueViolation (already exists)
        "sv-SE",        # → Inserts locale format "sv-SE"
        "日本語"         # → Inserts Unicode "日本語"
    ]

    for name in languages_tests:
        create_languages(con, name)

    # create_customer_types inputs
    customer_types_tests = [
        "Individual",     # → Inserts new customer type "Individual"
        "Business",       # → Inserts new customer type "Business"
        # "Individual",     # → Raises UniqueViolation (already exists)
        "B2B-Enterprise", # → Inserts "B2B-Enterprise"
        "Non-Profit"      # → Inserts "Non-Profit"
    ]

    for name in customer_types_tests:
        create_customer_types(con, name)

    # create_users inputs (assumes subscriptions_id=1, language_id=1, customer_type_id=1 exist)
    users_tests = [
        ("john_doe", "john@example.com", "hashedpass1", "1990-05-15", 1, 1, 1),  # → Creates user with no name/organisation
        ("jane_smith", "jane@test.se", "hashedpass2", "1985-12-03", 1, 1, 1, "Jane Smith"),  # → Creates with name only
        # ("test_user", "test@example.com", "pass", "2000-01-01", 999, 1, 1),  # → Raises ForeignKeyViolation (invalid subscriptions_id)
        # ("admin", "admin@company.se", "adminpass", "1970-01-01", 1, 999, 1),  # → Raises ForeignKeyViolation (invalid language_id)
        ("user5", "user5@org.com", "pass5", "1995-07-20", 1, 1, 1, "User Five", "TechCorp")  # → Creates full user with all fields
    ]

    for args in users_tests:
        create_users(con, *args)
    
        # your_kahoot
    your_kahoot_tests = [
        ("My first kahoot", 1),
        ("Swedish capitals", 1, "Quiz about Swedish geography"),
        ("Private math quiz", 1, "Algebra basics", True),
        ("No description public", 1, None, False),
    ]

    for args in your_kahoot_tests:
        create_your_kahoot(con, *args)


    # kahoot_owners
    kahoot_owners_tests = [
        (1, 1),   # user 1 → kahoot 1
        (1, 2),   # user 1 → kahoot 2
        (2, 1),   # user 2 → kahoot 1
    ]

    for users_id, your_kahoot_id in kahoot_owners_tests:
        create_kahoot_owners(con, users_id, your_kahoot_id)


    # favorite_kahoots
    favorite_kahoots_tests = [
        (1, 1),
        (1, 2),
        (2, 1),
    ]

    for users_id, your_kahoot_id in favorite_kahoots_tests:
        create_favorite_kahoots(con, users_id, your_kahoot_id)


    # groups
    groups_tests = [
        ("Teachers", "Internal teacher group"),
        ("Students", "All students in class 9A"),
        ("Empty description group", None),
        ("Special chars ✓", "Unicode test"),
    ]

    for name, description in groups_tests:
        create_groups(con, name, description)


    # user_group_members
    user_group_members_tests = [
        (1, 1),
        (1, 2),
        (2, 1),
    ]

    for user_id, group_id in user_group_members_tests:
        create_user_group_members(con, user_id, group_id)


    # written quiz
    written_quiz_tests = [
        ("What is 2+2?", 1),
        ("Capital of Sweden?", 1),
        ("Long description question...", 2),
    ]

    for question, your_kahoot_id in written_quiz_tests:
        create_written_quiz(con, question, your_kahoot_id)


    # written quiz answers
    answer_quiz_tests = [
        ("4", 1),
        ("Stockholm", 2),
        ("Wrong but valid", 1),
    ]

    for answer, quiz_with_written_answer_id in answer_quiz_tests:
        create_answer_quiz(con, answer, quiz_with_written_answer_id)


    # true/false quiz
    true_false_quiz_tests = [
        ("The earth is flat", False, 1),
        ("Stockholm is in Sweden", True, 1),
        ("Edge case question", True, 2),
    ]

    for question, answer, your_kahoot_id in true_false_quiz_tests:
        create_true_false_quiz(con, question, answer, your_kahoot_id)


    # presentation_classic
    presentation_classic_tests = [
        ("Intro slide", "Welcome to this kahoot", 1),
        ("Rules", "Answer fast to get more points", 1),
        (None, "Text-only slide", 1),
        ("Title only", None, 1),
    ]

    for title, text, your_kahoot_id in presentation_classic_tests:
        create_presentation_classic(con, your_kahoot_id, title, text)


####
def clear_tables(con):
    with con:
        with con.cursor() as cur:
            cur.execute("""
                TRUNCATE TABLE
                    users,
                    subscriptions,
                    languages,
                    customer_types,
                    your_kahoot,
                    kahoot_owners,
                    favorite_kahoots,
                    groups,
                    user_group_members,
                    quiz_with_written_answer,
                    quiz_written_answer,
                    quiz_with_true_false,
                    presentation_classic
                RESTART IDENTITY CASCADE
            """)
    print("All tables TRUNCATED (IDs reset to 1)!")

def delete_user_by_username(con, username):
    query = """
    DELETE FROM users 
    WHERE username = %s
    RETURNING id, username, email;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (username,))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="User not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the user. Error message: {e}")

def delete_your_kahoot_by_id(con, your_kahoot_id):
    query = """
    DELETE FROM your_kahoot 
    WHERE id = %s
    RETURNING id, title, description;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (your_kahoot_id, ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Kahoot id not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the Kahoot with that id. Error message: {e}")

def delete_quiz_question_with_written_answer(con, quiz_with_written_answer_id):
    query = """
    DELETE FROM quiz_with_written_answer
    WHERE id = %s
    RETURNING id, question, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (quiz_with_written_answer_id, ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz question not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the Quiz question with that id. Error message: {e}")
    # FIXME should this have a confirmation message, i.e blba bla deleted?
    # FIXME borde inte frågan + svaren deletas samtidigt?!

def delete_quiz_answer_with_written_answer(con, quiz_written_answer_id):
    query = """
    DELETE FROM quiz_written_answer
    WHERE id = %s
    RETURNING id, answer, quiz_with_written_answer_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (quiz_written_answer_id, ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz answer not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the Quiz answer with that id. Error message: {e}")
    # FIXME should this have a confirmation message, i.e blba bla deleted?
    # FIXME borde inte frågan + svaren deletas samtidigt?!

def delete_quiz_with_true_false(con, quiz_with_true_false_id):
    query = """
    DELETE FROM quiz_with_true_false
    WHERE id = %s
    RETURNING id, question, answer, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (quiz_with_true_false_id, ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz answer not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the Quiz answer with that id. Error message: {e}")
    # FIXME should this have a confirmation message, i.e blba bla deleted?

def update_quiz_with_true_false(con, id, question, answer, your_kahoot_id):
    query = """
    UPDATE quiz_with_true_false 
    SET question = %s, answer = %s, your_kahoot_id = %s
    WHERE id = %s
    RETURNING id, question, answer, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (question, answer, your_kahoot_id, id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz answer/question id not found, no update could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Quiz answer/question id not found, no update could be made. Error message: {e}")

def update_quiz_answer_with_written_answer(con, id, quiz_with_written_answer_id, answer):
    query = """
    UPDATE quiz_written_answer
    SET answer = %s, quiz_with_written_answer_id = %s
    WHERE id = %s
    RETURNING id, answer, quiz_with_written_answer_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (answer, quiz_with_written_answer_id, id ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz answer not found, no update could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the Quiz answer with that id. Error message: {e}")

def update_quiz_question_with_written_answer(con, id, question, your_kahoot_id):
    query = """
    UPDATE quiz_with_written_answer
    SET question = %s, your_kahoot_id = %s
    WHERE id = %s
    RETURNING id, question, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (question, your_kahoot_id, id ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz question not found, no update could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the Quiz question with that id. Error message: {e}")
    # FIXME should this have a confirmation message, i.e blba bla deleted?
    # FIXME borde inte frågan + svaren deletas samtidigt?!

def update_your_kahoot_by(con, your_kahoot_id, title, description, is_private, language_id):
    query = """
    UPDATE your_kahoot 
    SET title = %s, description = %s, is_private = %s, language_id = %s
    WHERE id = %s
    RETURNING id, title, description;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (title, description, is_private, language_id, your_kahoot_id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Kahoot id not found, no update could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the Kahoot with that id. Error message: {e}")
    
def update_groups(con, id, name, description):
    query = """
    UPDATE groups
    SET name = %s, description = %s
    WHERE id = %s
    RETURNING name, description, id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (name, description, id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Group not found, no update could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the user. Error message: {e}")

def update_presentation_classic(con, id, your_kahoot_id, title=None, text=None):
    query = """
    UPDATE presentation_classic 
    SET title = %s, text = %s, your_kahoot_id = %s 
    WHERE id = %s
    RETURNING *;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (title, text, your_kahoot_id, id))
                result = cur.fetchone()
                return result
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the presenation. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to update the presentation. Error message: {e}")

def patch_question_quiz_with_true_false(con, id, question):
    query = """
    UPDATE quiz_with_true_false
    SET question = %s
    WHERE id = %s
    RETURNING id, question, answer, your_kahoot_id;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (question, id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Quiz answer/question id not found, no update could be made")
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Database error while updating quiz. Error message: {e}")

# clear_tables(con)
# test_inputs()

# # Example calls for delete functions
#=====================================================
# delete_user_by_username(con, ("jane_smith",))
# delete_your_kahoot_by_id(con, 1)
# delete_quiz_with_written_answer(con, 1)
# delete_quiz_answer_with_written_answer(con, 1)
# delete_quiz_with_true_false(con, 3)
#=====================================================

# # Example calls for update functions
# #=====================================================
# update_quiz_with_true_false(con, 1, "Did the catholic church believe earth was center of universe in 16th century", True, 1)
# update_quiz_answer_with_written_answer(con, 1, 1, '6')
# update_quiz_question_with_written_answer(con, 1, 'What is 3 + 3', 1)
# update_your_kahoot_by(con, 1, 'The best kahoot', 'Best of the best', True, 1)
# update_groups(con, 3, 'Teknikhögskolan', 'AI nerds')
# update_presentation_classic(con, 3, 1, title='Welcome to the Tobias AI-quiz', text='Prepare to be amazed by AI-generated questions!')
# #=====================================================

# # Example calls for patch functions
# #=====================================================
# patch_question_quiz_with_true_false(con, 1, "Do most people believe the earth is flat?")
# #=====================================================


# TODO REMOVE THIS BEFORE SENDING IN
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
