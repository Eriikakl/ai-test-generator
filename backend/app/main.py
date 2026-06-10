from fastapi import FastAPI
from app.llm import LLMService
from app.domain.story import Story

from app.generate_from_csv import (
    generate_test_cases,
    generate_usability_tests
)

app = FastAPI()
llm = LLMService()

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