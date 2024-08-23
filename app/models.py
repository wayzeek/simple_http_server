from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    zip: str
    country: str
    
class Locode(BaseModel):
    locode: str