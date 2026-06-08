from app.csv_reader import read_stories

from app.csv_writer import (
    write_test_cases,
    write_usability_tests,
    write_robot_file
)

from app.llm import LLMService


llm = LLMService()


def run():

    stories = read_stories("stories/user_stories.csv")

    test_case_rows = []
    usability_rows = []
    robot_tests = []

    for story in stories:

        prompt = f"""
        Key: {story['Issue key']}
        Summary: {story['summary']}
        Description: {story['description']}
        Priority: {story['priority']}
        """

        result = llm.generate(prompt)

        for test_case in result["test_cases"]:

            test_case_rows.append({
                "story_key": story["Issue key"],
                "story_title": story["summary"],
                "test_case": test_case,
                "priority": story["priority"]
            })

        for usability_test in result["usability_tests"]:

            usability_rows.append({
                "story_key": story["Issue key"],
                "story_title": story["summary"],
                "usability_test": usability_test,
                "priority": story["priority"]
            })

        robot_tests.append(result["robot_framework"])

    write_test_cases(
        "output/test_cases.csv",
        test_case_rows
    )

    write_usability_tests(
        "output/usability_tests.csv",
        usability_rows
    )

    write_robot_file(
        "output/generated_tests.robot",
        robot_tests
    )

    print("Files generated successfully")


if __name__ == "__main__":
    run()