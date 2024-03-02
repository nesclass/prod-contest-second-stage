from typing import Iterator, Optional
from fastapi import Depends

from sqlalchemy import select, update, or_, text
from sqlalchemy.orm import Session

from app.database import get_session, engine
from app.models.user import User

def get_user_repository(
    session: Session = Depends(get_session)
) -> Iterator["UserRepository"]:
    yield UserRepository(session)


class UserRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_login(self, login: str) -> Optional[User]:
        stmt = select(User).where(User.login == login).limit(1)
        return self.session.scalar(stmt)
    
    def find_by_credentials(self, login: str, email: str, phone: Optional[str]) -> Optional[User]:
        stmt = select(User).where(or_(
            User.login == login,
            User.email == email,
            User.phone == phone if phone else None
        )).limit(1)
        return self.session.scalar(stmt)
    
    def find_by_password(self, login: str, password: str) -> Optional[User]:
        stmt = select(User).where(User.login == login, User.password == password).limit(1)
        return self.session.scalar(stmt)
    
    def create(
            self,
            login: str,
            email: str,
            password: str,
            countryCode: str,
            isPublic: bool,
            phone: Optional[str] = None,
            image: Optional[str] = None
    ) -> User:
        user = User(
            login=login,
            email=email,
            password=password,
            countryCode=countryCode,
            isPublic=isPublic,
            phone=phone,
            image=image
        )
        
        self.session.add(user)
        self.session.commit()
        
        return user
    
    def update_profile(
        self,
        login: str,
        countryCode: Optional[str] = None,
        isPublic: Optional[bool] = None,
        phone: Optional[str] = None,
        image: Optional[str] = None
    ) -> User:
        stmt = update(User).returning(User).where(User.login == login)
        
        if countryCode is not None:
            stmt = stmt.values(countryCode=countryCode)
        if isPublic is not None:
            stmt = stmt.values(isPublic=isPublic)
        if phone is not None:
            stmt = stmt.values(phone=phone)
        if image is not None:
            stmt = stmt.values(image=image)
            
        if stmt._values is None:
            stmt = select(User).where(User.login == login)
        
        result = self.session.execute(stmt)
        self.session.commit()
        
        return result.fetchone()[0]
    
    def change_password(self, login: str, password: str):
        stmt = update(User).where(User.login == login).values(password=password)
        self.session.execute(stmt)
        self.session.commit()
