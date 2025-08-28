# async engine, session, Base, get_db

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
