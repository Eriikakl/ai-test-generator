from app.llm import LLMService
from app.service.jira_service import JiraService
from app.generate_from_csv import generate_test_cases, generate_usability_tests

llm = LLMService()
jira = JiraService()

def run(issue_key: str):

    story = jira.get_story(issue_key)

    test_cases = generate_test_cases(llm, story)

    usability_tests = generate_usability_tests(
        llm,
        story,
        [t["test_case"] for t in test_cases]
    )

    jira.push_results(issue_key, test_cases, usability_tests)


if __name__ == "__main__":
    run("ABC-1")