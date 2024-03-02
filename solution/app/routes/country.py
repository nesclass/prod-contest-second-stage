from typing import List, Union, Sequence
from typing_extensions import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException

from app.exceptions import APIError
from app.schemas.country import CountrySchema, CountryRegion, CountryAlpha2
from app.repositories.country import CountryRepository, get_country_repository

router = APIRouter()


@router.get("/api/countries")
def list_countries_handler(
    regions: Annotated[Union[List[CountryRegion], None], Query(alias="region")] = None,
    country_repository: CountryRepository = Depends(get_country_repository)
) -> Sequence[CountrySchema]:
    return country_repository.list_countries(regions=regions)


@router.get("/api/countries/{alpha2}")
def find_country_by_alpha2_handler(
    alpha2: CountryAlpha2,
    country_repository: CountryRepository = Depends(get_country_repository)
) -> CountrySchema:
    country = country_repository.find_country_by_alpha2(alpha2=alpha2)
    if country is None:
        raise APIError(status_code=404, reason="Страна с указанным alpha2-кодом не найдена.")
    return country
