import csv

def read_stories(filepath: str):

    stories = []

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stories.append(row)

    return stories