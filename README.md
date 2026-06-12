# AI Test Generator

Tavoitteena on automatisoida käyttäjätarinoiden muuttaminen testitapauksiksi sekä mahdollistaa integraatio Jiraan. 

Tarkoituksena luoda AI-pohjainen testausagentti/testiautomaatioputki, joka käsittelee käyttäjätarinoita kahdessa eri workflow:ssa.



## Nykyinen tilanne

- Kehityksessä

Tällä hetkellä projekti koostuu kahdesta eri workflow:sta.

Jira-pohjainen test case -generointi:
- Hakee Jira API:sta käyttäjätarinan
- Generoi testitapaukset LLM:n (Gemini) avulla
- Luo käyttäjätarinan pohjalta test case-issuen
- Luo Jiraan Task:it testitapauksista linkittäen ne alkuperäiseen käyttäjätarinaan

CSV-pohjainen testidatan generointi:
- Lukee käyttäjätarinat CSV-tiedostosta
- Käyttää MockLLM-komponenttia testidatan generointiin
- Tuottaa:
      - `test_cases.csv`
      - `usability_tests.csv`
      - `generated_tests.robot`

 FastAPI on valmisteltu tulevaa API-rajapintaa ja integraatioita varten.

## Projektirakenne

```text
backend/
├── app/
│   ├── domain/
│       └── story.py
│   ├── service/
│       └── jira_service.py
│   ├── config.py
│   ├── csv_reader.py
│   ├── csv_writer.py
│   ├── generate_from_csv.py
│   ├── llm.py
│   ├── main.py
│   ├── mock_llm.py
│   ├── prompt_builder.py
│   ├── run_from_jira.py
│
├── stories/
│   └── user_stories.csv
├── output/
│   ├── test_cases.csv
│   ├── usability_tests.csv
│   ├── generated_tests.robot
```

## Teknologiat

### Backend

- Python
- Requests
- FastAPI


### AI

Nykyinen:
- Google Gemini API
- MockLLM

### Data

Nykyinen:
- CSV
- JSON

Suunnitteilla:
- PostgreSQL

## Jira

### Käyttäjätarinan formaatti

```JSON
{
  "issue_key": "ABC-1",
  "summary": "User can login",
  "description": "As a user I want to login...",
  "priority": "High",
  "status": "To Do"
}
```
### Arkkitehtuuri

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
```

### Tulokset

**Jira:**
![alt text](/screenshots/Jira.png)

## CSV
### Käyttäjätarinan formaatti

```csv
Issue key,Summary,Description,Priority,Status
AUTH-3,User can edit profile,"As a user, I want to update my profile information",Medium,To Do
```

### Tuotettavat tiedostot

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



### Arkkitehtuuri


```text
User Stories - Syöte
      ↓
CSV Reader - Luku
      ↓
Prompt Builder - LLM-ohjeistus
      ↓
LLM Service - AI generointi*
      ↓
Result Processing - LLM:n vastauksen käsittely
      ↓
Output Writers - Tuotoksen kirjoitus
      ↓
CSV ja Robot Framework File - Tuotokset
```

-  *LLM Service: MockLLM (simuloitu AI)

## Setup

### 1. Kloonataan repositorio

### 2. Luodaan virtuaaliympäristö

```bash
python -m venv .venv
```

Aktivointi:

**Windows:**
```bash
. .venv/scripts/activate
```


### 3. Asennetaan riippuvuudet

#### Vain Jira-workflow:
```bash
pip install requests

pip install python-dotenv
```

---
```bash
pip install google-genai
```

---

### 4. Ympäristömuuttujat
Projektiin on luotu `.env` tiedosto Jira-asetusten turvalliseen käyttöön: 

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your.email@example.com
JIRA_API_TOKEN=your_api_token_here
JIRA_PROJECT_KEY=ABC

GEMINI_API_KEY=your_api_token_here
```


## Suoritus

### Ajetaan batch-ajona

#### CSV

```bash
python -m app.generate_from_csv
```

---

#### Jira 
```bash
python -m app.run_from_jira
```

---


