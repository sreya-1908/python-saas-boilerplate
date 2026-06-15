# from passlib.context import CryptContext

# # This tells Python to use 'bcrypt', the industry-standard password scrambling tool
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Helper 1: Scrambles a plain text password into a secure hash
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# # Helper 2: Compares a user's typed password with the scrambled hash in the database
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# from datetime import datetime, timedelta
# from passlib.context import CryptContext
# from jose import jwt

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # SECRET_KEY is used to sign the digital tokens. In real life, keep this super secret!
# SECRET_KEY = "SUPER_SECRET_BOILERPLATE_KEY_DONT_TELL_ANYONE"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# # NEW: This function builds the secure digital token for the user
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
    
#     # Encrypt everything into a single, scrambled string
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, status
# from jose import JWTError

# # This tells FastAPI where to look for the security token in incoming requests
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # NEW: This function acts as a security guard for routes
# def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate your security token!",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         # Decode the token using our secret key
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         return email
#     except JWTError:
#         raise credentials_exception


from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "SUPER_SECRET_BOILERPLATE_KEY_DONT_TELL_ANYONE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_email(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token session")