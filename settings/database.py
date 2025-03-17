from datetime import datetime
from typing import Annotated
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from settings.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

unique_str_an = Annotated[str, mapped_column(unique=True)]

# connection decorator for db method

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session = session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper
