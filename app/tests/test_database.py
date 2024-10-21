# app/tests/test_database.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/test_db")

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(prepare_database):
    async with TestingSessionLocal() as session:
        yield session


async def test_insert_activacion(db_session: AsyncSession):
    from app.models import Activacion
    from datetime import date

    activacion = Activacion(
        usuario_activador="test_user",
        fecha_activacion=date.today(),
        numero_archivos=3
    )
    db_session.add(activacion)
    await db_session.commit()
    assert activacion.id_lote is not None
