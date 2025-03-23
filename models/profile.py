from sqlalchemy import ForeignKey
from settings.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sql_enums.base import GenderEnum, StatusEnum

class Profile(Base):
    surname: Mapped[str|None]
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.DEMO, server_default="'DEMO'")
    about: Mapped[str|None]
    age: Mapped[str|None]
    group: Mapped[str|None]
    gender: Mapped[GenderEnum] = mapped_column(default=GenderEnum.UNDEFINE, server_default="'UNDEFINE'")
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    # Обратная связь one-to-one к табл. "users"
    user: Mapped['User'] = relationship(
        'User',
        back_populates='profile',
        uselist=False,
        )
    