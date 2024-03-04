from typing import Iterator, Optional, Sequence
from fastapi import Depends
from datetime import datetime

from sqlalchemy import select, delete, update, insert, desc
from sqlalchemy.orm import Session, selectinload

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

    def update_or_insert(self, user_id: int, target_id: int) -> None:
        # friendship = Friendship(user_id=user_id, target_id=target_id)
        # self.session.add(friendship)
        # self.session.commit()
        # return friendship
        stmt = update(Friendship) \
            .returning(Friendship) \
            .where(Friendship.user_id == user_id, Friendship.target_id == target_id) \
            .values(added_at=datetime.now())
        
        if self.session.execute(stmt).first() is None:
            stmt = insert(Friendship).values(
                user_id=user_id,
                target_id=target_id,
                added_at=datetime.now()
            )
            
            self.session.execute(stmt)
        
        self.session.commit()
    
    def delete(self, user_id: int, target_id: int):
        stmt = delete(Friendship).where(Friendship.user_id == user_id, Friendship.target_id == target_id)
        self.session.execute(stmt)
        self.session.commit()
        
    def find_and_paginate(self, user_id: int, limit: int = 5, offset: int = 0) -> Sequence[Friendship]:
        stmt = select(Friendship) \
            .where(Friendship.user_id == user_id) \
            .order_by(desc(Friendship.added_at)) \
            .limit(limit) \
            .offset(offset) \
            .options(selectinload(Friendship.target))
            
        return self.session.scalars(stmt).fetchall()
