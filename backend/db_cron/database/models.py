from sqlalchemy import (
  Column, Integer, String, TIMESTAMP
)
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

T = TypeVar('T')

class UserDBSchema(BaseModel, Generic[T]):
    id: int = Field(..., description="Unique identifier for the user.")
    username: str = Field(..., description="The username of the user.")
    email: str = Field(..., description="The email of the user.")
    password: str = Field(..., description="The password of the user.")
    created_at: datetime = Field(..., description="The date and time the user was created.")
    updated_at: datetime = Field(..., description="The date and time the user was last updated.")

class UserDB(Base):
    """
    SQLAlchemy model for the user table.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __get_pydantic_core_schema__(self):
        return UserDBSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
