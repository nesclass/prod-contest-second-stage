from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Country(Base):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True)
    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    alpha2: Mapped[str] = mapped_column("alpha2", String(2), nullable=False)
    alpha3: Mapped[str] = mapped_column("alpha3", String(3), nullable=False)
    region: Mapped[str] = mapped_column("region", String(16), nullable=False)
