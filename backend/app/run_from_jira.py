from app.llm import LLMService
from app.service.jira_service import JiraService

from app.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
    GEMINI_API_KEY
)

from app.service.test_generation_service import (
    generate_test_cases
)

llm = LLMService(use_mock=True) ## use_mock=True (MockLLM mode), GEMINI_API_KEY (Gemini mode)

jira = JiraService(
    base_url=JIRA_BASE_URL,
    email=JIRA_EMAIL,
    api_token=JIRA_API_TOKEN,
    project_key=JIRA_PROJECT_KEY
)


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
    