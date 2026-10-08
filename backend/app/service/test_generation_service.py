
from app.llm.prompt_builder import (
    build_test_case_prompt,
    build_usability_prompt
)


def generate_test_cases(llm, story):

    prompt = build_test_case_prompt(story)
    result = llm.generate(prompt)

    return [
        {
            "story_key": story.issue_key,
            "story_title": story.summary,
            "summary": test_case["summary"],
            "test_case": test_case["description"],
            "priority": story.priority
        }
        for test_case in result.get("test_cases", [])
    ]


def generate_usability_tests(llm, story, test_cases):

    prompt = build_usability_prompt(story, test_cases)
    result = llm.generate(prompt)

    return [
        {
            "story_key": story.issue_key,
            "story_title": story.summary,
            "title": usability_test["title"],
            "description": usability_test["description"],
            "test_case_keys": usability_test["test_case_keys"],
            "priority": story.priority
        }
        for usability_test in result.get("usability_tests", [])
    ]


## Robot Framework integration is planned for a later development phase.
## The current implementation focuses on test case and usability test generation.