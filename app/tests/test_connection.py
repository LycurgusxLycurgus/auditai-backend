# app/tests/test_connection.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

async def test_connection():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres.ppdacijqpyzzitxhkxgo:uEDEVyUPzSF66nz9@aws-0-us-east-1.pooler.supabase.com:5432/postgres")
    
    # Ensure the URL uses the asyncpg driver
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(DATABASE_URL)
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Connection successful! Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())