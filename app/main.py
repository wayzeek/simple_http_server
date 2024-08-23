from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Geocoding API",
    description="API for converting addresses and locodes to geographic coordinates",
    version="1.0.0"
)

# Include API routes
app.include_router(router)

# Global exception handler for catching unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please contact support."},
    )
