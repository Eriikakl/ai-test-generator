from app.llm.mock_llm import MockLLM
from google import genai
import json

class LLMService:
    def __init__(self, api_key: str = None, use_mock: bool = False):

      self.use_mock = use_mock 

      if use_mock:
         self.engine = MockLLM()
      else:
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> dict:
        
        if self.use_mock: 
           return self.engine.generate(prompt)
        
        response = self.client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
        )

        return json.loads(response.text)