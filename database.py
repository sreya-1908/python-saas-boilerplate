# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # 1. This tells Python to create a local database file named 'saas.db'
# DATABASE_URL = "sqlite:///./saas.db"

# # 2. This is the engine that connects our code to the database file
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # 3. This creates a 'Session' which lets us read and write data
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 4. This is a helper that we will use later to create database tables (like Users)
# Base = declarative_base()

# # 5. A quick helper function to open and close database connections automatically
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./saas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()