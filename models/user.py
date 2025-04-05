import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.profile import Profile
from settings.config import settings
from settings.database import Base, connection, unique_str_an
from sqlalchemy.orm import Mapped, relationship
from sql_enums.base import GenderEnum, StatusEnum

class User(Base):
    username: Mapped[unique_str_an]
    email: Mapped[unique_str_an]
    password: Mapped[str]

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
        name: str | None = '',
        surname: str | None = '',
        status: StatusEnum = StatusEnum.DEMO,
        gender: GenderEnum = GenderEnum.UNDEFINE,
        about: str | None = '',
        session: AsyncSession = None,
    ) -> 'User':
        """Модель для создания пользователя.

        Args:
            username (str): Имя пользователя(уникальное)
            email (str): Email пользователя(уникальное)
            password (str): Пароль позователя
            name (str | None, optional):  Имя пользователя на сайте. Опционально.
            surname (str | None, optional): Фамилия пользователя на сайте. Опциально.
            status (StatusEnum, optional): статус пользователя. В дальнейшем можно для подписки реализовать. Опционально.
            gender (GenderEnum, optional): Пол. По умочанию - UNDEFINE. Опционально.
            about (str | None, optional): Описание пользователя. Типо графы "о себе. Опционально
            session (AsyncSession, optional): аргумент под объект рабочей сессии.
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
            name=name,
            surname=surname, 
            status=status, 
            gender=gender, 
            about=about
            )

        session.add(new_profile)
        await session.commit()
        
        return new_user

    @classmethod
    @connection
    async def get_by_username(cls, username: str, session: AsyncSession = None):
        rows = await session.execute(select(cls).where(cls.username == username))
        return rows.scalar_one_or_none()



    @classmethod
    @connection
    async def check(cls, username: str, password: str, session: AsyncSession = None):
        user: User = cls.get_by_username(username)
        if not user:
            return False, "Неверное имя пользователя или пароль"
        
        elif not bcrypt.checkpw(password.encode(), user.password):
            return False, "Неверное имя пользователя или пароль"

        return True, "Пользователь успешно вошел"
        

        