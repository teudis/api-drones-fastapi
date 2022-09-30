from fastapi import APIRouter, Body
from models.drone import Drone, Medication

drone_router = APIRouter(
    tags=["drone"]
)


@drone_router.post("/drone/new")
async def register_drone(drone : Drone = Body(...)):
    return drone