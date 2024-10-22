import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the Python path to import the ContractProcessor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.contract_processor import ContractProcessor

# Load environment variables
load_dotenv()

def test_contract_processor():
    # Hypothetical addendum text
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

    # Initialize the ContractProcessor
    processor = ContractProcessor()

    # Process the addendum
    result, tokens = processor.process_addendum(addendum_text)

    # Print the results
    print("Standardized JSON:")
    print(json.dumps(result, indent=2))
    print(f"\nEstimated tokens used: {tokens}")

    # Updated assertions to match the current implementation
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "contract_reference" in result, "Result should contain contract_reference"
    assert "addendum_number" in result, "Result should contain addendum_number"
    assert result["contract_reference"] == "CT-2023-0456", "Incorrect contract reference"
    assert result["addendum_number"] == "02", "Incorrect addendum number"

if __name__ == "__main__":
    test_contract_processor()
