from fastapi import APIRouter, HTTPException
from app.models import Address, Locode
from app.services import get_coordinates, lookup_locode

# Initialize an API router instance to define route handlers
router = APIRouter()

@router.post("/geocode")
async def geocode_address(address: Address):
    """
    Endpoint to geocode an address. 
    It takes an Address model as input, processes it to obtain latitude and longitude, 
    and returns these coordinates in a JSON response.
    """
    try:
        # Call the get_coordinates function to retrieve latitude and longitude
        latitude, longitude = await get_coordinates(address)
        return {"latitude": latitude, "longitude": longitude}
    except ValueError as e:
        # Raise a 404 Not Found error if no results are found for the address
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Raise a 500 Internal Server Error for any unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the address.")

@router.post("/locode")
async def geocode_locode(locode: Locode):
    """
    Endpoint to geocode a location code (locode).
    It takes a Locode model as input, looks up the associated address, 
    and then processes it to obtain latitude and longitude, returning these in a JSON response.
    """
    try:
        # Look up the address corresponding to the provided locode
        address = lookup_locode(locode)
        # Reuse the geocode_address function to get the coordinates
        return await geocode_address(address)
    except ValueError as e:
        # Raise a 404 Not Found error if the locode or corresponding address is not found
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        # Propagate any HTTPException raised by the geocode_address function
        raise e
    except Exception as e:
        # Raise a 500 Internal Server Error for any unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the locode.")
