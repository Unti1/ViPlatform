
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models import quiz
from settings.database import Base


class QuizQuest(Base):
    """Модель для решенных студенческих работ"""
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizs.id'))
    grade: Mapped[float]

