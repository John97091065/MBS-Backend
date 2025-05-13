from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schema, crud, auth
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


#HOMEPAGE ROUTE
@app.get("/")
def read_root():
    """Root endpoint."""
    return {"Hello": "World"}

#Register 
@app.post("/register", response_model=schema.UserResponse)
def register(user: schema.UserCreate, db: Session = Depends(auth.get_db)):
    """Register a new user."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = crud.create_user(db=db, user=user)
    return {
        "message": "User created successfully",
        "redirect_url": "/",
        "user": new_user,
    }

#Register Admin
@app.post("/register/admin", response_model=schema.UserResponse)
def register_admin(admin: schema.AdminCreate, db: Session = Depends(auth.get_db)):
    """Register a new admin user."""
    db_user = crud.get_user_by_email(db, email=admin.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_admin = crud.create_user(db=db, user=admin)
    return {
        "message": "Admin user created successfully",
        "redirect_url": "/admin/dashboard",
        "user": new_admin,
    }

#Login
@app.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(auth.get_db)):
    db_user = crud.login_user(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = crud.create_access_token(data={"sub": db_user.id})

    #Logica Redirect URL
    if db_user.is_admin:
        redirect_url = "/admin/dashboard"
    else:
        redirect_url = "/"

    return {
        "access_token": token,
        "token_type": "bearer",
        "redirect_url": redirect_url,
    }

@app.get("/admin-only")
def read_admin_data(
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(auth.get_current_user),
):
    admin_user = crud.get_current_admin(db, user)
    return {"message": f"Welcome admin: {admin_user.name}"}