from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class TodoBase(BaseModel):
    """Base fields shared by create and read schemas."""
    title: str = Field(..., max_length=255, description="Title of the todo item")
    description: Optional[str] = Field(None, description="Optional detailed description")
    is_completed: bool = Field(False, description="Completion status")

    @validator("title")
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

class TodoCreate(TodoBase):
    """Schema for creating a new Todo."""
    pass

class TodoUpdate(BaseModel):
    """Schema for partial updates; all fields are optional."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = None

    @validator("title")
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v

class TodoRead(TodoBase):
    """Schema returned to clients; includes identifiers and timestamps."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
