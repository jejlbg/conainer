from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, UniqueConstraint, JSON
from sqlalchemy.orm import relationship

# import Base to create classes that inherit from it
from database import Base

# Class to create db tables named "users"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)