from typing import TYPE_CHECKING, List
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, nullable=False, unique=True, primary_key=True)
    createdAt: Mapped[datetime] = mapped_column("createdAt", DateTime(), nullable=False, default=datetime.now)
    
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="posts_user_id", foreign_keys=[user_id], lazy="selectin")
    
    content: Mapped[str] = mapped_column("content", String(1000), nullable=False)
    tags: Mapped[List[str]] = mapped_column("tags", ARRAY(String(20)), default=[], nullable=False)
