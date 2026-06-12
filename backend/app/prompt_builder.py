from app.domain.story import Story 


## Test case generation prompt
def build_test_case_prompt(story: Story) -> str:
    return f"""

            Generate test cases strictly based on the provided user story details.
            
            Issue Key: {story.issue_key}
            Summary: {story.summary}
            Description: {story.description}
            Priority: {story.priority}

            Generate detailed software TEST CASES including positive and negative scenarios.
            Each test case must be a clear and testable sentence.
            Return ONLY valid JSON in the following format:

            {{
            "test_cases": [
                "test case 1",
                "test case 2",
                "test case 3"
            ]
            }}
            IMPORTANT:
            Return ONLY raw JSON.
            Do not use markdown.
            Do not wrap in ``` or ```json.
            Do not add explanations.
            Do not wrap the response in code blocks.
            """

## Usability test generation prompt
def build_usability_prompt(story: Story, test_cases: list) -> str:

    test_cases_text = "\n".join(test_cases)

    return f"""
            Issue Key: {story.issue_key}
            Summary: {story.summary}
            Description: {story.description}
            Priority: {story.priority}

            TEST CASES:
            {test_cases_text}

            Generate USABILITY TESTS based on the above test cases.

            Focus on:
            - user experience
            - clarity
            - discoverability
            - error understanding

            Return as bullet list.
            """

## Robot Framework generation prompt
def build_robot_prompt(story: Story) -> str:
    return f"""
            Issue Key: {story.issue_key}
            Summary: {story.summary}
            Description: {story.description}
            Priority: {story.priority}

            Generate ROBOT FRAMEWORK test script.

            Use format:
            *** Test Cases ***
            Example Test
                Open Browser    http://example.com
            """