from sqlalchemy import (
  Column, Integer, String, TIMESTAMP, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.schema import ForeignKey

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

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class MessageDBSchema(BaseModel, Generic[T]):
    id: int = Field(..., description="Unique identifier for the message.")
    user_id: int = Field(..., description="The user associated with the message.")    
    message: str = Field(..., description="Table name associated with the message.")

class MessageDB(Base):
    """
    SQLAlchemy model for the audit table.
    """
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = ForeignKey('users.id')
    message = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    
    
