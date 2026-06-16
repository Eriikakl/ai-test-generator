import csv
from app.domain.story import Story


def read_stories(filepath: str):

    stories = []

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            issue_key = (row.get("Issue key") or "").strip()
            summary = (row.get("Summary") or "").strip()

            if not issue_key or not summary:
                continue

            stories.append(
                Story(
                issue_key=issue_key,
                summary=summary,
                description=(row.get("Description") or "").strip(),
                priority=(row.get("Priority") or "Medium").strip(),
                status=(row.get("Status") or "To Do").strip()
                )
            )

    return stories