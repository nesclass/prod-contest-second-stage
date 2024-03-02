from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Friendship(Base):
    __tablename__ = "friendships"
    
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, nullable=False, unique=True, primary_key=True)
    
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"), nullable=False)
    # user: Mapped["User"] = relationship("User", backref=backref("friendships", order_by=id), primaryjoin="friendships.user_id == users.id")
    user: Mapped["User"] = relationship("User", backref="friendships_user_id", foreign_keys=[user_id])
    
    target_id: Mapped[int] = mapped_column("target_id", ForeignKey("users.id"), nullable=False)
    # target: Mapped["User"] = relationship("User", primaryjoin="friendships.target_id == users.id")
    target: Mapped["User"] = relationship("User", backref="friendships_target_id", foreign_keys=[target_id])
