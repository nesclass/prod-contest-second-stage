from typing import Sequence, Iterator, List, Union, Optional
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.country import Country
from app.schemas.country import CountryRegion, CountryAlpha2


def get_country_repository(
    session: Session = Depends(get_session)
) -> Iterator["CountryRepository"]:
    yield CountryRepository(session)


class CountryRepository:
    session: Session
    
    def __init__(self, session: Session):
        self.session = session
    
    def list_countries(self, regions: Union[List[CountryRegion], None] = None) -> Sequence[Country]:
        stmt = select(Country)
        
        if regions:
            stmt = stmt.filter(Country.region.in_(regions))
        
        return self.session.scalars(stmt).fetchall()
    
    def find_country_by_alpha2(self, alpha2: CountryAlpha2) -> Optional[Country]:
        stmt = select(Country).where(Country.alpha2 == alpha2.upper()).limit(1)
        return self.session.scalar(stmt)
