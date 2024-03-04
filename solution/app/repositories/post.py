from typing import Iterator, Optional, Sequence, List
from fastapi import Depends
from datetime import datetime

from sqlalchemy import select, delete, update, insert, desc
from sqlalchemy.orm import Session, selectinload

from app.database import get_session
from app.models.post import Post
from app.models.user import User


def get_post_repository(
    session: Session = Depends(get_session)
) -> Iterator["PostRepository"]:
    yield PostRepository(session)


class PostRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user: User, content: str, tags: List[str]) -> Post:
        post = Post(user=user, content=content, tags=tags)
        self.session.add(post)
        self.session.commit()
        return post
    
    def find_by_id(self, post_id: int) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id).limit(1)
        return self.session.scalar(stmt)
    