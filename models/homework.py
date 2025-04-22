

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from settings.database import Base


class Homework(Base):
    user_id = mapped_column(ForeignKey('users.id'))
    quiz_id = mapped_column(ForeignKey(''))
    
    user = relationship(
        'User',
        back_populates='homework'
    )