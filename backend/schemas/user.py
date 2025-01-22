from typing import Optional, Union
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str = Field(..., max_length=50)
    password: str
    email: str
    sex: bool = Field(..., description="True is women, false is men")
    age: int
    identity: int = Field(..., description="1 is student, 2 is teacher, 3 is manager")

class UserCreate(UserBase):
    pass


class User(UserBase):
    uid: str

"""
{
    "name": "teddy",
    "password": "12345678",
    "email": "teddy@example.com",
    "sex": 0,
    "age": 20,
    "identity": 1

}

"""