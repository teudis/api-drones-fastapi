from fastapi import APIRouter, Body, Depends, HTTPException,status
from requests import session
from models.drone import Drone, DroneUpdate

from typing import List

from database.connection import get_session
from sqlmodel  import select


drone_router = APIRouter(
    tags=["drone"]
)


@drone_router.post("/new")
async def register_drone(new_drone : Drone = Body(...), session=Depends(get_session)):
    session.add(new_drone)
    session.commit()
    session.refresh(new_drone)
    return {
    "message": "Drone created successfully"
    }

@drone_router.get("/", response_model=List[Drone])
async def get_all_drone(session=Depends(get_session)):
    query = select(Drone)
    all_drones = session.exec(query).all()
    return all_drones

@drone_router.get("/{id}", response_model=Drone)
async def get_drone_id(id: int, session=Depends(get_session)):
    drone = session.get(Drone, id)
    if drone:
       return drone
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drone with supplied ID does not exist"
    )


@drone_router.put("/edit/{id}", response_model=Drone)
async def update_drone(id: int, updated_drone:DroneUpdate = Body(...), session=Depends(get_session)):
    drone = session.get(Drone, id)
    if drone:
        data_drone = updated_drone.dict(exclude_unset=True)
        for key, value in data_drone.items():
            setattr(drone, key, value)
            session.add(drone)
            session.commit()
            session.refresh(drone)
            return drone
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drone with supplied ID does not exist"
    )

@drone_router.delete("/delete/{id}")
async def delete_drone(id: int, session=Depends(get_session)):
    drone = session.get(Drone, id)
    if drone :
        session.delete(drone)
        session.commit()
        return {
        "message": "Drone was deleted successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drone with supplied ID does not exist"
    )
