from fastapi import FastAPI
from pydantic import BaseModel
from app.llm import LLMService

app = FastAPI()
llm = LLMService()

class Story(BaseModel):
    text: str

@app.post("/generate")
def generate(story: Story):
    return llm.generate(story.text)