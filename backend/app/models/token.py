from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

from .base import Base

T = TypeVar('T')

class TokensDBSchema(BaseModel, Generic[T]):
    id: int = Field(..., description="Unique identifier for the user.")
    created_at: str = Field(..., description="Date and time when the user was created.")
    token: str = Field(..., description="Token for the user.")

class TokensDB(Base):
    """
    SQLAlchemy model for the user table.
    """
    __tablename__ = 'tokens'
    
    id = Column(UUID, primary_key=True, index=True)
    created_at = Column(String, nullable=False)
    token = Column(String, nullable=False)

    def __get_pydantic_core_schema__(self):
        return TokensDBSchema(id=self.id, token=self.token)
    
