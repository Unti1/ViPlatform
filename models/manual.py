
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.database import Base


class Manual(Base):
    """
    Модель Методических материалов
    """
    
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    title: Mapped[str]
    description: Mapped[str]
    filepath: Mapped[str]
    
    group = relationship(
        'Group',
        back_populates='manuals',
    )
    
    