# app/tests/test_excel_export.py
import pytest
from app.templates.excel_export import create_excel_report
import os
import json


@pytest.mark.asyncio
async def test_create_excel_report():
    # Sample JSON data
    json_data = {
        "contrato": {
            "info_general": {
                "Consecutivo Contrato": "TEST-CONTRACT-001",
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
            },
            "clausulas": {
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
            "amparos": {
                "output": {
                    "Checklist de Pólizas": {
                        "¿Tiene Garantía para buen manejo de anticipo?": {
                            "Existe la garantía": "Si",
                            "Descripción": ["Guarantee details..."]
                        }
                    }
                }
            }
        },
        "otrosi": [
            {
                "numero_otrosi": "1",
                "info_general": {
                    "Nit tercero": "987654321",
                    "Nombre del Tercero": "Test Company B",
                    "Fecha firma otrosi": "2024-06-01"
                },
                "modificaciones": {
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
                }
            }
        ],
        "poliza": [
            {
                "numero_poliza": "POLICY-12345",
                "info_general": {
                    "Nombre de tomador": "Test Company A",
                    "Nombre de beneficiado": "Test Company B",
                    "Objeto de la póliza": "Insurance coverage for...",
                    "Valor total a pagar": "5000",
                    "Valor total asegurado": "200000",
                    "Fecha de pago": "2024-01-15"
                },
                "amparos": {
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
                },
                "hallazgos": False
            }
        ],
        "hallazgos": [
            {
                "output": {
                    "0": {
                        "Garantía para buen manejo de anticipo": {
                            "Existe en lista del contrato": True,
                            "Existe en documento póliza": False,
                            "Descripción": "Hallazgo - existe sólo en el contrato. Revisar póliza"
                        }
                    }
                }
            }
        ]
    }

    output_path = "test_report.xlsx"
    create_excel_report(json_data, output_path)

    assert os.path.exists(output_path)

    # Clean up
    os.remove(output_path)
