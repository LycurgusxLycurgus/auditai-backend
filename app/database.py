# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres.ppdacijqpyzzitxhkxgo:uEDEVyUPzSF66nz9@aws-0-us-east-1.pooler.supabase.com:5432/postgres")

# Ensure the URL uses the asyncpg driver
url = make_url(DATABASE_URL)
if url.drivername == "postgresql":
    url = url.set(drivername="postgresql+asyncpg")
elif url.drivername != "postgresql+asyncpg":
    raise ValueError("Database URL must use the postgresql+asyncpg driver")

engine = create_async_engine(
    str(url),  # Convert URL object to string
    echo=True,
    pool_pre_ping=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
