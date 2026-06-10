# AI Test Generator

Tavoitteena on automatisoida käyttäjätarinoiden muuttaminen testitapauksiksi sekä mahdollistaa myöhemmin integraatiot Jiraan. 
Tarkoituksena luoda AI-pohjainen testausagentti, joka lukee käyttäjätarinoita CSV-tiedostosta ja generoi:

- Testitapaukset
- Robot Framework -testiskriptit
- Käytettävyystestit



## Nykyinen tilanne

- Kehityksessä

Tällä hetkellä agentti:

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
│   ├── csv_reader.py
│   ├── csv_writer.py
│   ├── generate_from_csv.py
│   ├── llm.py
│   ├── main.py
│   ├── mock_llm.py
│   ├── prompt_builder.py
│
├── stories/
│   └── user_stories.csv
├── output/
│   ├── test_cases.csv
│   ├── usability_tests.csv
│   ├── generated_tests.robot
```

## Käyttäjätarinan formaatti

```csv
Issue key,Summary,Description,Priority,Status
AUTH-3,User can edit profile,"As a user, I want to update my profile information",Medium,To Do
```

## Tuotettavat tiedostot

### Test Cases

```csv
story_key,story_title,test_case,priority
AUTH-3,User can edit profile,User can update profile information successfully,Medium
AUTH-3,User can edit profile,Changes are saved and visible after refresh,Medium
AUTH-3,User can edit profile,Required fields cannot be left empty,Medium
AUTH-3,User can edit profile,Invalid email format is rejected,Medium
AUTH-3,User can edit profile,User receives confirmation after saving profile,Medium
```

### Usability Tests

```csv
story_key,story_title,usability_test,priority
AUTH-3,User can edit profile,Can users easily find the profile settings page?,Medium
AUTH-3,User can edit profile,Do users understand which fields can be edited?,Medium
AUTH-3,User can edit profile,Is the save action clearly visible?,Medium
AUTH-3,User can edit profile,Are validation messages understandable?,Medium
AUTH-3,User can edit profile,Can users confirm that changes were saved?,Medium
```

### Robot Framework

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

## Teknologiat

### Backend

- Python
- FastAPI

### AI

Nykyinen:
- MockLLM

Suunnitteilla:
- OpenAI
- Ollama
- Llama

### Data

Nykyinen:
- CSV

Suunnitteilla:
- PostgreSQL

## Arkkitehtuuri

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

- Ei vielä tarvitse

## Suoritus

### Ajetaan agentti batch-ajona

```bash
python -m app.generate_from_csv
```

---
