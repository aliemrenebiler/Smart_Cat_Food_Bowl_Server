from fastapi import FastAPI

from api.routes import devices
from db.models import device_models
from db.database import engine

# Create database tables
device_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Cat API")

# Include routers
app.include_router(devices.router)


@app.get("/")
def get_info():
    return "Welcome to the Smart Cat API"
