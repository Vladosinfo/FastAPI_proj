from pydantic import BaseModel, Field, EmailStr, AllowInfNan
from datetime import date
from typing import Optional


class ContactResponse(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    phone: str = Field(max_length=20)
    birthday: date = Field()
    additional: str|None = Field(default=None)
    
    class Config:
        orm_mode = True
