# app/tests/insert_data.py
import asyncio
import json
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models import Activacion, IndexTable, Documento, Contratos, Otrosi, Poliza, TablaMadre, OtrosiTablaMadre, PolizaTablaMadre

# Use the same database URL configuration as in test_connection.py
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres.ppdacijqpyzzitxhkxgo:uEDEVyUPzSF66nz9@aws-0-us-east-1.pooler.supabase.com:5432/postgres")

# Ensure the URL uses the asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def insert_data():
    async with AsyncSessionLocal() as session:
        # Insert Activacion
        activacion = Activacion(
            id_lote=101,
            usuario_activador="test_user",
            fecha_activacion=date(2024, 10, 26),
            numero_archivos=3
        )
        session.add(activacion)
        await session.flush()

        # Insert IndexTable entries
        index_entries = [
            IndexTable(id_documento=1001, id_lote=101, titulo_documento="TEST-CONTRACT-001.pdf", ocr=False, tipo_documento="contrato", trasladado_descargados=True, url_descargados="/path/to/contract.pdf", usuario_dueno="test_user", supervisado=True),
            IndexTable(id_documento=1002, id_lote=101, titulo_documento="TEST-CONTRACT-001-otrosi1.pdf", ocr=False, tipo_documento="otrosi", trasladado_descargados=True, url_descargados="/path/to/otrosi1.pdf", usuario_dueno="test_user", supervisado=True),
            IndexTable(id_documento=1003, id_lote=101, titulo_documento="TEST-CONTRACT-001-poliza.pdf", ocr=True, tipo_documento="poliza", trasladado_descargados=True, url_descargados="/path/to/poliza.pdf", usuario_dueno="test_user", supervisado=True)
        ]
        session.add_all(index_entries)
        await session.flush()

        # Insert Documento entries
        documento_entries = [
            Documento(id_documento=1001, id_lote=101, contenido="This is the content of the test contract."),
            Documento(id_documento=1002, id_lote=101, contenido="This is the content of the test otrosi."),
            Documento(id_documento=1003, id_lote=101, contenido="This is the content of the test poliza.")
        ]
        session.add_all(documento_entries)
        await session.flush()

        # Insert Contratos entry
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
        session.add(contrato)
        await session.flush()

        # Insert Otrosi entry
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
        session.add(otrosi)
        await session.flush()

        # Insert Poliza entry
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
        session.add(poliza)
        await session.flush()

        # Insert TablaMadre entry
        tabla_madre = TablaMadre(
            consecutivo_contrato="TEST-CONTRACT-001",
            id_documento_contrato=1001,
            id_documento_otrosi=[1002],
            id_documento_poliza=[1003],
            done=False,
            query=1
        )
        session.add(tabla_madre)
        await session.flush()

        # Insert OtrosiTablaMadre and PolizaTablaMadre entries
        otrosi_tabla_madre = OtrosiTablaMadre(id_documento=1002, consecutivo_contrato="TEST-CONTRACT-001")
        poliza_tabla_madre = PolizaTablaMadre(id_documento=1003, consecutivo_contrato="TEST-CONTRACT-001")
        session.add_all([otrosi_tabla_madre, poliza_tabla_madre])

        # Commit all changes
        await session.commit()

        print("Data inserted successfully!")

if __name__ == "__main__":
    asyncio.run(insert_data())