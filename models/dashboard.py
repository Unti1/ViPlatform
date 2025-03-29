

from uuid import uuid4
from sqlalchemy import ForeignKey, Integer, select
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, query, relationship
from settings.database import Base, array_or_none_an, connection


class Dashboard(Base):
    dashboard_id: Mapped[str] = mapped_column(default=str(uuid4()))
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    # connected_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    data: Mapped[dict] = mapped_column(JSON)
    
    group: Mapped['Group'] = relationship(
        'Group',
        back_populates='dashboard',
        lazy='joined'
    )
    
    user: Mapped['User'] = relationship(
        "User", 
        back_populates="dashboards"
        )
    
    @classmethod
    @connection
    async def add(cls, session: AsyncSession = None, **kwargs):
        dashboard = Dashboard(title="New Dashboard")
        session.add(dashboard)
        await session.commit()
        return dashboard
