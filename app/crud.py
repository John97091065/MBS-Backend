from sqlalchemy.orm import Session
from . import models, schema
from .utils import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def hash_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return hash_password(plain_password) == hashed_password

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

# def get_current_admin(db: Session, user: models.User):
#     """Get the current admin user."""
#     db_user = db.query(models.User).filter(models.User.id == user.id).first()
#     if not db_user or not db_user.is_admin:
#         raise HTTPException(status_code=403, detail="Not an admin user")
#     return db_user
