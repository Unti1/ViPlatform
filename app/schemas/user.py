


# Pydantic модель для валидации данных формы
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v