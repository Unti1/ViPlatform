from sqlalchemy import ForeignKey, select, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from models.user import User
from settings.database import Base, connection


class Quiz(Base):
    """Модель тестов"""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    description: Mapped[str]
    timer: Mapped[int]  # seconds
    quiz_description: Mapped[dict] = mapped_column(JSON)
    quiz_answers: Mapped[dict] = mapped_column(JSON)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    max_attempts: Mapped[int] = mapped_column(default=1)
    min_pass_percentage: Mapped[float] = mapped_column(default=60.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="quizzes")

    @classmethod
    @connection
    async def get_per_user_id(cls, user_id, session: AsyncSession = None):
        rows = await session.execute(select(cls).where(cls.user_id == user_id))
        return rows.scalars().all() or []

    @classmethod
    @connection
    async def get(cls, id: int, session: AsyncSession = None):
        rows = await session.execute(select(cls).where(cls.id == id))
        return rows.scalar_one_or_none()

    @classmethod
    @connection
    async def create(
        cls,
        user_id: int,
        title: str,
        description: str,
        timer: int,
        quiz_description: dict,
        quiz_answers: dict,
        deadline: datetime = None,
        max_attempts: int = 1,
        min_pass_percentage: float = 60.0,
        session: AsyncSession = None
    ) -> 'Quiz':
        # Конвертируем deadline в naive datetime если он есть
        if deadline and deadline.tzinfo:
            deadline = deadline.replace(tzinfo=None)
        
        quiz = cls(
            user_id=user_id,
            title=title,
            description=description,
            timer=timer,
            quiz_description=quiz_description,
            quiz_answers=quiz_answers,
            deadline=deadline,
            max_attempts=max_attempts,
            min_pass_percentage=min_pass_percentage
        )
        session.add(quiz)
        await session.commit()
        return quiz
