# app/tests/test_queries.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Activacion, IndexTable, Documento, Contratos, Otrosi, Poliza, TablaMadre
from app.queries import get_json_final
from datetime import date


@pytest.mark.asyncio
async def test_get_json_final(db_session: AsyncSession):
    # Insert test data
    activacion = Activacion(
        usuario_activador="test_user",
        fecha_activacion=date.today(),
        numero_archivos=3
    )
    db_session.add(activacion)
    await db_session.commit()

    index_contrato = IndexTable(
        id_lote=activacion.id_lote,
        titulo_documento="TEST-CONTRACT-001.pdf",
        ocr=False,
        tipo_documento="contrato",
        trasladado_descargados=True,
        url_descargados="/path/to/contract.pdf",
        usuario_dueno="test_user",
        supervisado=True
    )
    db_session.add(index_contrato)
    await db_session.commit()

    documento = Documento(
        id_documento=index_contrato.id_documento,
        id_lote=activacion.id_lote,
        contenido="This is the content of the test contract."
    )
    db_session.add(documento)
    await db_session.commit()

    contratos = Contratos(
        id_documento=index_contrato.id_documento,
        id_lote=activacion.id_lote,
        consecutivo_contrato="TEST-CONTRACT-001",
        programa_mitigacion="Test Mitigation Program",
        json_contratos_info_general={
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
        },
        json_contratos_clausulas={
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
        },
        json_contratos_amparos={
            "output": {
                "Checklist de Pólizas": {
                    "¿Tiene Garantía para buen manejo de anticipo?": {
                        "Existe la garantía": "Si",
                        "Descripción": ["Guarantee details..."]
                    }
                }
            }
        }
    }
    db_session.add(contratos)
    await db_session.commit()

    tabla_madre = TablaMadre(
        consecutivo_contrato="TEST-CONTRACT-001",
        id_documento_contrato=contratos.id_documento,
        done=False,
        query=1
    )
    db_session.add(tabla_madre)
    await db_session.commit()

    # Execute the query
    json_final = await get_json_final("TEST-CONTRACT-001", db_session)
    assert json_final is not None
    assert "contrato" in json_final
    assert "otrosi" in json_final
    assert "poliza" in json_final
