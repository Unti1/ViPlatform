from profile import Profile
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from settings.config import Settings
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
        
        hash_pass = str(bcrypt.hashpw(password.encode('UTF-8'), Settings.SECRET_KEY.encode('UTF-8')))
        
        new_user: User = User(
            username=username, 
            email=email, 
            password=hash_pass 
            )
        
        session.add(new_user)
        
        new_profile = Profile(
            name=name, 
            surname=surname, 
            status=status, 
            gender=gender, 
            about=about, 
            user_id=new_user.id
            )

        session.add(new_profile)
        await session.commit()
        
        return new_user.id

