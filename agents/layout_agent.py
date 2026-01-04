import json
import re
from services.ai_client import GeminiClient
from utils.logger import log


class LayoutAgent:
    """
    Decides visual layout rules for placing text on an image.
    Does NOT render anything.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, headline: str, tone: str) -> dict:
        log(
            "LayoutAgent",
            f"Deciding layout for headline length={len(headline)} and tone='{tone}'"
        )

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
        layout = self._safe_json_parse(raw_response)

        log("LayoutAgent", f"Selected layout: {layout}")

        return layout

    def _safe_json_parse(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            log("LayoutAgent", "Failed to parse JSON from model response")
            raise ValueError("No JSON object found in Gemini response")

        return json.loads(match.group())
