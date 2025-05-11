from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    is_admin: bool = False  # default to False for regular users


class AdminCreate(UserCreate):
    is_admin: bool = True  # force admin flag


class UserLogin(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True