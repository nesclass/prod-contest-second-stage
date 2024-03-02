from typing import Literal
from typing_extensions import Annotated

from pydantic import BaseModel, Field, ConfigDict

CountryName = Annotated[str, Field(max_length=100, description="Полное название страны")]
CountryAlpha2 = Annotated[str, Field(max_length=2, pattern=r"^[a-zA-Z]{2}$", description="Двухбуквенный код, уникально идентифицирующий страну")]
CountryAlpha3 = Annotated[str, Field(max_length=3, pattern=r"^[a-zA-Z]{3}$", description="Трехбуквенный код страны")]
CountryRegion = Annotated[Literal["Europe", "Asia", "Oceania", "Americas", "Africa"], Field(description="Географический регион, к которому относится страна")]
    

class CountrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: CountryName
    alpha2: CountryAlpha2
    alpha3: CountryAlpha3
    region: CountryRegion
