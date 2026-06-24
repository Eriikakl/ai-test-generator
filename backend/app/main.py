from fastapi import FastAPI
from app.llm import LLMService
from app.domain.story import Story
## from app.config import GEMINI_API_KEY
from fastapi.middleware.cors import CORSMiddleware

from app.service.test_generation_service import (
    generate_test_cases,
    generate_usability_tests
)

app = FastAPI()
llm = LLMService(use_mock=True) ## GEMINI_API_KEY (Gemini mode)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(story: Story):
    test_cases = generate_test_cases(llm, story)

    test_case_texts = [t["test_case"] for t in test_cases]

    usability_tests = generate_usability_tests(
        llm,
        story,
        test_case_texts
    )

    return {
        "test_cases": test_cases,
        "usability_tests": usability_tests
    }