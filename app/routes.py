from fastapi import APIRouter, HTTPException
from app.models import Address, Locode
from app.services import get_coordinates, lookup_locode

router = APIRouter()

@router.post("/geocode")
async def geocode_address(address: Address):
    try:
        latitude, longitude = await get_coordinates(address)
        return {"latitude": latitude, "longitude": longitude}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the address.")

@router.post("/locode")
async def geocode_locode(locode: Locode):
    try:
        address = lookup_locode(locode)
        return await geocode_address(address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e  # Propagate HTTPExceptions raised by `geocode_address`
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the locode.")