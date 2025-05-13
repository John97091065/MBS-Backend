from pydantic import BaseModel, EmailStr, Field

#USER CREATE
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    is_admin: bool = False  # default to False for regular users


#PRODUCT CREATE
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=255)
    price: int = Field(..., gt=0)  # price must be greater than 0
    image_url: str = Field(None, max_length=255)  # optional field for image URL
    category: str = Field(..., min_length=1, max_length=50)  # category field

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