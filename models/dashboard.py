from uuid import uuid4
from sqlalchemy import ForeignKey, select
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.database import Base, connection


class Dashboard(Base):
    dashboard_id: Mapped[str] = mapped_column(default=str(uuid4()))
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    # connected_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    data: Mapped[dict] = mapped_column(JSON, default={})

    group: Mapped["Group"] = relationship(
        "Group", back_populates="dashboard", lazy="joined"
    )

    user: Mapped["User"] = relationship("User", back_populates="dashboards")

    @classmethod
    @connection
    async def get(cls, dashboard_id: str, session: AsyncSession):
        query = select(cls).where(cls.dashboard_id == dashboard_id)
        rows = await session.execute(query)
        return rows.scalar_one_or_none()
