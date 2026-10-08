from app.domain.story import Story 


## Test case generation prompt
def build_test_case_prompt(story: Story) -> str:
    return f"""

            Generate test cases strictly based on the provided user story details.
            
            Issue Key: {story.issue_key}
            Summary: {story.summary}
            Description: {story.description}
            Priority: {story.priority}

            Generate 3-5 detailed software TEST CASES including positive and negative scenarios.
            Each test case must be clear, testable, and cover a distinct scenario without duplication.
            Each test case MUST contain:
            - A short summary of maximum 100 characters
            - A detailed test case description

            Return ONLY valid JSON in the following format:

            {{
            "test_cases": [
                {{
                    "summary": "Short test case summary",
                    "description": "Detailed test case including preconditions, steps and expected results"
                }},
                {{
                    "summary": "Short test case summary",
                    "description": "Detailed test case including preconditions, steps and expected results"
                }}
            ]
            }}

            IMPORTANT:
            Do not use markdown.
            Do not add explanations.
            """

## Usability test generation prompt
def build_usability_prompt(story: Story, test_cases: list) -> str:

    test_cases_text = "\n".join(
        f"{tc['key']}: {tc['summary']}"
        for tc in test_cases
    )

    return f"""
    
            Issue Key: {story.issue_key}
            Summary: {story.summary}
            Description: {story.description}
            Priority: {story.priority}

            TEST CASES:
            {test_cases_text}

            Generate 1-3 high-value USABILITY TESTS based on the above test cases.
            Do not generate multiple usability tests that evaluate the same user experience.
            Prioritize the most important and relevant usability aspects.

            Focus on:
            - user experience
            - clarity
            - discoverability
            - error understanding

            Each usability test MUST contain:
            - A short and descriptive title of maximum 80 characters
            - A detailed description explaining what the user should do and what should be evaluated
            - The test case keys related to the usability test

            The title must be concise.
            Do not put instructions or long explanations in the title.
            Put the detailed task and evaluation criteria in the description.

            Return ONLY valid JSON in the following format:

            {{
                "usability_tests": [
                    {{
                        "title": "Short usability test title",
                        "description": "Detailed description of the usability test, including the task and what should be evaluated.",
                        "test_case_keys": ["TC-101", "TC-102"]
                    }},
                    {{
                        "title": "Short usability test title",
                        "description": "Detailed description of the usability test, including the task and what should be evaluated.",
                        "test_case_keys": ["TC-103"]
                    }}
                ]
            }}

            IMPORTANT:
            Do not use markdown.
            Do not add explanations.
            Only use test case keys provided in the TEST CASES.
            """

## Robot Framework generation prompt
## Robot Framework integration is planned for a later development phase.
## The current implementation focuses on test case and usability test generation.