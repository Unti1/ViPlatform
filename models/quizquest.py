
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column
from settings.database import Base


class QuizQuest(Base):
    """Модель для решенных студенческих работ"""
    manual_id: Mapped[int] = mapped_column(ForeignKey('manuals.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizs.id'))
    time_below: Mapped[int]
    answers: Mapped[dict] = mapped_column(JSON)
    grade: Mapped[float]

