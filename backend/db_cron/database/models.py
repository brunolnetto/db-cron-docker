from sqlalchemy import (
  Column, Integer, String
)
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

T = TypeVar('T')

class TokensDBSchema(BaseModel, Generic[T]):
    id: int = Field(..., description="Unique identifier for the user.")
    token: str = Field(..., description="Token for the user.")

class TokensDB(Base):
    """
    SQLAlchemy model for the user table.
    """
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, nullable=False)

    def __get_pydantic_core_schema__(self):
        return TokensDBSchema(id=self.id, token=self.token)
    
