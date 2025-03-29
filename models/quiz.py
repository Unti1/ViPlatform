from sqlalchemy import ARRAY, ForeignKey, String, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from settings.database import Base, connection


class Quiz(Base):
    """Модель тестов"""
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]
    description: Mapped[str]
    quiz_description: Mapped[list[str]] = mapped_column(ARRAY(String))
    quiz_answers: Mapped[list[str]] = mapped_column(ARRAY(String))
    
    user: Mapped['User'] = relationship(
        'User',
        back_populates='quizzes'
    )
    
    @classmethod
    @connection
    async def get_per_user_id(cls, user_id, session: AsyncSession=None):
        rows = await session.execute(select(cls).where(cls.user_id == user_id))
        return rows.scalars().all()


