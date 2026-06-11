from app.llm import LLMService
from app.service.jira_service import JiraService

from app.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY
)

from app.generate_from_csv import (
    generate_test_cases
)

llm = LLMService()

jira = JiraService(
    base_url=JIRA_BASE_URL,
    email=JIRA_EMAIL,
    api_token=JIRA_API_TOKEN,
    project_key=JIRA_PROJECT_KEY
)


def run(issue_key: str):

    story = jira.get_story(issue_key)

    test_cases = generate_test_cases(llm, story)

    jira.push_test_cases(issue_key, test_cases)


if __name__ == "__main__":
    run("ABC-1")
    