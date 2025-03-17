from sqlalchemy import String
from settings.database import Base, unique_str_an
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sql_enums.base import GenderEnum, StatusEnum

class User(Base):
    username: Mapped[unique_str_an]
    email: Mapped[unique_str_an]
    password: Mapped[str]

    # Связь one-to-one с profile
    profile: Mapped['Profile'] = relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        lazy='joined',
        cascade='all, delete-orphan'
    )