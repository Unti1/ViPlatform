from typing import List

from pydantic import BaseModel


class QuizCreate(BaseModel):
    user_id: int
    title: str
    description: str
    quiz_description: List[str]
    quiz_answers: List[str]