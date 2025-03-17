from sqlalchemy import ARRAY, ForeignKey, String, desc
from sqlalchemy.orm import Mapped, mapped_column
from settings.database import Base


class Quiz(Base):
    """Модель тестов"""
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]
    description: Mapped[str]
    quiz_description: Mapped[list[str]] = mapped_column(ARRAY(String))
    quiz_answers: Mapped[list[str]] = mapped_column(ARRAY(String))

