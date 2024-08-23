import os
from dotenv import load_dotenv
import urllib.parse
import httpx
import pandas as pd
from fastapi import HTTPException
from app.models import Address, Locode


# Load environment variables from .env file
load_dotenv()

# Access the environment variables
API_KEY = os.getenv("API_KEY")  # API key for accessing the geocoding service
BASE_URL = os.getenv("BASE_URL")  # Base URL for the geocoding API

async def get_coordinates(address: Address):
    """
    Retrieves the geographic coordinates (latitude and longitude) for a given address.
    Constructs the query string using address components and makes an API call 
    to the geocoding service. Returns the coordinates if found.
    """
     # Create a dictionary of the query parameters
    query_params = {
        "q": f"{address.city} {address.zip} {address.state} {address.country}",
        "api_key": API_KEY
    }

    # Encode the query parameters as a URL
    encoded_query = urllib.parse.urlencode(query_params)

    # Construct the full URL
    url = f"{BASE_URL}?{encoded_query}"
    try:
        # Make the request to the geocoding API
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()

                # Check if there are results in the response
                if data:
                    # Extract the latitude and longitude from the first result
                    latitude = data[0]['lat']
                    longitude = data[0]['lon']
                    return float(latitude), float(longitude)
                else:
                    # Raise a 404 Not Found error if no results are found
                    raise HTTPException(status_code=404, detail="No results found for the provided address.")
            else:
                # Raise an HTTPException with the status code from the API response if the call fails
                raise HTTPException(status_code=response.status_code, detail=f"Error in geocoding API call: {response.text}")
    except httpx.RequestError as e:
        # Raise a 502 Bad Gateway error if the geocoding API request fails (e.g., network issues)
        raise HTTPException(status_code=502, detail="Geocoding API request failed. Please try again later.")
    except Exception as e:
        # Raise a 500 Internal Server Error for any unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching coordinates.")

# Load the CSV file into a DataFrame once when the module is loaded
locode_df = pd.read_csv('app/locode_data/code-list.csv')

def lookup_locode(locode: Locode):
    """
    Looks up the address associated with a given locode.
    Splits the locode into country code and location code, then filters the CSV data 
    to find the corresponding address. Returns an Address object if found.
    """
    try:
        # Split the locode into country code and location code
        country_code = locode.locode[:2].strip().upper()
        location_code = locode.locode[2:].strip().upper()

        # Filter the DataFrame to find the row matching the country and location code
        locode_row = locode_df[(locode_df['Country'] == country_code) & (locode_df['Location'] == location_code)]

        if not locode_row.empty:
            # Extract the relevant fields
            country = locode_row.iloc[0]['Country']
            city = locode_row.iloc[0]['Name']
            state = locode_row.iloc[0]['Subdivision'] if pd.notna(locode_row.iloc[0]['Subdivision']) else ''
            zip_code = ''  # No zip code is provided in the CSV

            # Create and return an Address object
            address = Address(
                city=city,
                state=state,
                zip=zip_code,
                country=country
            )
            return address
        else:
            # Raise a 404 Not Found error if the locode is not found in the CSV
            raise HTTPException(status_code=404, detail=f"Locode {locode.locode} not found. Make sure to use the <COUNTRY> <LOCATION> format.")
    except HTTPException as e:
        # Propagate any HTTPExceptions that were raised
        raise e
    except Exception as e:
        # Raise a 500 Internal Server Error for any unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred while looking up the locode.")
