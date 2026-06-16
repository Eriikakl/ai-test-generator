from app.csv_pipeline.csv_reader import read_stories

from app.csv_pipeline.csv_writer import (
    write_test_cases,
    write_usability_tests,
    write_robot_file
)

from app.llm import LLMService
from app.llm import LLMService
from app.service.test_generation_service import (
    generate_test_cases,
    generate_usability_tests,
    generate_robot_test
)

def run():
    
    llm = LLMService(use_mock=True)
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