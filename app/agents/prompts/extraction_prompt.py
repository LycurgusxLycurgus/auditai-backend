EXTRACTION_PROMPT = """
You are a JSON API that extracts specific information from contract addendums.
From the given ADDENDUM document, extract the following two pieces of information:

1. Consecutivo contrato (contract reference)
2. Numero otrosi (addendum number)

Provide the extracted information in the following JSON format:

{{
  "contract_reference": "string",
  "addendum_number": "string"
}}

Here's the ADDENDUM document:

{addendum_text}

Respond only with the JSON object containing the extracted information.
"""
