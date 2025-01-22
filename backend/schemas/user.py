from typing import Optional
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

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = None
    email: Optional[str] = None
    sex: Optional[bool] = Field(None, description="True is women, false is men")
    age: Optional[int] = None
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