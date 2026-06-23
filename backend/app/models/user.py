from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    """User model representing an account holder.

    Attributes
    ----------
    id: Primary key.
    email: Unique email address used for login.
    hashed_password: Bcrypt‑hashed password.
    is_active: Indicates if the account is active.
    created_at / updated_at: Timestamps.
    todos: Relationship to the user's Todo items.
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")
