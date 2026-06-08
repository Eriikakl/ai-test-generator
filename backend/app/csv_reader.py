import csv
from app.domain.story import Story


def read_stories(filepath: str):

    stories = []

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stories.append(
                Story(
                issue_key=row.get("Issue key"),
                summary=row.get("Summary"),
                description=row.get("Description"),
                priority=row.get("Priority"),
                status=row.get("Status")
                )
            )

    return stories