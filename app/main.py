from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import auth
from app.api.routers import resume
from app.api.routers import information
from app.db.database import engine
from app.db import models

app = FastAPI(title=settings.PROJECT_NAME)

# Routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(information.router)

# DEV ONLY: auto-create tables on startup 
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)