from fastapi import APIRouter
from app.models import Address, Locode
from app.services import get_coordinates, lookup_locode

router = APIRouter()

@router.post("/geocode")
async def geocode_address(address: Address):
    latitude, longitude = await get_coordinates(address)
    return {"latitude": latitude, "longitude": longitude}

@router.post("/locode")
async def geocode_locode(locode: Locode):
    address = lookup_locode(locode)
    geocode_address(address)