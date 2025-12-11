from datetime import date
from typing import Optional

from pydantic import BaseModel


# Pydantic Models for POST endpoints (CREATE)
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

class GroupMembershipCreate(BaseModel):
    user_id: int
    group_id: int

class WrittenQuizCreate(BaseModel):
    question: str
    your_kahoot_id: int

class QuizAnswerCreate(BaseModel):
    answer: str
    quiz_with_written_answer_id: int

class TrueFalseQuizCreate(BaseModel):
    question: str
    answer: bool
    your_kahoot_id: int

class PresentationClassicCreate(BaseModel):
    your_kahoot_id: int
    title: Optional[str] = None
    text: Optional[str] = None

# Pydantic Models for PUT endpoints (UPDATE)
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

# Pydantic Models for PATCH endpoints (PARTIAL UPDATE)
class QuizTrueFalseQuestionPatch(BaseModel):
    question: str

# Pydantic Models for DELETE endpoints
class Username(BaseModel):
    username: str