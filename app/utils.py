from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")

def hash_password(password: str):
    """Hash a password using pbkdf2_sha512 algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)