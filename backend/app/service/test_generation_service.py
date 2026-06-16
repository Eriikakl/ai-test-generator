
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