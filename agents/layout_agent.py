import json
import re
from services.ai_client import GeminiClient


class LayoutAgent:
    """
    Decides visual layout rules for placing text on an image.
    Does NOT render anything.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, headline: str, tone: str) -> dict:
        prompt = f"""
You are a creative director designing ad visuals.

Given:
Headline text: "{headline}"
Brand tone: "{tone}"

Decide layout rules for placing this headline on a product image.

OUTPUT RULES:
- Return VALID JSON ONLY
- No markdown
- No explanations
- Use ONLY the allowed values

Allowed values:
text_position: top_center | center | bottom_center
font_weight: light | regular | bold
background_style: none | solid_strip | gradient_strip
text_color: valid hex color
safe_margin_ratio: number between 0.05 and 0.15

Return JSON with EXACTLY:
- text_position
- font_weight
- background_style
- text_color
- safe_margin_ratio
"""

        raw_response = self.client.generate(prompt)
        return self._safe_json_parse(raw_response)

    def _safe_json_parse(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in Gemini response")

        return json.loads(match.group())
