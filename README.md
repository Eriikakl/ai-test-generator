# AI Test Generator

An AI-based test automation project that combines Jira integration with LLM-based test generation. Test cases are automatically generated from Jira user stories, created in Jira, and linked back to the original user stories.

The project can generate usability tests based on user stories and their related test cases. Usability tests can be reviewed and edited before they are pushed to Jira.

The project is designed to be extended with test script generation.

> **Note:** This English version was translated from Finnish with the help of AI and reviewed manually.


## Current status

- In development

Currently, the project consists of two different workflows.

Jira-based test case and usability test generation

- Fetches the user story from the Jira API

- Generates test cases using an LLM (Gemini)

- Creates Task issues in Jira from the test cases and links them to the original user story

- Fetches the test cases linked to the user story and generates usability tests based on them and the original user story

- Usability test generation can be started from the user interface or through a FastAPI endpoint, after which the tests can be reviewed, approved, and pushed to Jira

- Creates Jira Task issues from the approved usability tests and links them to the original user story

[View the current state of the project](docs/Results.md)

---

For development and testing, the project also includes a CSV-based generation workflow.

CSV-based test data generation:

- Reads user stories from a CSV file

- Uses the MockLLM component for test data generation

- Produces:

  ```
  - `test_cases.csv`

  - `usability_tests.csv`

  - `generated_tests.robot`
  ```

## Project structure

```text

backend/

├── app/
│   ├── csv_pipeline/
│       ├── csv_reader.py
│       ├── csv_writer.py
│       └── generate_from_csv.py
│
│   ├── domain/
│       └── story.py
│
│   ├── llm/
│       ├── llm_service.py
│       ├── mock_llm.py
│       └── prompt_builder.py
│
│   ├── service/
│       ├── jira_service.py
│       └── test_generation_service.py
│
│   ├── config.py
│   ├── main.py
│
├── stories/
│   └── user_stories.csv
│
├── output/
│   ├── test_cases.csv
│   ├── usability_tests.csv
│   └── generated_tests.robot

```

## Technologies

### Backend

- Python
- FastAPI
- Requests (Jira API)

### AI

- Google Gemini API
- MockLLM (Development and testing)

### Data

- Jira (test cases and usability tests)
- CSV (testing)
- JSON

### Frontend

- TypeScript
- React
- Vite
- CSS

## Jira

### User story format

```JSON

{
  "issue_key": "ABC-1",
  "summary": "User can login",
  "description": "As a user I want to login...",
  "priority": "High",
  "status": "To Do"
}

```

## Architecture

### Processing a single user story

```text
Jira User Story (ABC-1)
      ↓
JiraService (GET /issue)
      ↓
Story (domain model)
      ↓
Prompt Builder
      ↓
LLM Service (Gemini)
      ↓
Test Case Generation
      ↓
JiraService (POST /issue)
      ↓
JiraService (POST /issueLink)
```

### Usability test generation and review

```text
Jira User Story (ABC-1)
      ↓
JiraService (GET /issue)
      ↓
Linked Test Cases
      ↓
Prompt Builder
      ↓
LLM Service (Gemini)
      ↓
Usability Test Generation
      ↓
Frontend
      ↓
Human Review
      ↓
Approved Usability Tests
      ↓
JiraService (POST /issue)
      ↓
JiraService (POST /issueLink)
```

### Automatic Jira synchronization

```text
FastAPI
      ↓
Jira Sync
      ↓
JiraService (GET /search/jql)
      ↓
Story (domain model)
      ↓
Prompt Builder
      ↓
LLM Service (Gemini / MockLLM)
      ↓
Test Case Generation
      ↓
JiraService (POST /issue)
      ↓
JiraService (POST /issueLink)
```


## API

**Jira Webhook**

```http

POST /jira/webhook

```

- Prepared endpoint for Jira automation.

- Intended to automatically process new user stories.

---

**Jira Sync**

```http

POST /jira/sync

```

- Synchronizes unprocessed user stories from Jira.

- Automatically creates test cases for new user stories.

---

**Fetching test cases**

```http

GET /test-cases/{issue_key}

```

- Fetches the test cases linked to the user story based on the given issue key.

---

**Test case generation**

