from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.database import Base

class GroupItem(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    
    user: Mapped['User'] = relationship(
        'User'
    )
    
    group: Mapped['Group'] = relationship(
        'Group',
        back_populates='group_items'
    )