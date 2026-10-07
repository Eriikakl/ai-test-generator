from fastapi import FastAPI
from app.llm import LLMService
## from app.config import GEMINI_API_KEY
from fastapi.middleware.cors import CORSMiddleware
from app.service.jira_service import get_jira_service

import asyncio
from contextlib import asynccontextmanager

from app.service.test_generation_service import (
    generate_test_cases,
    generate_usability_tests
)

## Starts Jira synchronization as a background task when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(sync_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan) ## lifespan=lifespan
llm = LLMService(use_mock=True) ## GEMINI_API_KEY (Gemini mode)
jira = get_jira_service()

## Allow requests from the frontend and configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

## Jira webhook for automatic test case generation
## Endpoint is available but not currently configured in Jira
@app.post("/jira/webhook")
def jira_webhook(payload: dict):

    issue = payload["issue"]

    if issue["fields"]["issuetype"]["name"] != "Story":
        return {"status": "ignored"}

    issue_key = issue["key"]
    story = jira.get_story(issue_key)
    test_cases = generate_test_cases(llm, story)
    jira.push_test_cases(story, test_cases)

    return {
        "status": "success",
        "issue_key": issue_key,
        "test_cases_created": len(test_cases)
    }

## Manually triggers Jira synchronization through an API request
@app.post("/jira/sync")
def sync():

    processed = sync_stories()

    return {
        "status": "success",
        "stories_processed": processed
    }

## Retrieves test cases linked to a user story
@app.get("/test-cases/{issue_key}")
def get_test_cases_endpoint(issue_key: str):

    test_cases = jira.get_test_cases(issue_key)

    return {
        "issue_key": issue_key,
        "test_cases": [
            {
                "key": tc["key"],
                "summary": tc["fields"]["summary"]
            }
            for tc in test_cases
        ]
    }

## Generates test cases based on the given user story key
## Saves the generated test cases to Jira
@app.post("/generate/test-cases/{issue_key}")
def generate_test_cases_endpoint(issue_key: str):
    story = jira.get_story(issue_key)

    test_cases = generate_test_cases(llm, story)

    jira.push_test_cases(story, test_cases)

    return {
        "issue_key": issue_key,
        "test_cases": test_cases
    }

## Generates usability tests based on the given user story key and its linked test cases
## Saves the generated usability tests to Jira
@app.post("/generate/usability-tests/{issue_key}") 
def generate_usability_tests_endpoint(issue_key: str): 
 
    story = jira.get_story(issue_key) 
    test_cases = jira.get_test_cases(issue_key) 

    test_cases_for_prompt = [ 
        { 
            "key": tc["key"], 
            "summary": tc["fields"]["summary"] 
        } 
        for tc in test_cases 
    ] 

    usability_tests = generate_usability_tests( 
        llm, 
        story, 
        test_cases_for_prompt 
    )

    created_usability_tests = jira.push_usability_tests(
        story,
        usability_tests
    )
 
    return { 
        "issue_key": issue_key, 
        "usability_tests": created_usability_tests
    }



## Synchronizes unprocessed user stories
def sync_stories():

    stories = jira.get_new_stories()

    processed = 0

    for story in stories:

        if jira.has_test_cases(story.issue_key):
            print(f"{story.issue_key} already processed.")
            continue

        test_cases = generate_test_cases(llm, story)
        jira.push_test_cases(story, test_cases)

        processed += 1

    return processed

## Runs Jira synchronization in the background every minute
async def sync_loop():
    while True:
        try:
            processed = await asyncio.to_thread(sync_stories)
            print(f"Jira sync completed. Processed {processed} stories.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Jira sync failed: {e}")

        await asyncio.sleep(60)


