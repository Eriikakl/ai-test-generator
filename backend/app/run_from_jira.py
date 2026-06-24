from app.llm import LLMService
from app.services import get_jira_service

from app.service.test_generation_service import (
    generate_test_cases
)

llm = LLMService(use_mock=True) ## use_mock=True (MockLLM mode), GEMINI_API_KEY (Gemini mode)

jira = get_jira_service()


def run(issue_key: str):

    story = jira.get_story(issue_key)

    test_cases = generate_test_cases(llm, story)

    jira.push_test_cases(story, test_cases)

    test_cases = jira.get_test_cases(issue_key)

    print("\n=== TEST CASES ===\n")

    for tc in test_cases:
        print("-", tc["fields"]["summary"])


if __name__ == "__main__":
    run("ABC-1")
    