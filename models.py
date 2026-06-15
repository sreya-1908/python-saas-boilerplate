# from sqlalchemy import Column, Integer, String, Boolean
# from database import Base

# # This sets up a "users" table in our database
# class User(Base):
#     __tablename__ = "users"

#     # These are the columns in our database table
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
    
#     # This column is crucial for a SaaS! It tracks if they paid or not.
#     is_premium = Column(Boolean, default=False)

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)