from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base

class Todo(Base):
    """Todo model representing a single task.

    Attributes
    ----------
    id: Primary key.
    user_id: Foreign key to the owning user.
    title: Short description of the task.
    description: Optional longer description.
    is_completed: Completion flag.
    created_at / updated_at: Timestamps.
    owner: Relationship back to the User.
    """

    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_user_id", "user_id"),
        Index("ix_todos_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="todos")
