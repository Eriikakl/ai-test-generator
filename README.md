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
│   ├── csv_reader.py
│   ├── csv_writer.py
│   ├── generate_from_csv.py
│   ├── llm.py
│   ├── main.py
│   └── mock_llm.py
├── stories/
│   └── user_stories.csv
├── output/
│   ├── test_cases.csv
│   ├── usability_tests.csv
│   ├── generated_tests.robot
```

## Käyttäjätarinan formaatti

```csv
Issue key,summary,description,priority,status
AUTH-1,User can login,"As a user, I want to login so that I can access my account",High,To Do,3
```

## Tuotettavat tiedostot

### Test Cases

```csv
story_key,story_title,test_case,priority
AUTH-1,User can login,User can login with valid credentials,High
```

### Usability Tests

```csv
story_key,story_title,usability_test,priority
AUTH-1,User can login,Can user find login button?,High
```

### Robot Framework

```robot
*** Test Cases ***

Login Test
    Open Browser    http://example.com
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
User Stories
      ↓
CSV Reader
      ↓
LLM Service
      ↓
MockLLM
      ↓
Result Processing
      ↓
Output Writers
      ↓
CSV ja Robot Framework File
```

## Setup

### 1. Kloonataan repositorio

### 2. Luodaan virtuaaliympäristö

```bash
python -m venv .venv
```

Aktivointi:

**Windows:**
```bash
.venv\Scripts\activate
```


### 3. Asennetaan riippuvuudet

- Ei vielä tarvitse

## Suoritus

### Ajetaan agentti batch-ajona

```bash
python -m app.generate_from_csv
```

---
