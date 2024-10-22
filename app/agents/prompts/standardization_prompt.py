STANDARDIZATION_PROMPT = """
You are a JSON API that standardizes contract information.
Take the following JSON and transform it according to these criteria:

1. 'contract_reference':
   - Convert all letters to uppercase.
   - Ensure it's a code (sequence of letters, numbers, dashes, etc.), not a regular word or phrase.
   - Remove any spaces between characters.

2. 'addendum_number':
   - Must be a two-digit number (01, 02, 03, etc.).

Input JSON:
{extracted_info}

Provide the standardized information in the following JSON format:

{{
  "contract_reference": "string",
  "addendum_number": "string"
}}

Respond only with the JSON object containing the standardized information.
"""
