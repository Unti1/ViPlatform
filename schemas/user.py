


# Pydantic модель для валидации данных формы
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from sql_enums.base import GenderEnum



class UserSignIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    
    model_config = ConfigDict(from_attributes=True)
    
class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str|None
    surname: str|None
    age: str|None
    gender: GenderEnum
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
