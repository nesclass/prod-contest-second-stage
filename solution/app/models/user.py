from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.friendship import Friendship


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, nullable=False, unique=True, primary_key=True)
    login: Mapped[str] = mapped_column("login", String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column("email", String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column("phone", String(20), nullable=True, unique=True)
    password: Mapped[str] = mapped_column("password", String(64), nullable=False, unique=False)
    countryCode: Mapped[str] = mapped_column("countryCode", String(2), nullable=False, unique=False)
    isPublic: Mapped[bool] = mapped_column("isPublic", Boolean(), nullable=False, unique=False)
    image: Mapped[str] = mapped_column("image", String(200), nullable=True, unique=False)
