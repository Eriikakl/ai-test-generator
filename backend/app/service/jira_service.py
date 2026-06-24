import requests
from app.domain.story import Story

## extracted text from Jira ADF description.
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

## built Jira compatible description
def build_description(issue_key: str, story: Story):

    text = f"""Generated from story: {issue_key} {story.summary}"""

    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }

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
    def create_test_case(self, summary: str, description: dict):
        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
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
    def push_test_cases(self, story: Story, test_cases):

        print(f"\n Pushing test cases for {story.issue_key}")

        created = []

        for tc in test_cases:
            issue = self.create_test_case(
                summary=f"[TEST] {tc['test_case']}",
                description=build_description(story.issue_key, story)
            )

            test_key = issue["key"]
            tc["test_key"] = test_key
            
            created.append(tc)

            print("Created:", test_key)
            self.link_issues(story.issue_key, test_key)

            print(f"Linked {story.issue_key} -> {test_key}")
        print("\nDONE")
        return created
    
    ## created Jira issue link between user story and test case
    def link_issues(self, story_key: str, test_key: str):

            url = f"{self.base_url}/rest/api/3/issueLink"

            payload = {
                "type": {
                    "name": "Relates"
                },
                "inwardIssue": {
                    "key": test_key
                },
                "outwardIssue": {
                    "key": story_key
                }
            }

            response = requests.post(
                url,
                json=payload,
                auth=self.auth,
                headers=self.headers
            )

            response.raise_for_status()

    ## get test cases from Jira
    def get_test_cases(self, issue_key: str):
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

        params = {
            "fields": "issuelinks"
        }

        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()

        data = response.json()

        links = data["fields"].get("issuelinks", [])

        test_case_keys = []

        for link in links:
            if "outwardIssue" in link:
                test_case_keys.append(link["outwardIssue"]["key"])
            if "inwardIssue" in link:
                test_case_keys.append(link["inwardIssue"]["key"])

        issues = []

        for key in test_case_keys:
            url = f"{self.base_url}/rest/api/3/issue/{key}"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            issues.append(response.json())

        return issues
