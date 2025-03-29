from sqlalchemy import ForeignKey
from settings.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sql_enums.base import GenderEnum, StatusEnum

class Profile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str|None]
    surname: Mapped[str|None]
    about: Mapped[str|None]
    age: Mapped[str|None]
    group: Mapped[str|None]
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.DEMO, server_default="'DEMO'")
    gender: Mapped[GenderEnum] = mapped_column(default=GenderEnum.UNDEFINE, server_default="'UNDEFINE'")
    
    # Обратная связь one-to-one к табл. "users"
    user: Mapped['User'] = relationship(
        'User',
        back_populates='profile',
        uselist=False,
        )
    