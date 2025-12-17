import psycopg2
from fastapi import HTTPException
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor


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
        raise HTTPException(status_code=409, detail=f"Unable to insert the user. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to insert the user. Error message: {e}")

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
        raise HTTPException(status_code=409, detail=f"Unable to create favorite kahoot. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create favorite kahoot. Error message: {e}")

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
                if result is None:
                    raise HTTPException(status_code=400, detail="No user found with provided primary key id.")
                return result
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Unable to read the users data. Error message: {e}")

def read_questions_by_kahoot_id(con, kahoot_id):
    """
    Fetches True/False, Written Questions, and Slides for a specific Kahoot
    and combines them into a single list.
    """
    questions = []
    
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                
                # 1. Get True/False Questions
                cur.execute("""
                    SELECT id, question, 'True/False' as type, answer 
                    FROM quiz_with_true_false 
                    WHERE your_kahoot_id = %s
                """, (kahoot_id,))
                questions.extend(cur.fetchall())

                # 2. Get Written Questions (Stems)
                cur.execute("""
                    SELECT id, question, 'Written' as type 
                    FROM quiz_with_written_answer 
                    WHERE your_kahoot_id = %s
                """, (kahoot_id,))
                questions.extend(cur.fetchall())

                # 3. Get Slides (Presentation)
                cur.execute("""
                    SELECT id, title as question, 'Slide' as type, text 
                    FROM presentation_classic 
                    WHERE your_kahoot_id = %s
                """, (kahoot_id,))
                questions.extend(cur.fetchall())
                
                return questions

    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=f"Error fetching questions: {e}")

def delete_group_by_id(con, group_id):
    query = """
    DELETE FROM groups 
    WHERE id = %s
    RETURNING id, name;
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (group_id, ))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Group not found, no deletion could be made")
                return result
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete the group. Error message: {e}")

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

