# from fastapi import FastAPI

# # This creates your web application
# app = FastAPI()

# # This is the front page of your server
# @app.get("/")
# def home():
#     return {"message": "Welcome to your SaaS Boilerplate foundation! It works!"}
# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# import database

# app = FastAPI()

# # This tells the server to automatically create the database file when it starts
# database.Base.metadata.create_all(bind=database.engine)

# @app.get("/")
# def home(db: Session = Depends(database.get_db)):
#     return {"message": "Welcome to your SaaS Boilerplate! Your server and database are connected!"}
# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# import database
# import models  # <-- We added this import

# app = FastAPI()

# # This line reads your models.py and builds the actual tables in the database file
# database.Base.metadata.create_all(bind=database.engine)

# @app.get("/")
# def home(db: Session = Depends(database.get_db)):
#     return {"message": "Welcome to your SaaS Boilerplate! Server, Database, and User Models are live!"}
# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# import database
# import models
# import auth  # <-- We import our new security helpers
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi import Request
# import payments


# app = FastAPI()

# app.include_router(payments.router)

# templates = Jinja2Templates(directory="templates")

# database.Base.metadata.create_all(bind=database.engine)

# @app.get("/", response_class=HTMLResponse)
# def serve_home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# # NEW: This is the registration/signup route
# @app.post("/register")
# def register_user(email: str, password: str, db: Session = Depends(database.get_db)):
#     # 1. Check if a user with this email already exists
#     existing_user = db.query(models.User).filter(models.User.email == email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="Email is already registered!"
#         )
    
#     # 2. Scramble the password securely using our auth tool
#     secure_password = auth.get_password_hash(password)
    
#     # 3. Create a new user blueprint row
#     new_user = models.User(email=email, hashed_password=secure_password)
    
#     # 4. Save the user into the saas.db file
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return {"message": "User registered successfully!", "user_id": new_user.id}

# # NEW: This is the login route
# @app.post("/login")
# def login_user(email: str, password: str, db: Session = Depends(database.get_db)):
#     # 1. Look for the user in the database
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Invalid email or password!"
#         )


#     # 2. Check if the password they typed matches the scrambled hash in the DB
#     if not auth.verify_password(password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Invalid email or password!"
#         )
    
#     # 3. Create the secure login token containing their email
#     access_token = auth.create_access_token(data={"sub": user.email})
    
#     return {"access_token": access_token, "token_type": "bearer", "message": "Logged in successfully!"}

# # NEW: A protected route that only logged-in users can see
# from fastapi import Header

# @app.get("/dashboard")
# def get_dashboard_data(authorization: str = Header(None), db: Session = Depends(database.get_db)):
#     # 1. Check if the frontend sent the Authorization header
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Missing security token")
        
#     try:
#         # 2. Extract the raw token from "Bearer <token>"
#         token_type, token = authorization.split(" ")
#         email = auth.get_current_user_email(token)
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token session")

#     # 3. Pull the user from the database file
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User profile not found")

#     return {
#         "status": "success",
#         "user_email": user.email,
#         "is_premium_subscriber": user.is_premium,
#         "secret_dashboard_data": "This is secure data retrieved dynamically for your account."
#     }


from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database
import models
import auth
import payments

app = FastAPI()
templates = Jinja2Templates(directory="templates")

database.Base.metadata.create_all(bind=database.engine)
app.include_router(payments.router)

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    # Pass context safely using explicit keyword notation to satisfy Python 3.14 requirements
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/register")
def register_user(email: str, password: str, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered!")
    
    secure_password = auth.get_password_hash(password)
    new_user = models.User(email=email, hashed_password=secure_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully!", "user_id": new_user.id}

@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password!")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/dashboard")
def get_dashboard_data(authorization: str = Header(None), db: Session = Depends(database.get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    try:
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
        email = auth.get_current_user_email(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "status": "success",
        "user_email": user.email,
        "is_premium_subscriber": user.is_premium,
        "secret_dashboard_data": "This is secure data retrieved dynamically for your account."
    }
