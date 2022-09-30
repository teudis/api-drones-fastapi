from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Model(str, Enum):
    Lightweight = "Lightweight"
    Middleweight = "Middleweight"
    Cruiserweight = "Cruiserweight"
    Heavyweight = "Heavyweight"


class State(Enum):
    IDLE = "IDLE"
    LOADING = "LOADING"
    LOADED = "LOADED"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    RETURNING = "RETURNING"


class Medication (BaseModel):
    name : str
    weight : float
    code : str
    image :str

class Drone(BaseModel):
    serial_number : str = Field(..., max_length=100)
    model: Model = Field(...,default=None)
    weigth_limit: float = Field(..., gt=0, le=500)
    battery_capacity: int = Field(..., gt=0, le=100, )
    state : State = Field(..., default=None)
    medications : Optional[list[Medication]]
