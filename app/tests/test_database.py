# app/tests/test_database.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.engine.url import make_url
from sqlalchemy import select
from app.database import get_db, AsyncSessionLocal
from app.base import Base
from app.models import *  # Import all models
import os
import json
from datetime import date, datetime

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://postgres.ppdacijqpyzzitxhkxgo:uEDEVyUPzSF66nz9@aws-0-us-east-1.pooler.supabase.com:5432/postgres")

# Ensure the URL uses the asyncpg driver
url = make_url(TEST_DATABASE_URL)
if url.drivername == "postgresql":
    url = url.set(drivername="postgresql+asyncpg")
elif url.drivername != "postgresql+asyncpg":
    raise ValueError("Test Database URL must use the postgresql or postgresql+asyncpg driver")

engine = create_async_engine(
    url,
    echo=True,
    poolclass=NullPool,
    future=True
)

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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_complete_data_scenario(db_session: AsyncSession):
    # 1. Create Activacion
    activacion = Activacion(
        id_lote=101,
        usuario_activador="test_user",
        fecha_activacion=date(2024, 10, 26),
        numero_archivos=3
    )
    db_session.add(activacion)
    await db_session.flush()

    # 2. Create IndexTable entries
    index_entries = [
        IndexTable(id_documento=1001, id_lote=101, titulo_documento="TEST-CONTRACT-001.pdf", ocr=False, tipo_documento="contrato", trasladado_descargados=True, url_descargados="/path/to/contract.pdf", usuario_dueno="test_user", supervisado=True),
        IndexTable(id_documento=1002, id_lote=101, titulo_documento="TEST-CONTRACT-001-otrosi1.pdf", ocr=False, tipo_documento="otrosi", trasladado_descargados=True, url_descargados="/path/to/otrosi1.pdf", usuario_dueno="test_user", supervisado=True),
        IndexTable(id_documento=1003, id_lote=101, titulo_documento="TEST-CONTRACT-001-poliza.pdf", ocr=True, tipo_documento="poliza", trasladado_descargados=True, url_descargados="/path/to/poliza.pdf", usuario_dueno="test_user", supervisado=True)
    ]
    db_session.add_all(index_entries)
    await db_session.flush()

    # 3. Create Documento entries
    documento_entries = [
        Documento(id_documento=1001, id_lote=101, contenido="This is the content of the test contract."),
        Documento(id_documento=1002, id_lote=101, contenido="This is the content of the test otrosi."),
        Documento(id_documento=1003, id_lote=101, contenido="This is the content of the test poliza.")
    ]
    db_session.add_all(documento_entries)
    await db_session.flush()

    # 4. Create Contratos entry
    contrato = Contratos(
        id_documento=1001,
        id_lote=101,
        consecutivo_contrato="TEST-CONTRACT-001",
        programa_mitigacion="Test Mitigation Program",
        json_contratos_info_general=json.dumps({
            "output": {
                "Datos Generales del Contrato": {
                    "Compañía": "Test Company A",
                    "Nit/Rut/RFC compañía": "123456789",
                    "Nit tercero": "987654321",
                    "Nombre del Tercero": "Test Company B",
                    "Tipo de contrato": "Service Agreement",
                    "Tipo de servicio": "Consulting",
                    "Objeto": "Provide consulting services.",
                    "Moneda": "USD",
                    "Valor": "100000",
                    "Fecha Inicio y Terminación": {
                        "Inicio": "2024-01-01",
                        "Terminación": "2024-12-31"
                    },
                    "Vigencia": "1 year"
                }
            }
        }),
        json_contratos_clausulas=json.dumps({
            "output": {
                "Checklist de Cláusulas Contractuales": {
                    "Obligaciones de las Partes": {
                        "Existe la cláusula": "Si",
                        "Número de la cláusula": ["1", "2"],
                        "Nombre de la cláusula": ["Obligations of Company A", "Obligations of Company B"],
                        "Descripción": ["Company A will...", "Company B will..."]
                    }
                }
            }
        }),
        json_contratos_amparos=json.dumps({
            "output": {
                "Checklist de Pólizas": {
                    "¿Tiene Garantía para buen manejo de anticipo?": {
                        "Existe la garantía": "Si",
                        "Descripción": ["Guarantee details..."]
                    }
                }
            }
        })
    )
    db_session.add(contrato)
    await db_session.flush()

    # 5. Create Otrosi entry
    otrosi = Otrosi(
        id_documento=1002,
        id_lote=101,
        numero_otrosi="1",
        consecutivo_contrato="TEST-CONTRACT-001",
        json_otrosi_info_general=json.dumps({
            "output": {
                "Datos Generales del otrosi": {
                    "Nit tercero": "987654321",
                    "Nombre del Tercero": "Test Company B",
                    "Fecha firma otrosi": "2024-06-01"
                }
            }
        }),
        json_otrosi_modificaciones=json.dumps({
            "output": {
                "Modificaciones": {
                    "Valor_del_contrato": [
                        {
                            "Hay_modificación": "Si",
                            "Modificacion_hecha": "Increased contract value to $150,000."
                        }
                    ]
                }
            }
        })
    )
    db_session.add(otrosi)
    await db_session.flush()

    # 6. Create Poliza entry
    poliza = Poliza(
        id_documento=1003,
        id_lote=101,
        numero_otrosi=None,
        numero_poliza="POLICY-12345",
        consecutivo_contrato="TEST-CONTRACT-001",
        json_poliza_info_general=json.dumps({
            "output": {
                "Datos Generales de la póliza": {
                    "Nombre de tomador": "Test Company A",
                    "Nombre de beneficiado": "Test Company B",
                    "Objeto de la póliza": "Insurance coverage for...",
                    "Valor total a pagar": "5000",
                    "Valor total asegurado": "200000",
                    "Fecha de pago": "2024-01-15"
                }
            }
        }),
        json_poliza_amparos=json.dumps({
            "output": {
                "Checklist de Pólizas": {
                    "¿Tiene Garantía para buen manejo de anticipo?": {
                        "Existe la garantía": "Si",
                        "Descripción": ["Policy details..."],
                        "Fecha inicio": "2024-01-01",
                        "Fecha terminación": "2024-12-31",
                        "Valor_garantia": "10000"
                    }
                }
            }
        }),
        hallazgos=False
    )
    db_session.add(poliza)
    await db_session.flush()

    # 7. Create TablaMadre entry
    tabla_madre = TablaMadre(
        consecutivo_contrato="TEST-CONTRACT-001",
        id_documento_contrato=1001,
        id_documento_otrosi=[1002],
        id_documento_poliza=[1003],
        done=False,
        query=1
    )
    db_session.add(tabla_madre)
    await db_session.flush()

    # 8. Create OtrosiTablaMadre and PolizaTablaMadre entries
    otrosi_tabla_madre = OtrosiTablaMadre(id_documento=1002, consecutivo_contrato="TEST-CONTRACT-001")
    poliza_tabla_madre = PolizaTablaMadre(id_documento=1003, consecutivo_contrato="TEST-CONTRACT-001")
    db_session.add_all([otrosi_tabla_madre, poliza_tabla_madre])

    # Commit all changes
    await db_session.commit()

    # Perform assertions to verify the data was inserted correctly
    result = await db_session.execute(select(Activacion).where(Activacion.id_lote == 101))
    assert result.scalar_one() is not None

    result = await db_session.execute(select(IndexTable).where(IndexTable.id_lote == 101))
    assert len(result.scalars().all()) == 3

    result = await db_session.execute(select(Documento).where(Documento.id_lote == 101))
    assert len(result.scalars().all()) == 3

    result = await db_session.execute(select(Contratos).where(Contratos.consecutivo_contrato == "TEST-CONTRACT-001"))
    assert result.scalar_one() is not None

    result = await db_session.execute(select(Otrosi).where(Otrosi.consecutivo_contrato == "TEST-CONTRACT-001"))
    assert result.scalar_one() is not None

    result = await db_session.execute(select(Poliza).where(Poliza.consecutivo_contrato == "TEST-CONTRACT-001"))
    assert result.scalar_one() is not None

    result = await db_session.execute(select(TablaMadre).where(TablaMadre.consecutivo_contrato == "TEST-CONTRACT-001"))
    assert result.scalar_one() is not None

    # You can add more specific assertions here to check the content of the inserted data

