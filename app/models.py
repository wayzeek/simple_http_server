from pydantic import BaseModel

# Define the Address model using Pydantic
class Address(BaseModel):
    """
    The Address model represents a physical address with the following components:
    - city: The name of the city (e.g., "Montreal")
    - state: The state or province name (e.g., "QC" for Quebec)
    - zip: The postal or ZIP code (e.g., "H3A")
    - country: The country name or code (e.g., "Canada")
    """
    city: str
    state: str
    zip: str
    country: str

# Define the Locode model using Pydantic
class Locode(BaseModel):
    """
    The Locode model represents a location code, typically in the format:
    - locode: A string combining a country code and location code separated by a space (e.g., "CAM TR" for Montreal, Canada)
    """
    locode: str
