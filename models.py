from typing import Literal
from pydantic import BaseModel, Field, field_validator


def _clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=12000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        return _clean_text(value)


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=12000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class QuizRequest(TextRequest):
    pass


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=500)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return _clean_text(value)


class QAResponse(BaseModel):
    answer: str


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(..., min_length=1, max_length=3)


class LearningPathResponse(BaseModel):
    result: str


class ErrorResponse(BaseModel):
    detail: str
