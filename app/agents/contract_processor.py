import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .prompts.extraction_prompt import EXTRACTION_PROMPT
from .prompts.standardization_prompt import STANDARDIZATION_PROMPT
import json

class ContractProcessor:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.3,
            model_name="llama-3.1-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_kwargs={"response_format": {"type": "json_object"}}  # Move response_format here
        )
        
        # Create extraction chain
        extraction_prompt = PromptTemplate(
            input_variables=["addendum_text"],
            template=EXTRACTION_PROMPT
        )
        self.extraction_chain = extraction_prompt | self.llm | StrOutputParser()

        # Create standardization chain
        standardization_prompt = PromptTemplate(
            input_variables=["extracted_info"],
            template=STANDARDIZATION_PROMPT
        )
        self.standardization_chain = standardization_prompt | self.llm | StrOutputParser()

    def process_addendum(self, addendum_text):
        # Run extraction chain
        extracted_info = self.extraction_chain.invoke({"addendum_text": addendum_text})
        
        # Run standardization chain
        standardized_json = self.standardization_chain.invoke({"extracted_info": extracted_info})

        # Estimate tokens (this is a rough estimation)
        estimated_tokens = len(addendum_text) + len(extracted_info) + len(standardized_json)

        return json.loads(standardized_json), estimated_tokens

# Usage example
if __name__ == "__main__":
    processor = ContractProcessor()
    addendum_text = "Your addendum text here..."
    result, tokens = processor.process_addendum(addendum_text)
    print(f"Standardized JSON: {result}")
    print(f"Estimated tokens used: {tokens}")
