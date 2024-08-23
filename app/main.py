from fastapi import FastAPI
from routes import router
from services import lookup_locode, get_coordinates

app = FastAPI()

app.include_router(router)

