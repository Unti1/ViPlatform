from sqlalchemy import ForeignKey
from settings.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sql_enums.base import GenderEnum, StatusEnum

class Group(Base):
    name: Mapped[str]
    
    dashboard: Mapped['Dashboard'] = relationship(
        'Dashboard',
        back_populates='group'
    )
    
    group_items: Mapped['GroupItem'] = relationship(
        'GroupItem',
        back_populates='group',
        cascade='all, delete-orphan',
    )




    