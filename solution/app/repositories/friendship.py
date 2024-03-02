from typing import Iterator, Optional
from fastapi import Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.friendship import Friendship


def get_friendship_repository(
    session: Session = Depends(get_session)
) -> Iterator["FriendshipRepository"]:
    yield FriendshipRepository(session)


class FriendshipRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_users(self, user_id: int, target_id: int) -> Optional[Friendship]:
        stmt = select(Friendship).where(Friendship.user_id == user_id, Friendship.target_id == target_id).limit(1)
        return self.session.scalar(stmt)

    def create(self, user_id: int, target_id: int) -> Friendship:
        friendship = Friendship(user_id=user_id, target_id=target_id)
        self.session.add(friendship)
        self.session.commit()
        return friendship
    
    def remove(self, user_id: int, target_id: int):
        stmt = delete(Friendship).where(Friendship.user_id == user_id, Friendship.target_id == target_id)
        self.session.execute(stmt)
        self.session.commit()
