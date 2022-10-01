from select import select
from fastapi import APIRouter, Body, Depends, HTTPException,Request, status
from typing import List
from models.drone import Medication

from database.connection import get_session

from sqlmodel  import select

medication_router = APIRouter(
    tags=["medication"]
)

@medication_router.post("/new")
async def register_medication(
    new_medication : Medication = Body(...),
    session=Depends(get_session)
    ):
    session.add(new_medication)
    session.commit()
    session.refresh(new_medication)
    return {
    "message": "Medication created successfully"
    }

@medication_router.get("/", response_model=List[Medication])
async def get_all_medications(session=Depends(get_session)):
    statement = select(Medication) 
    medications = session.exec(statement).all()
    return medications

@medication_router.get("/{id}", response_model=Medication)
async def get_medication(id: int, session=Depends(get_session)):
    medication = session.get(Medication, id)
    if medication:
        return medication
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Medication with supplied ID does not exist"
    )