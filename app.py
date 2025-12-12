import psycopg2
from fastapi import Depends, FastAPI, HTTPException

import schemas as s
from db import (
    create_answer_quiz,
    create_customer_types,
    create_favorite_kahoots,
    create_groups,
    create_kahoot_owners,
    create_languages,
    create_presentation_classic,
    create_subscriptions,
    create_true_false_quiz,
    create_user_group_members,
    create_users,
    create_written_quiz,
    create_your_kahoot,
    delete_quiz_answer_with_written_answer,
    delete_quiz_question_with_written_answer,
    delete_quiz_with_true_false,
    delete_user_by_username,
    delete_your_kahoot_by_id,
    patch_question_quiz_with_true_false,
    read_all_groups,
    read_all_kahoots,
    read_all_users,
    read_individual_user,
    read_users_favorite_kahoot,
    read_users_groups,
    read_users_joined_kahoot,
    update_groups,
    update_presentation_classic,
    update_quiz_answer_with_written_answer,
    update_quiz_question_with_written_answer,
    update_quiz_with_true_false,
    update_your_kahoot_by,
)
from db_setup import get_connection, release_connection

app = FastAPI()


# Dependency function to manage database connection lifecycle
def get_db_connection():
    """
    FastAPI dependency that provides a database connection and ensures proper cleanup.
    The connection is automatically returned to the pool after the request completes.
    https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#sub-dependencies-with-yield
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        release_connection(conn)

# ==================== POST ENDPOINTS (CREATE) ====================

@app.post("/subscriptions")
def create_subscription_endpoint(
    subscription: s.SubscriptionCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_subscriptions(connection, subscription.name)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to save the subscription name. Error message: {e}")

@app.post("/language")
def create_language_endpoint(
    language: s.LanguageCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_languages(connection, language.name)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to save the language name. Error message: {e}")

@app.post("/customer_type")
def create_customer_types_endpoint(
    customer_type: s.CustomerTypeCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_customer_types(connection, customer_type.name)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to save the customer type name. Error message: {e}")

@app.post("/user")
def create_users_endpoint(
    user: s.UsersCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_users(connection,
                                username=user.username,
                                email=user.email,
                                password=user.password,
                                birthdate=user.birthdate,
                                subscriptions_id=user.subscriptions_id,
                                language_id=user.language_id,
                                customer_type_id=user.customer_type_id,
                                name=user.name,
                                organisation=user.organisation
        )
        return out_data
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=409, detail=f"Unable to save the user, userdata already exists violating unique constraints. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to save the user, violating foreign key constraints. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to save the user. Error message: {e}")

@app.post("/your_kahoot")
def create_your_kahoot_endpoint(
    kahoot: s.YourKahootCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_your_kahoot(connection,
                                    title=kahoot.title,
                                    language_id=kahoot.language_id,
                                    description=kahoot.description,
                                    is_private=kahoot.is_private
        )
        return out_data
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to save the kahoot because of foreign key violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to save the kahoot. Error message: {e}")

@app.post("/kahoot_owner")
def create_kahoot_owners_endpoint(
    kahoot_owner: s.KahootOwnerCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_kahoot_owners(connection,
                                        users_id=kahoot_owner.users_id,
                                        your_kahoot_id=kahoot_owner.your_kahoot_id
        )
        return out_data
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=409, detail=f"Unable to create the kahoot ownership because it already exists. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the kahoot ownership. Foreign key violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the kahoot ownership. Error message: {e}")

@app.post("/favorite_kahoot")
def create_favorite_kahoot_endpoint(
    favorite: s.FavoriteKahootCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_favorite_kahoots(connection,
                                        users_id=favorite.users_id,
                                        your_kahoot_id=favorite.your_kahoot_id
        )
        return out_data
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=409, detail=f"Unable to create favorite kahoot because it already exists as favorite. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create favorite kahoot. Foreign key violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create favorite kahoot. Error message: {e}")

@app.post("/group")
def create_groups_endpoint(
    group: s.GroupCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_groups(connection,
                                name=group.name,
                                description=group.description
        )
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group. Error message: {e}")

@app.post("/group_membership")
def create_group_membership_endpoint(
    membership: s.GroupMembershipCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_user_group_members(connection,
                                user_id=membership.user_id,
                                group_id=membership.group_id
        )
        return out_data
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=409, detail=f"Unable to create the group membership because it already exists. Error message: {e}")
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the group membership. Foreign key constraint violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the group membership. Error message: {e}")

@app.post("/written_quiz")
def create_written_quiz_endpoint(
    quiz: s.WrittenQuizCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_written_quiz(connection,
                                    question=quiz.question,
                                    your_kahoot_id=quiz.your_kahoot_id
        )
        return out_data
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the quiz. Foreign key constraint violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")

@app.post("/quiz_answer")
def create_answer_quiz_endpoint(
    quiz_answer: s.QuizAnswerCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_answer_quiz(connection,
                                    answer=quiz_answer.answer,
                                    quiz_with_written_answer_id=quiz_answer.quiz_with_written_answer_id
        )
        return out_data
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the quiz answer. Foreign key constraint violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz answer. Error message: {e}")

@app.post("/true_false_quiz")
def create_true_false_quiz_endpoint(
    quiz: s.TrueFalseQuizCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_true_false_quiz(connection,
                                        question=quiz.question,
                                        answer=quiz.answer,
                                        your_kahoot_id=quiz.your_kahoot_id
        )
        return out_data
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the quiz. Foreign key constraint violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the quiz. Error message: {e}")

@app.post("/classic_presentation")
def create_classic_presentation_endpoint(
    presentation: s.PresentationClassicCreate,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = create_presentation_classic(connection,
                                            your_kahoot_id=presentation.your_kahoot_id,
                                            title=presentation.title,
                                            text=presentation.text
        )
        return out_data
    except psycopg2.errors.ForeignKeyViolation as e:
        raise HTTPException(status_code=404, detail=f"Unable to create the presention. Foreign key constraint violation. Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to create the presenation. Error message: {e}")

# ==================== GET ENDPOINTS (READ) ====================

@app.get("/all_users")
def read_all_users_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_all_users(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get all user information. Error message: {e}")

@app.get("/all_kahoots")
def read_all_kahoots_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_all_kahoots(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get information of all kahoots. Error message: {e}")

@app.get("/all_groups")
def read_all_groups_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_all_groups(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get information of all groups. Error message: {e}")

@app.get("/users_kahoot")
def read_users_kahoot_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_users_joined_kahoot(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get information of all users and their kahoots. Error message: {e}")

@app.get("/users_favorite")
def read_users_favorite_kahoot_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_users_favorite_kahoot(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get information of all users and their favorite kahoots. Error message: {e}")

@app.get("/users_group")
def read_users_groups_endpoint(
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_users_groups(connection)
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get information of all users and their groups. Error message: {e}")

@app.get("/user/{user_id}")
def read_individual_user_endpoint(
    user_id: int,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        out_data = read_individual_user(connection, user_id)
        if out_data is None:
            raise HTTPException(status_code=404, detail="No user found with provided primary key id.")
        return out_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to provide information of the user. Error message: {e}")

# ==================== DELETE ENDPOINTS ====================

@app.delete("/users/{username}")
def delete_user_endpoint(
    username: str,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = delete_user_by_username(connection, username)
        return {
            "message": f"User '{username}' deleted successfully",
            "deleted_user": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# If DELETE endpoints that only take an {id} "int" in the URL, 
# The we should be able to skip Pydantic models and keep just the typed path parameter

@app.delete("/your_kahoot/{your_kahoot_id}")
def delete_your_kahoot_endpoint(
    your_kahoot_id: int,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = delete_your_kahoot_by_id(connection, your_kahoot_id)
        return {
            "message": f"Kahoot id '{your_kahoot_id}' deleted successfully",
            "deleted_kahoot": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

@app.delete("/quiz_question_with_written_answer/{quiz_with_written_answer_id}")
def delete_quiz_question_with_written_answer_endpoint(
    quiz_with_written_answer_id: int,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = delete_quiz_question_with_written_answer(connection, quiz_with_written_answer_id)
        return {
            "message": f"Quiz question with written answer id '{quiz_with_written_answer_id}' deleted successfully",
            "deleted_quiz_question": result,
    }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

@app.delete("/quiz_answer_with_written_answer/{quiz_written_answer_id}")
def delete_quiz_answer_with_written_answer_endpoint(
    quiz_written_answer_id: int,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = delete_quiz_answer_with_written_answer(connection, quiz_written_answer_id)
        return {
            "message": f"Quiz answer with written answer id '{quiz_written_answer_id}' deleted successfully",
            "deleted_quiz_answer": result,
    }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

@app.delete("/quiz_true_false/{quiz_with_true_false_id}")
def delete_quiz_with_true_false_endpoint(
    quiz_with_true_false_id: int,
    connection: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = delete_quiz_with_true_false(connection, quiz_with_true_false_id)
        return {
            "message": f"Quiz question/answer with written answer id '{quiz_with_true_false_id}' deleted successfully",
            "deleted_quiz_question/answer": result,
    }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# ==================== PUT ENDPOINTS (UPDATE) ====================

@app.put("/quiz_true_false/{id}")
def put_quiz_true_false(
    id: int,
    quiz: s.QuizTrueFalseUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_quiz_with_true_false(con, id=id, question=quiz.question, answer=quiz.answer,your_kahoot_id=quiz.your_kahoot_id,)
        return {
            "message": f"Quiz true/false id '{id}' updated successfully",
            "updated_quiz": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.put("/quiz_answer_with_written_answer/{id}")
def put_quiz_answer_with_written_answer(
    id: int,
    body: s.QuizAnswerWrittenUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_quiz_answer_with_written_answer(con, id=id, quiz_with_written_answer_id=body.quiz_with_written_answer_id,answer=body.answer,)
        return {
            "message": f"Quiz written answer id '{id}' updated successfully",
            "updated_answer": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.put("/quiz_question_with_written_answer/{id}")
def put_quiz_question_with_written_answer(
    id: int,
    body: s.QuizQuestionWrittenUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_quiz_question_with_written_answer(con, id=id, question=body.question, your_kahoot_id=body.your_kahoot_id,)
        return {
            "message": f"Quiz question with written answer id '{id}' updated successfully",
            "updated_question": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.put("/your_kahoot/{your_kahoot_id}")
def put_your_kahoot(
    your_kahoot_id: int,
    body: s.YourKahootUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_your_kahoot_by(con, your_kahoot_id=your_kahoot_id, title=body.title, description=body.description, is_private=body.is_private, language_id=body.language_id,)
        return {
            "message": f"Kahoot id '{your_kahoot_id}' updated successfully",
            "updated_kahoot": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.put("/groups/{id}")
def put_group(
    id: int,
    body: s.GroupUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_groups(con, id=id, name=body.name, description=body.description,)
        return {
            "message": f"Group id '{id}' updated successfully",
            "updated_group": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.put("/presentation_classic/{id}")
def put_presentation_classic(
    id: int,
    body: s.PresentationClassicUpdate,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = update_presentation_classic(con, id=id,your_kahoot_id=body.your_kahoot_id,title=body.title,text=body.text,)
        return {
            "message": f"Presentation classic id '{id}' updated successfully",
            "updated_presentation": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

# ==================== PATCH ENDPOINTS (PARTIAL UPDATE) ====================

@app.patch("/quiz_true_false/{id}")
def patch_quiz_true_false_question(
    id: int,
    body: s.QuizTrueFalseQuestionPatch,
    con: psycopg2.extensions.connection = Depends(get_db_connection)
):
    try:
        result = patch_question_quiz_with_true_false(con, id=id, question=body.question,)
        return {
            "message": f"Quiz true/false id '{id}' question updated successfully",
            "updated_quiz": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")
