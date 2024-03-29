import os

from typing import Iterator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base(
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
)

engine = create_engine(
    os.getenv(
        "POSTGRES_CONN",
        default="postgresql://postgres:postgres@127.0.0.1:5432/prod"
    ).replace("postgres://", "postgresql://"),
    pool_pre_ping=True,
    echo=False
)

session_maker = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


def init_database():
    from app.models import country, user, friendship, post  # noqa: F401


def get_session() -> Iterator[Session]:
    with session_maker() as session:
        yield session
