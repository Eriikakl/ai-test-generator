from dataclasses import dataclass

@dataclass
class Story:
    issue_key: str
    summary: str
    description: str
    priority: str
    status: str | None = None