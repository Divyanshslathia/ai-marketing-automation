import os
import time
import random
import google.genai as genai
from google.genai.errors import ServerError, ClientError

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        # Switching to 1.5-flash which often has more stable free-tier limits
        self.model = "models/gemini-2.5-flash-lite" 

    def generate(self, prompt: str, retries: int = 3) -> str:
        for attempt in range(1, retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                if not response or not response.text:
                    raise RuntimeError("Empty response from Gemini")
                return response.text.strip()

            except ClientError as e:
                if "429" in str(e):
                    wait_time = 30 + random.uniform(0, 5)
                    print(f"Rate limit hit. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue 
                raise e
            except ServerError as e:
                if attempt == retries: raise
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)