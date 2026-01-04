# services/ai_client.py
import os
import google.genai as genai


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        self.client=genai.Client(api_key=api_key)
        self.model = "models/gemini-2.5-flash-lite"

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        if not response or not response.text:
            raise RuntimeError("empty response from Gemini")
        return response.text.strip()
