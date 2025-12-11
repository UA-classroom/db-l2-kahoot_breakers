import os

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import (
    create_subscriptions,
    delete_quiz_answer_with_written_answer,
    delete_quiz_question_with_written_answer,
    delete_quiz_with_true_false,
    delete_user_by_username,
    delete_your_kahoot_by_id,
    patch_question_quiz_with_true_false,
    update_groups,
    update_presentation_classic,
    update_quiz_answer_with_written_answer,
    update_quiz_question_with_written_answer,
    update_quiz_with_true_false,
    update_your_kahoot_by,
)
from db_setup import get_connection

app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""

class SubscriptionCreate(BaseModel):
    name: str

class QuizAnswerWrittenUpdate(BaseModel):
    answer: str
    quiz_with_written_answer_id: int

class QuizQuestionWrittenUpdate(BaseModel):
    question: str
    your_kahoot_id: int

class YourKahootUpdate(BaseModel):
    title: str
    description: str | None = None
    is_private: bool
    language_id: int

class GroupUpdate(BaseModel):
    name: str
    description: str | None = None

class QuizTrueFalseUpdate(BaseModel):
    question: str
    answer: bool
    your_kahoot_id: int

class PresentationClassicUpdate(BaseModel):
    your_kahoot_id: int
    title: str | None = None
    text: str | None = None

class QuizTrueFalseQuestionPatch(BaseModel):
    question: str

@app.post("/subscriptions")
def create_subscription_endpoint(subscription: SubscriptionCreate):
    connection = get_connection()

    try:
        out_data = create_subscriptions(connection, subscription.name)
        return out_data
    except:
        pass
    finally:
        connection.close()


class Username(BaseModel):
    username: str

@app.delete("/users/{username}")
def delete_user_endpoint(username: str):
    connection = get_connection()

    try:
        result = delete_user_by_username(connection, username)
        return {
            "message": f"User '{username}' deleted successfully",
            "deleted_user": result,
        }
    except HTTPException:
        raise
    finally:
        connection.close()

# AI suggestion: So for your DELETE endpoints that only take an {id} in the URL, 
# skip Pydantic models and keep just the typed path parameter

@app.delete("/your_kahoot/{your_kahoot_id}")
def delete_your_kahoot_endpoint(your_kahoot_id: int):
    connection = get_connection()

    try:
        result = delete_your_kahoot_by_id(connection, your_kahoot_id)
        return {
            "message": f"Kahoot id '{your_kahoot_id}' deleted successfully",
            "deleted_kahoot": result,
        }
    except HTTPException:
        raise
    finally:
        connection.close()

@app.delete("/quiz_question_with_written_answer/{quiz_with_written_answer_id}")
def delete_quiz_question_with_written_answer_endpoint(quiz_with_written_answer_id: int):
    connection = get_connection()

    try:
        result = delete_quiz_question_with_written_answer(connection, quiz_with_written_answer_id)
        return {
            "message": f"Quiz question with written answer id '{quiz_with_written_answer_id}' deleted successfully",
            "deleted_quiz_question": result,
    }
    except HTTPException:
        raise
    finally:
        connection.close()

@app.delete("/quiz_answer_with_written_answer/{quiz_written_answer_id}")
def delete_quiz_answer_with_written_answer_endpoint(quiz_written_answer_id: int):
    connection = get_connection()

    try:
        result = delete_quiz_answer_with_written_answer(connection, quiz_written_answer_id)
        return {
            "message": f"Quiz answer with written answer id '{quiz_written_answer_id}' deleted successfully",
            "deleted_quiz_answer": result,
    }
    except HTTPException:
        raise
    finally:
        connection.close()

@app.delete("/delete_quiz_with_true_false/{quiz_with_true_false_id}")
def delete_quiz_with_true_false_endpoint(quiz_with_true_false_id: int):
    connection = get_connection()

    try:
        result = delete_quiz_with_true_false(connection, quiz_with_true_false_id)
        return {
            "message": f"Quiz question/answer with written answer id '{quiz_with_true_false_id}' deleted successfully",
            "deleted_quiz_question/answer": result,
    }
    except HTTPException:
        raise
    finally:
        connection.close()



@app.put("/quiz_true_false/{id}")
def put_quiz_true_false(id: int, quiz: QuizTrueFalseUpdate):
    con = get_connection()

    try:
        result = update_quiz_with_true_false(
            con,
            id=id,
            question=quiz.question,
            answer=quiz.answer,
            your_kahoot_id=quiz.your_kahoot_id,
        )
        return {
            "message": f"Quiz true/false id '{id}' updated successfully",
            "updated_quiz": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.put("/quiz_answer_with_written_answer/{id}")
def put_quiz_answer_with_written_answer(id: int, body: QuizAnswerWrittenUpdate):
    con = get_connection()
    try:
        result = update_quiz_answer_with_written_answer(
            con,
            id=id,
            quiz_with_written_answer_id=body.quiz_with_written_answer_id,
            answer=body.answer,
        )
        return {
            "message": f"Quiz written answer id '{id}' updated successfully",
            "updated_answer": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.put("/quiz_question_with_written_answer/{id}")
def put_quiz_question_with_written_answer(id: int, body: QuizQuestionWrittenUpdate):
    con = get_connection()
    try:
        result = update_quiz_question_with_written_answer(
            con,
            id=id,
            question=body.question,
            your_kahoot_id=body.your_kahoot_id,
        )
        return {
            "message": f"Quiz question with written answer id '{id}' updated successfully",
            "updated_question": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.put("/your_kahoot/{your_kahoot_id}")
def put_your_kahoot(your_kahoot_id: int, body: YourKahootUpdate):
    con = get_connection()
    try:
        result = update_your_kahoot_by(
            con,
            your_kahoot_id=your_kahoot_id,
            title=body.title,
            description=body.description,
            is_private=body.is_private,
            language_id=body.language_id,
        )
        return {
            "message": f"Kahoot id '{your_kahoot_id}' updated successfully",
            "updated_kahoot": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.put("/groups/{id}")
def put_group(id: int, body: GroupUpdate):
    con = get_connection()
    try:
        result = update_groups(
            con,
            id=id,
            name=body.name,
            description=body.description,
        )
        return {
            "message": f"Group id '{id}' updated successfully",
            "updated_group": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.put("/presentation_classic/{id}")
def put_presentation_classic(id: int, body: PresentationClassicUpdate):
    con = get_connection()
    try:
        result = update_presentation_classic(
            con,
            id=id,
            your_kahoot_id=body.your_kahoot_id,
            title=body.title,
            text=body.text,
        )
        return {
            "message": f"Presentation classic id '{id}' updated successfully",
            "updated_presentation": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

@app.patch("/quiz_true_false/{id}")
def patch_quiz_true_false_question(id: int, body: QuizTrueFalseQuestionPatch):
    con = get_connection()
    try:
        result = patch_question_quiz_with_true_false(
            con,
            id=id,
            question=body.question,
        )
        return {
            "message": f"Quiz true/false id '{id}' question updated successfully",
            "updated_quiz": result,
        }
    except HTTPException:
        raise
    finally:
        con.close()

# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}


# IMPLEMENT THE ACTUAL ENDPOINTS! Feel free to remove
