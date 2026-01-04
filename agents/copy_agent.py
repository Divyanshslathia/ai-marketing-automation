import json
import re
from services.ai_client import GeminiClient


class CopyAgent:
    """
    Generates marketing copy (headlines + captions)
    based on a structured campaign brief.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, brief: dict) -> dict:
        prompt = f"""
You are a senior performance copywriter.

Using the campaign brief below, generate marketing copy.

CAMPAIGN BRIEF:
{brief}

OUTPUT RULES:
- Return VALID JSON ONLY
- No markdown
- No explanations
- Headlines must be MAX 6 words
- Captions must be concise and platform-appropriate

Return JSON with EXACTLY:
- headlines: array of exactly 3 short headline options
- captions:
    - linkedin: array of exactly 2 professional captions
    - instagram: array of exactly 2 casual captions (emojis allowed)
    - facebook: array of exactly 2 friendly captions
"""

        raw_response = self.client.generate(prompt)
        
        result = self._safe_json_parse(raw_response)

        result["headlines"] = self._enforce_headline_length(
            result.get("headlines", [])
        )

        return result

    def _safe_json_parse(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in Gemini response")

        return json.loads(match.group())
    def _enforce_headline_length(self, headlines: list[str], max_words: int = 6) -> list[str]:
        cleaned = []
        for h in headlines:
            words = h.replace(":", "").split()
            cleaned.append(" ".join(words[:max_words]))
        return cleaned

