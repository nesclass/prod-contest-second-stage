from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Friendship(Base):
    __tablename__ = "friendships"
    
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, nullable=False, unique=True, primary_key=True)
    
    # я не делаю default=datetime.now только потому, что у меня более тяжелая логика обновления дат
    added_at: Mapped[datetime] = mapped_column("added_at", DateTime(), nullable=False)
    
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"), nullable=False)
    # user: Mapped["User"] = relationship("User", backref=backref("friendships", order_by=id), primaryjoin="friendships.user_id == users.id")
    user: Mapped["User"] = relationship("User", backref="friendships_user_id", foreign_keys=[user_id], lazy="noload")
    
    target_id: Mapped[int] = mapped_column("target_id", ForeignKey("users.id"), nullable=False)
    # target: Mapped["User"] = relationship("User", primaryjoin="friendships.target_id == users.id")
    target: Mapped["User"] = relationship("User", backref="friendships_target_id", foreign_keys=[target_id], lazy="noload")
