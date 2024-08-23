import os
from dotenv import load_dotenv
import httpx
import pandas as pd
from models import Address, Locode

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


async def get_coordinates(address: Address):
    # Construct the query string from the address components
    query = f"{address.city}+{address.state}+{address.zip}+{address.country}"
    url = f"{BASE_URL}?q={query}&api_key={API_KEY}"
    
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
                raise ValueError("No results found for the provided address.")
        else:
            raise ValueError(f"Error in geocoding API call: {response.status_code} - {response.text}")

# Load the CSV file into a DataFrame once when the module is loaded
locode_df = pd.read_csv('app/locode_data/code-list.csv')

def lookup_locode(locode: Locode):
    
     # Split the locode into country code and location code
    country_code = locode[:2].strip().upper()
    location_code = locode[2:].strip().upper()
    
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
        raise ValueError(f"Locode {locode} not found.\nMake sure to use the <COUNTRY> <LOCATION> format.")