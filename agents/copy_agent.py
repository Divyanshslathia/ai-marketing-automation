import json
import re
from services.ai_client import GeminiClient

class CopyAgent:
    def __init__(self):
        self.client = GeminiClient()

    def run(self, inputs: dict) -> dict:
        # Combined Prompt: Strategy + Creative
        prompt = f"""
        You are a Marketing Strategist and Copywriter.
        Product: {inputs['product_name']}
        Features: {inputs['features']}
        Tone: {inputs['tone']}

        Task: Create a campaign brief and marketing copy in ONE JSON object.
        
        OUTPUT JSON STRUCTURE:
        {{
            "brief": {{
                "target_audience": "string",
                "key_value_prop": "string"
            }},
            "headlines": ["3 short options"],
            "captions": {{
                "linkedin": ["2 options"],
                "instagram": ["2 options"],
                "facebook": ["2 options"]
            }}
        }}
        """
        raw_response = self.client.generate(prompt)
        return self._safe_json_parse(raw_response)

    def _safe_json_parse(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group()) if match else {}