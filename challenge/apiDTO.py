from typing import List
from pydantic import BaseModel, validator
from enum import Enum

class ValidStrValues(str, Enum):
    VALUE1 = "I"
    VALUE2 = "N"

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: ValidStrValues
    MES: int
    @validator("MES")
    def quantity_must_be_under_100(cls, value):
        if value > 12:
            raise ValueError("La cantidad no debe ser mayor a 12")
        return value
class FlightData(BaseModel):
    flights: List[Flight]
