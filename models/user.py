import bcrypt
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.profile import Profile
from settings.database import Base, connection, unique_str_an
from sql_enums.base import RoleEnum


class User(Base):
    username: Mapped[unique_str_an]
    email: Mapped[unique_str_an]
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.STUDENT, server_default=text("'STUDENT'"))

    # tokens: Mapped['UserToken'] = relationship(
    #     'UserToken',
    #     back_populates='user'
    # )
    
    # Связь one-to-one с profile
    profile: Mapped['Profile'] = relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        lazy='joined',
        cascade='all, delete-orphan'
    )
    
    dashboards: Mapped['Dashboard'] = relationship(
        'Dashboard',
        back_populates='user',
        lazy='joined',
        cascade='all, delete-orphan'
    )
    
    groupitem: Mapped['GroupItem'] = relationship(
        'GroupItem',
        back_populates='user',
        lazy='joined',
        cascade='all, delete-orphan'
    )
    
    quizzes: Mapped['Quiz'] = relationship(
        'Quiz',
        back_populates='user',
        cascade='all, delete-orphan'
    ) 
    

    
    @classmethod
    @connection
    async def create(
        cls,
        username: str,
        email: str,
        password: str,
        session: AsyncSession = None,
        **profile_data
    ) -> 'User':
        """Модель для создания пользователя.

        Args:
            username (str): Имя пользователя(уникальное)
            email (str): Email пользователя(уникальное)
            password (str): Пароль позователя
            **profile_data: Прочие данные профиля
        Returns:
            user.id: ID нового пользователя.
 
        """
        
        hash_pass = str(bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()))
        
        new_user: User = User(
            username=username, 
            email=email, 
            password=hash_pass 
            )
        
        session.add(new_user)
        await session.commit()
        
        new_profile = Profile(
            user_id=new_user.id,
            **profile_data
            )

        session.add(new_profile)
        await session.commit()
        
        return new_user

    @classmethod
    @connection
    async def get_by_username(cls, username: str, session: AsyncSession = None):
        rows = await session.execute(select(cls).where(cls.username == username))
        return rows.scalars().first()



    @classmethod
    @connection
    async def check(cls, username: str, password: str, session: AsyncSession = None):
        user: User = await cls.get_by_username(username)

        if not user:
            return False, "Неверное имя пользователя или пароль"
        elif not bcrypt.checkpw(password.encode(), user.password[2:-1].encode()):
            return False, "Неверное имя пользователя или пароль"

        return user, "Успех"
        

        