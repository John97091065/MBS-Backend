from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schema, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#CORS ACTIVATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173",
                   "http://localhost:5173"],  # Replace with your production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"Hello": "World"}

#Register 
@app.post("/register", response_model=schema.UserResponse)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#Register Admin
@app.post("/register/admin", response_model=schema.UserResponse)
def register_admin(admin: schema.AdminCreate, db: Session = Depends(get_db)):
    """Register a new admin user."""
    db_user = crud.get_user_by_email(db, email=admin.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=admin)


#Login
@app.post("/login", response_model=schema.UserResponse)
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

# # Get current admin
# @app.get("/admin/dashboard")
# def read_admin_dashboard(admin_user = Depends(crud.get_current_admin)):
#     return {"message": f"Welcome, {admin_user.name}"}