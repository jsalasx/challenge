from pydantic import BaseModel
from typing import List

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO:str
    MES: int


class FlightData(BaseModel):
    flights: List[Flight]
