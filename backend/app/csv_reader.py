import csv

def read_stories(filepath: str):

    stories = []

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stories.append({
                "issue_key": row.get("Issue key"),
                "summary": row.get("Summary"),
                "description": row.get("Description"),
                "priority": row.get("Priority"),
                "status": row.get("Status")
            })

    return stories