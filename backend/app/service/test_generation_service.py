from app.csv_reader import read_stories

from app.csv_writer import (
    write_test_cases,
    write_usability_tests,
    write_robot_file
)

from app.llm import LLMService

from app.prompt_builder import (
    build_test_case_prompt,
    build_usability_prompt,
    build_robot_prompt
)


def generate_test_cases(llm, story):

    prompt = build_test_case_prompt(story)
    result = llm.generate(prompt)

    return [
        {
            "story_key": story.issue_key,
            "story_title": story.summary,
            "test_case": test_case,
            "priority": story.priority
        }
        for test_case in result.get("test_cases", [])
    ]


def generate_usability_tests(llm, story, test_cases):

    test_cases_text = "\n".join(test_cases)
    prompt = build_usability_prompt(story, test_cases_text)
    result = llm.generate(prompt)

    return [
        {
            "story_key": story.issue_key,
            "story_title": story.summary,
            "usability_test": usability_test,
            "priority": story.priority
        }
        for usability_test in result.get("usability_tests", [])
    ]


def generate_robot_test(llm, story):

    prompt = build_robot_prompt(story)
    result = llm.generate(prompt)

    return result.get("robot_framework", "")


def run():
    
    llm = LLMService()
    stories = read_stories("stories/user_stories.csv")

    test_case_rows = []
    usability_rows = []
    robot_tests = []

    for story in stories:

        # Test cases

        test_case_rows_result = generate_test_cases(llm, story)

        test_case_rows.extend(test_case_rows_result)

        # Usability tests

        test_case_texts = [t["test_case"] for t in test_case_rows_result]
        usability_rows.extend(
            generate_usability_tests(llm, story, test_case_texts)
        )

        # Robot Framework
        robot_tests.append(
            generate_robot_test(llm, story)
        )


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