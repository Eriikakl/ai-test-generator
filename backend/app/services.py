from app.service.jira_service import JiraService

from app.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
)

def get_jira_service():
    return JiraService(
        base_url=JIRA_BASE_URL,
        email=JIRA_EMAIL,
        api_token=JIRA_API_TOKEN,
        project_key=JIRA_PROJECT_KEY
    )