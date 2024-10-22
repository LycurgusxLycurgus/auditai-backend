import os
import sys
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path to import the necessary modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Otrosi, ChainOtrosi
from app.agents.contract_processor import ContractProcessor

# Load environment variables
load_dotenv()

# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres.ppdacijqpyzzitxhkxgo:uEDEVyUPzSF66nz9@aws-0-us-east-1.pooler.supabase.com:5432/postgres")

# Ensure the URL uses the asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def test_otrosi_chain_insertion():
    # Initialize the ContractProcessor
    processor = ContractProcessor()

    # Hypothetical addendum text (you can use the same text from test_contract_processor.py)
    addendum_text = """
    ADDENDUM TO CONTRACT

    ## ADDENDUM
    ---
    **Contrato Número:** CT-2023-0456  
    **Fecha de Emisión:** 15 de Marzo de 2023  

    **Parte A:** Empresa XYZ S.A.  
    **Parte B:** Proveedor ABC Ltda.  

    **Objeto del Contrato:**  
    El presente contrato tiene por objeto la prestación de servicios de consultoría tecnológica por parte de Proveedor ABC Ltda. a Empresa XYZ S.A.

    **Otrosí Número:** 02  
    **Fecha de Otrosí:** 20 de Abril de 2023  

    **Modificaciones:**  
    En virtud de este otrosí, se amplía el alcance de los servicios para incluir soporte técnico adicional y capacitación al personal de Empresa XYZ S.A.

    **Duración:**  
    La duración del contrato se extiende hasta el 30 de Septiembre de 2023, con posibilidad de renovación previa evaluación de desempeño.

    **Firmas:**

    _________________________  
    **Representante de Empresa XYZ S.A.**

    _________________________  
    **Representante de Proveedor ABC Ltda.**
    ---
    """

    # Process the addendum
    result, total_tokens = processor.process_addendum(addendum_text)

    # Estimate input and output tokens (this is a rough estimation)
    tokens_input = len(addendum_text)
    tokens_output = len(json.dumps(result))

    async with AsyncSessionLocal() as session:
        # Update or insert Otrosi
        otrosi_stmt = select(Otrosi).where(
            Otrosi.consecutivo_contrato == result['contract_reference'],
            Otrosi.numero_otrosi == result['addendum_number']
        )
        existing_otrosi = await session.execute(otrosi_stmt)
        existing_otrosi = existing_otrosi.scalar_one_or_none()

        if existing_otrosi:
            existing_otrosi.numero_otrosi = result['addendum_number']
            existing_otrosi.consecutivo_contrato = result['contract_reference']
        else:
            new_otrosi = Otrosi(
                numero_otrosi=result['addendum_number'],
                consecutivo_contrato=result['contract_reference'],
                # Add other required fields with default values or None
                id_documento=None,
                id_lote=None,
                json_otrosi_info_general=None,
                json_otrosi_modificaciones=None
            )
            session.add(new_otrosi)
            await session.flush()
            existing_otrosi = new_otrosi

        # Insert ChainOtrosi
        chain_otrosi = ChainOtrosi(
            output_prompt_extractor=processor.extraction_chain.invoke({"addendum_text": addendum_text}),
            output_prompt_estandarizador=processor.standardization_chain.invoke({"extracted_info": json.dumps(result)}),
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            total_tokens=total_tokens,
            otrosi_id=existing_otrosi.id_documento
        )
        session.add(chain_otrosi)

        await session.commit()

    print("Data inserted successfully!")
    print(f"Otrosi: {result}")
    print(f"ChainOtrosi: Tokens - Input: {tokens_input}, Output: {tokens_output}, Total: {total_tokens}")

if __name__ == "__main__":
    asyncio.run(test_otrosi_chain_insertion())
