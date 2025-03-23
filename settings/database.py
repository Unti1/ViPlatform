from datetime import datetime
from typing import Annotated
from sqlalchemy import Integer, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs, async_sessionmaker
from settings.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# connection decorator for db method
# декоратор для методов которые работают с бд
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


class Base(AsyncAttrs, DeclarativeBase):
    """
    Основной класс-шаблон для всех моделей БД
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
    
    @classmethod
    @connection
    async def get_per_id(
        cls,
        id: int,
        session: AsyncSession = None
        ) -> 'Base':
        """Выдает пользователя по id.
        Примечание: т.к. описан в главном родительском классе то метод есть во всех зависимых моделях(ТО ЕСТЬ ВО ВСЕХ) 

        Args:
            id (int): id необходимой ячейки данных
            session (AsyncSession, optional): аргумент для вставки сессии для работы с базой данных. Больше описанию не подллежит. 
            Есть во всех зависимых методах с запросом в бд, идет "в комплекте" с декором "connection"

        Raises:
            e: Если ошибка то откат действий над бд

        Returns:
            Base | None: возвращает  модель к которой происходит обращение или None если не найден
  
        """
        
        rows = await session.execute(select(cls).where(cls.id == id))
        return rows.scalars().first()
    
    @classmethod
    @connection
    async def update(
        cls,
        id: int,
        session: AsyncSession = None,
        **updateting_data 
        ) -> 'Base':
        """Обновление любого атрибута наследуемой от Base
        Args:
            id (int): id строки данных которая требует обновления
            **updateting_data (dict): данные которые нужно обновить в формате `атрибут = значение`

        Returns:
            Base: _description_
        """
        
        modified = False
        rows = await session.execute(select(cls).where(cls.id == id))
        concrete_row = rows.scalars().first()
        if not concrete_row:
            return None, 'Not found'
        
        for key, value in updateting_data.items():
            if getattr(concrete_row, key) and (getattr(concrete_row, key) != value):
                setattr(concrete_row, key, value)
                modified = True

        if modified:
            # само обновление данных
            await session.commit()

        return concrete_row, 'Success'
                
    
# Тут блок для повторяющихся аннотаций
unique_str_an = Annotated[str, mapped_column(unique=True)]
