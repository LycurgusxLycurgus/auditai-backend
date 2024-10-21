# app/queries.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_json_final(consecutivo_contrato: str, db: AsyncSession):
    query = text("""
    WITH contratos_info AS (
        SELECT m.consecutivo_contrato, c.json_contratos_info_general, c.json_contratos_clausulas, c.json_contratos_amparos
        FROM tabla_madre m
        JOIN contratos c ON m.id_documento_contrato = c.id_documento
        WHERE m.consecutivo_contrato = :consecutivo_contrato AND m.done = FALSE
    ),
    otrosi_info AS (
        SELECT o.numero_otrosi, o.json_otrosi_info_general, o.json_otrosi_modificaciones
        FROM otrosi o
        JOIN tabla_madre m ON o.consecutivo_contrato = m.consecutivo_contrato
        WHERE m.consecutivo_contrato = :consecutivo_contrato
    ),
    poliza_info AS (
        SELECT p.numero_poliza, p.json_poliza_info_general, p.json_poliza_amparos, p.hallazgos
        FROM poliza p
        JOIN tabla_madre m ON p.consecutivo_contrato = m.consecutivo_contrato
        WHERE m.consecutivo_contrato = :consecutivo_contrato
    )
    SELECT json_build_object(
        'contrato', json_build_object(
            'info_general', ci.json_contratos_info_general,
            'clausulas', ci.json_contratos_clausulas,
            'amparos', ci.json_contratos_amparos
        ),
        'otrosi', json_agg(json_build_object(
            'numero_otrosi', oi.numero_otrosi,
            'info_general', oi.json_otrosi_info_general,
            'modificaciones', oi.json_otrosi_modificaciones
        )) FILTER (WHERE oi.numero_otrosi IS NOT NULL),
        'poliza', json_agg(json_build_object(
            'numero_poliza', pi.numero_poliza,
            'info_general', pi.json_poliza_info_general,
            'amparos', pi.json_poliza_amparos,
            'hallazgos', pi.hallazgos
        )) FILTER (WHERE pi.numero_poliza IS NOT NULL)
    ) AS json_final
    FROM contratos_info ci
    LEFT JOIN otrosi_info oi ON TRUE
    LEFT JOIN poliza_info pi ON TRUE
    GROUP BY ci.consecutivo_contrato, ci.json_contratos_info_general, ci.json_contratos_clausulas, ci.json_contratos_amparos
    """)
    result = await db.execute(query, {"consecutivo_contrato": consecutivo_contrato})
    json_final = result.scalar()
    return json_final
