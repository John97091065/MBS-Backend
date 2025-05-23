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
@app.post("/admin/register", response_model=schema.UserResponse)
def register_admin(admin: schema.AdminCreate, db: Session = Depends(auth.get_db)):
    """Register a new admin user."""
    db_user = crud.get_user_by_email(db, email=admin.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_admin = crud.create_user(db=db, user=admin)
    return {
        "message": "Admin user created successfully",
        "redirect_url": "/admin-dashboard",
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
        redirect_url = "/admin-dashboard"
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

#GET ALL USERS
@app.get("/users", response_model=list[schema.UserResponse])
def get_all_users(
    db: Session = Depends(auth.get_db),
    # user: models.User = Depends(auth.get_current_user),
):
    # """Get all users."""
    # if not user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not an admin user")
    
    users = crud.get_all_users(db=db)
    return users

#GET ALL ADMINS
@app.get("/admins", response_model=list[schema.UserResponse])
def get_all_admins(
    db: Session = Depends(auth.get_db),
    # user: models.User = Depends(auth.get_current_user),
):
    # """Get all admin users."""
    # if not user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not an admin user")
    
    admins = crud.get_all_admins(db=db)
    return admins

#PRODUCTS CREATE
@app.post("/CreateProducts", response_model=schema.ProductCreate)
def create_product(
    product: schema.ProductCreate,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(auth.get_current_user),
):
    """Create a new product."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin user")
    
    new_product = crud.create_product(db=db, product=product, user=user)
    return {
        "message": "Product created successfully",
        "redirect_url": "/admin-dashboard",
        "product": new_product,
    }

#VIEW ALL PRODUCTS
@app.get("/products", response_model=list[schema.ProductCreate])
def get_all_products(db: Session = Depends(auth.get_db)):
    """Get all products."""
    products = crud.get_all_products(db=db)
    return products