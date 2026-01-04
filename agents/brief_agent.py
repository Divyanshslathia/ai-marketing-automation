import json
import re
from services.ai_client import GeminiClient

class BriefAgent:
    """
    Converts raw user inputs into a structured campaign brief.
    Output must be JSON-compatible dict.
    """
    def __init__(self):
        self.client = GeminiClient()

    def run(self, inputs: dict) -> dict:
        """
        inputs expected:
        {
            "product_name": str,
            "features": list[str],
            "tone": str
        }
        """

        prompt = f"""
You are a senior digital marketing strategist.

Convert the following inputs into a HIGH-LEVEL campaign brief.
This brief will be used by other AI agents.

INPUTS:
Product name: {inputs["product_name"]}
Key features: {inputs["features"]}
Brand tone/style: {inputs["tone"]}

OUTPUT RULES:
- Return VALID JSON ONLY
- Keep values concise (1–2 sentences max per field)
- Do NOT include nested objects except brand_voice
- Do NOT include ad formats, content ideas, or tactics

Return JSON with EXACTLY these keys:
- campaign_goal (string)
- target_audience (string)
- brand_voice (object with tone and style)
- key_value_props (array of strings)
- platform_notes (object with linkedin, instagram, facebook as strings)
"""

        raw_response = self.client.generate(prompt)

        return self._safe_json_parse(raw_response)

    def _safe_json_parse(self, text: str) -> dict:
        """
        Extracts and parses JSON safely from model output.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in Gemini response")

        return json.loads(match.group())