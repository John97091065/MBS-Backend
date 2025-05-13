from pydantic import BaseModel, EmailStr, Field

#USER CREATE
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    is_admin: bool = False  # default to False for regular users

#ADMIN CREATE
class AdminCreate(UserCreate):
    is_admin: bool = True  # force admin flag

#LOGIN
class UserLogin(BaseModel):
    name: str
    password: str

#TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True