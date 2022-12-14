from sqlmodel import JSON, SQLModel, Field, Column
from enum import Enum
from typing import Optional, List

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

class Medication (SQLModel, table=True):
    """Class Model Medication"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name : str
    weight : float
    code : str
    image : Optional[str]

   
class MedicationUpate (SQLModel):
    """Class Update Model Medication"""     
    name : str
    weight : float
    code : str
    image : Optional[str]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
        "example": {
        "name": "Paracetamol",
        "weight": "10",   
        "code": "K45R"
         }
        }

class Drone(SQLModel, table=True):
    """Class Model Drone"""
    id: int = Field(default=None, primary_key=True)
    serial_number : str = Field(..., max_length=100)
    model: Model = Field(...)
    weigth_limit: float = Field(..., gt=0, le=500)
    battery_capacity: int = Field(..., gt=0, le=100, )
    state : State = Field(...)
    medications : Optional[List[str]] = Field(sa_column=Column(JSON))


class DroneUpdate(SQLModel):
    """Class Update Model Drone"""    
    serial_number : str = Field(..., max_length=100)
    model: Model = Field(...)
    weigth_limit: float = Field(..., gt=0, le=500)
    battery_capacity: int = Field(..., gt=0, le=100, )
    state : State = Field(...)
    medications : Optional[List[str]] = Field(sa_column=Column(JSON))
    
