

from sqlalchemy.orm import Mapped
from settings.database import Base


class Group(Base):
    name: Mapped[str]
    