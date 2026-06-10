from dataclasses import dataclass

@dataclass
class Story:
    issue_key: str
    summary: str
    description: str = ""
    priority: str = "Medium"
    status: str | None = None

    def __post_init__(self):
        if not self.issue_key:
            raise ValueError("issue_key is required")

        if not self.summary:
            raise ValueError("summary is required")