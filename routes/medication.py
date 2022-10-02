from select import select
from fastapi import APIRouter, Body, Depends, HTTPException,Request, status
from typing import List
from models.drone import Medication, MedicationUpate

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

@medication_router.put("/edit/{id}", response_model=Medication)
async def update_medication( 
    id: int, 
    updated_medication : MedicationUpate = Body(...),
    session=Depends(get_session)):
    medication = session.get(Medication, id)
    if medication:
        medication_data = updated_medication.dict(exclude_unset=True)
        for key, value in medication_data.items():
            setattr(medication, key, value)
        session.add(medication)
        session.commit()
        session.refresh(medication)
        return medication
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Medication with supplied ID does not exist"
    )


@medication_router.delete("/delete/{id}")
async def delete_medication(id:int, sesion=Depends(get_session)):
    medication = sesion.get(Medication, id)
    if medication:
        sesion.delete(medication)
        sesion.commit()
        return {
        "message": "Medication was deleted successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Medication with supplied ID does not exist"
    )