```http

POST /generate/test-cases/{issue_key}

```

- Fetches the user story from the Jira API based on the given issue key.

- Generates test cases based on the user story using an LLM.

- Creates Jira Task issues from the generated test cases.

- Links the test cases to the original user story.

---

**Usability test generation**

```http

POST /generate/usability-tests/{issue_key}

```

- Fetches the user story from the Jira API based on the given issue key.

- Fetches the test cases linked to the user story.

- Generates usability tests based on the user story and test cases using an LLM.

- Returns the generated usability tests to the user interface for review.

- The generated tests are not yet created in Jira at this stage.

---

**Sending usability tests to Jira**

```http

POST /push/usability-tests/{issue_key}

```

- Receives the usability tests reviewed in the user interface.

- Sends only the tests approved by the user to Jira.

- Creates Jira Task issues from the approved usability tests.

- Set the priority defined by the user for the test.

- Links the created usability tests to the original user story.

---

**Jira user story search**

```http

GET /jira/stories/search?q={query}&limit={limit}

```

- Searches for user stories in the Jira project based on a search term or issue key.

- Limits the search to Story-type issues only.

- Returns the issue keys and summaries of the found user stories as an API response.

- The user interface uses the endpoint for selecting a user story.

---

## Setup

### 1. Clone the repository

### 2. Create a virtual environment

```bash

python -m venv .venv

```

Activation:

```bash

. .venv/scripts/activate

```

### 3. Install dependencies /backend

```bash

pip install fastapi uvicorn requests python-dotenv google-genai

```

#### Jira workflow only:

```bash

pip install requests python-dotenv google-genai

```

---

### 4. Environment variables

An `.env` file has been created for securely using the Jira settings:

```env

JIRA_BASE_URL=https://your-domain.atlassian.net

JIRA_EMAIL=your.email@example.com

JIRA_API_TOKEN=your_api_token_here

JIRA_PROJECT_KEY=ABC

GEMINI_API_KEY=your_api_token_here

```

## Running

### Start FastAPI /backend

```bash

uvicorn app.main:app --reload

```

- When starting, the application begins automatic Jira synchronization.

- Synchronization runs in the background every minute.

---

### Start /frontend

```bash

npm install

npm run dev

```

---

## CSV

### User story format

```csv

Issue key,Summary,Description,Priority,Status

AUTH-3,User can edit profile,"As a user, I want to update my profile information",Medium,To Do

```

### Generated files

#### Test Cases

```csv

story_key,story_title,test_case,priority

AUTH-3,User can edit profile,User can update profile information successfully,Medium

AUTH-3,User can edit profile,Changes are saved and visible after refresh,Medium

AUTH-3,User can edit profile,Required fields cannot be left empty,Medium

AUTH-3,User can edit profile,Invalid email format is rejected,Medium

AUTH-3,User can edit profile,User receives confirmation after saving profile,Medium

```

#### Usability Tests

```csv

story_key,story_title,usability_test,priority

AUTH-3,User can edit profile,Can users easily find the profile settings page?,Medium

AUTH-3,User can edit profile,Do users understand which fields can be edited?,Medium

AUTH-3,User can edit profile,Is the save action clearly visible?,Medium

AUTH-3,User can edit profile,Are validation messages understandable?,Medium

AUTH-3,User can edit profile,Can users confirm that changes were saved?,Medium

```

#### Robot Framework

```robot

*** Test Cases ***

               Edit Profile Test

                    Open Browser    http://example.com

                    Click Element    profile_menu

                    Click Element    edit_profile_button

                    Input Text    first_name_field    John

                    Input Text    last_name_field    Doe

                    Click Button    save_button

                    Page Should Contain    Profile updated successfully

```

### Architecture

```text

User Stories - Input

      ↓

CSV Reader - Reading

      ↓

Prompt Builder - LLM instructions

      ↓

LLM Service - AI generation*

      ↓

Result Processing - Processing the LLM response

      ↓

Output Writers - Writing the output

      ↓

CSV and Robot Framework File - Outputs

```

* *LLM Service: MockLLM (simulated AI)

### Run as a batch job /backend (testing)

#### CSV

```bash

python -m app.csv_pipeline.generate_from_csv

```

---
