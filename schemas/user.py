


# Pydantic модель для валидации данных формы
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator



class UserSignIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    
    model_config = ConfigDict(from_attributes=True)
    
class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('confirm_password')
    async def passwords_match(cls, value, values, **kwargs):
        print(value, values)
        return value
    
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
