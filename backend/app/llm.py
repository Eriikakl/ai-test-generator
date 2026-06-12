## from app.mock_llm import MockLLM
from google import genai
import json

class LLMService:
    def __init__(self, api_key: str):
      ##  self.engine = MockLLM()
      self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> dict:
        response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )

        return json.loads(response.text)