from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Pydantic Models for POST endpoints (CREATE)
class SubscriptionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)

class LanguageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

class CustomerTypeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)

class UsersCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=1, max_length=255)
    birthdate: date
    subscriptions_id: int
    language_id: int
    customer_type_id: int
    name: Optional[str] = Field(None, max_length=255)
    organisation: Optional[str] = Field(None, max_length=50)

class YourKahootCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    language_id: int
    description: Optional[str] = Field(None, max_length=500)
    is_private: bool = False

class KahootOwnerCreate(BaseModel):
    users_id: int = Field(..., gt=0) # must be over 0 and positive integers
    your_kahoot_id: int = Field(..., gt=0) # must be over 0 and positive integers

class FavoriteKahootCreate(BaseModel):
    users_id: int = Field(..., gt=0)
    your_kahoot_id: int = Field(..., gt=0)

class GroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class GroupMembershipCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    group_id: int = Field(..., gt=0)

class WrittenQuizCreate(BaseModel):
    question: str = Field(..., min_length=1, max_length=100)
    your_kahoot_id: int = Field(..., gt=0)

class QuizAnswerCreate(BaseModel):
    answer: str = Field(..., min_length=1, max_length=100)
    quiz_with_written_answer_id: int = Field(..., gt=0)

class TrueFalseQuizCreate(BaseModel):
    question: str = Field(..., min_length=1, max_length=100)
    answer: bool
    your_kahoot_id: int = Field(..., gt=0)

class PresentationClassicCreate(BaseModel):
    your_kahoot_id: int = Field(..., gt=0)
    title: Optional[str] = Field(None, max_length=100)
    text: Optional[str] = Field(None, max_length=500)

# Pydantic Models for PUT endpoints (UPDATE)
class QuizAnswerWrittenUpdate(BaseModel):
    answer: str = Field(..., min_length=1, max_length=100)
    quiz_with_written_answer_id: int

class QuizQuestionWrittenUpdate(BaseModel):
    question: str = Field(..., min_length=1, max_length=100)
    your_kahoot_id: int

class YourKahootUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    description: Optional[str] = Field(None, max_length=500)
    is_private: bool
    language_id: int 

class GroupUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)  

class QuizTrueFalseUpdate(BaseModel):
    question: str = Field(..., min_length=1, max_length=100)
    answer: bool
    your_kahoot_id: int

class PresentationClassicUpdate(BaseModel):
    your_kahoot_id: int
    title: Optional[str] = Field(None, max_length=100)
    text: Optional[str] = Field(None, max_length=500)

# Pydantic Models for PATCH endpoints (PARTIAL UPDATE)
class QuizTrueFalseQuestionPatch(BaseModel):
    question: str = Field(..., min_length=1, max_length=100)

# Pydantic Models for DELETE endpoints
class Username(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
