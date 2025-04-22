
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings.database import Base


# class UserToken(Base):
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     token: Mapped[str]
    
#     user: Mapped['User'] = relationship(
#         'User',
#         back_populates='tokens'
#     )

