import os
from datetime import date
from typing import Optional

import psycopg2
from db import (
    create_customer_types,
    create_favorite_kahoots,
    create_groups,
    create_kahoot_owners,
    create_languages,
    create_subscriptions,
    create_users,
    create_your_kahoot,
)
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
class LanguageCreate(BaseModel):
    name: str
class CustomerTypeCreate(BaseModel):
    name: str
class UsersCreate(BaseModel):
    username: str
    email: str
    password: str
    birthdate: date
    subscriptions_id: int
    language_id: int
    customer_type_id: int
    name: Optional[str] = None
    organisation: Optional[str] = None
class YourKahootCreate(BaseModel):
    title: str
    language_id: int
    description: Optional[str] = None
    is_private: bool = False
class KahootOwnerCreate(BaseModel):
    users_id: int
    your_kahoot_id: int
class FavoriteKahootCreate(BaseModel):
    users_id: int
    your_kahoot_id: int
class GroupCreate(BaseModel):
    name: str
    description: str | None = None

    

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

@app.post("/language")
def create_language_endpoint(language: LanguageCreate):
    connection = get_connection()
    try:
        out_data = create_languages(connection, language.name)
        return out_data
    except:
        pass
    finally:
        connection.close()

@app.post("/customer_type")
def create_customer_types_endpoint(customer_type: CustomerTypeCreate):
    connection = get_connection()
    try:
        out_data = create_customer_types(connection, customer_type.name)
        return out_data
    except:
        pass
    finally:
        connection.close()

@app.post("/user")
def create_users_endpoint(user: UsersCreate):
    connection = get_connection()
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
    except:
        pass
    finally:
        connection.close()

@app.post("/your_kahoot")
def create_your_kahoot_endpoint(kahoot: YourKahootCreate):
    connection = get_connection()
    try:
        out_data = create_your_kahoot(connection,
                                    title=kahoot.title,
                                    language_id=kahoot.language_id,
                                    description=kahoot.description,
                                    is_private=kahoot.is_private
        )
        return out_data
    except:
        pass
    finally:
        connection.close()

@app.post("/kahoot_owner")
def create_kahoot_owners_endpoint(kahoot_owner: KahootOwnerCreate):
    connection = get_connection()
    try:
        out_data = create_kahoot_owners(connection,
                                        users_id=kahoot_owner.users_id,
                                        your_kahoot_id=kahoot_owner.your_kahoot_id
        )
        return out_data
    except:
        pass
    finally:
        connection.close()

@app.post("/favorite_kahoot")
def create_favorite_kahoot_endpoint(favorite: FavoriteKahootCreate):
    connection = get_connection()
    try:
        out_data = create_favorite_kahoots(connection,
                                        users_id=favorite.users_id,
                                        your_kahoot_id=favorite.your_kahoot_id
        )
        return out_data
    except:
        pass
    finally:
        connection.close()

@app.post("/group")
def create_groups_endpoint(group: GroupCreate):
    connection = get_connection()
    try:
        out_data = create_groups(connection,
                                name=group.name,
                                description=group.description
        )
        return out_data
    except:
        pass
    finally:
        connection.close()








#~/desktop/project/db-l2-kahoot_breakers 

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
