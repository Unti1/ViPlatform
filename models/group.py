from settings.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Group(Base):
    name: Mapped[str] = mapped_column(unique=True)

    dashboard: Mapped["Dashboard"] = relationship(
        "Dashboard", 
        back_populates="group"
        )

    group_items: Mapped["GroupItem"] = relationship(
        "GroupItem",
        back_populates="group",
        cascade="all, delete-orphan",
    )
    
    manuals: Mapped["Manual"]  = relationship(
        'Manual',
        back_populates='group',
    )
