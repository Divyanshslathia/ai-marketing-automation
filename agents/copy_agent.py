import json
import re
from services.ai_client import GeminiClient
from utils.logger import log


class CopyAgent:
    def __init__(self):
        self.client = GeminiClient()

    def run(self, inputs: dict) -> dict:
        log(
            "CopyAgent",
            f"Received inputs: product={inputs.get('product_name')}, tone={inputs.get('tone')}"
        )

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

        result = self._safe_json_parse(raw_response)

        # High-signal agent "thinking" logs
        log(
            "CopyAgent",
            f"Generated {len(result.get('headlines', []))} headlines"
        )
        log(
            "CopyAgent",
            f"Generated captions for platforms: {list(result.get('captions', {}).keys())}"
        )

        return result

    def _safe_json_parse(self, text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            log("CopyAgent", "Failed to parse JSON from model response")
            return {}

        return json.loads(match.group())
