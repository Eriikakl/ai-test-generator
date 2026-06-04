import csv


def write_test_cases(filepath: str, rows):

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "story_key",
                "story_title",
                "test_case",
                "priority"
            ]
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def write_usability_tests(filepath: str, rows):

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "story_key",
                "story_title",
                "usability_test",
                "priority"
            ]
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def write_robot_file(filepath: str, robot_tests):

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("*** Test Cases ***\n\n")

        for robot_test in robot_tests:
            file.write(robot_test)
            file.write("\n\n")