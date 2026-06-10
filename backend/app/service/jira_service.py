from app.domain.story import Story

class JiraService:

    def __init__(self, client=None):
        self.client = client

    def get_story(self, issue_key: str):
        ## Mock versio
        return Story(
            issue_key=issue_key,
            summary="User can change password",
            description="As a user I want to change password",
            priority="High",
            status="To Do"
        )

    def push_results(self, issue_key: str, test_cases, usability_tests):
        print(f"\n=== PUSHING TO JIRA {issue_key} ===")

        print("\nTEST CASES:")
        for tc in test_cases:
            print("-", tc["test_case"])

        print("\nUSABILITY TESTS:")
        for ut in usability_tests:
            print("-", ut["usability_test"])