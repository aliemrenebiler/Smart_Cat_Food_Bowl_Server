from fastapi import FastAPI

from api.routes import devices
from db import models
from db.database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Cat API")

# Include routers
app.include_router(devices.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Cat API"}
