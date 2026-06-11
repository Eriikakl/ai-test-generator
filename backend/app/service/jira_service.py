import requests
from app.domain.story import Story

def extract_text(adf):
    if not adf:
        return ""

    try:
        content = adf.get("content", [])
        texts = []

        for block in content:
            for inner in block.get("content", []):
                if inner.get("type") == "text":
                    texts.append(inner.get("text", ""))

        return " ".join(texts)

    except Exception:
        return ""

class JiraService:

    def __init__(self, base_url: str, email: str, api_token: str, project_key: str):
        self.base_url = base_url.rstrip("/")
        self.project_key = project_key

        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    ## get story from jira
    def get_story(self, issue_key: str) -> Story:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        fields = data["fields"]

        return Story(
            issue_key=data["key"],
            summary=fields.get("summary", ""),
            description=extract_text(fields.get("description")),
            priority=(fields.get("priority") or {}).get("name", "Medium"),
            status=(fields.get("status") or {}).get("name", "To Do")
        )

    ## create test case
    def create_test_case(self, summary: str, description: str):
        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "issuetype": {
                    "name": "Task"
                }
            }
        }

        response = requests.post(
            url,
            json=payload,
            auth=self.auth,
            headers=self.headers
        )

        response.raise_for_status()
        return response.json()

    ## push results to jira
    def push_test_cases(self, issue_key: str, test_cases):

        print(f"\n Pushing test cases for {issue_key}")

        created = []

        for tc in test_cases:
            issue = self.create_test_case(
                summary=f"[TEST] {tc['test_case']}",
                description=f"""
                Generated from story: {issue_key}

                Test case:
                {tc['test_case']}

                Priority: {tc['priority']}
                """
            )
            created.append(issue["key"])
            print("Created:", issue["key"])

        print("\nDONE")
        return created