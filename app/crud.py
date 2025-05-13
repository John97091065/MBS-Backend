from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schema, auth
from datetime import timedelta, datetime
from .utils import hash_password, verify_password
from jose import jwt




def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

#CREATE USER FUNCTION
def create_user(db: Session, user: schema.UserCreate):
    """Create a new user in the database."""
    hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#TOKEN CREATION
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, auth.SECRET_KEY, algorithm=auth.ALGORITHM)


#LOGIN USER FUNCTION
def login_user(db: Session, user: schema.UserLogin):
    print(f"Attempting login for: {user.name}")
    db_user = get_user_by_name(db, name=user.name)
    if not db_user:
        print("User not found.")
        return None
    if not verify_password(user.password, db_user.password):
        print("Invalid password.")
        return None
    print("Login successful.")
    return db_user


#GET CURRENT ADMIN FUNCTION
def get_current_admin(db: Session, user: models.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin user")
    return db_user


#CREATE PRODUCTS FUNCTION
def create_product(db: Session, product: schema.ProductCreate, user: models.User):
    """Create a new product in the database."""
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        category=product.category,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#GET ALL PRODUCTS FUNCTION
def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    """Get all products from the database."""
    return db.query(models.Product).offset(skip).limit(limit).all()