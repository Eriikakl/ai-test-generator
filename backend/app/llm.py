from app.mock_llm import MockLLM

class LLMService:
    def __init__(self):
        self.engine = MockLLM()

    def generate(self, prompt: str) -> dict:
        return self.engine.generate(prompt)