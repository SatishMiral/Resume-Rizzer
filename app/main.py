# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import auth
from app.db.database import engine
from app.db import models
from app.api.routers import resume

app = FastAPI(title=settings.PROJECT_NAME)

# Routers
app.include_router(auth.router)
app.include_router(resume.router)

# DEV ONLY: auto-create tables on startup 
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)