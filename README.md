# AI Test Generator

AI-pohjainen testiautomaatioprojekti, joka yhdistää Jira-integraation ja LLM-pohjaisen testitapausten generoinnin. Jiran käyttäjätarinoista generoidaan testitapauksia automaattisesti, luodaan ne Jiraan ja linkitetään takaisin alkuperäisiin käyttäjätarinoihin.

Projektia on suunniteltu laajennettavaksi myös käytettävyystestien ja testiscriptien generointiin.

## Nykyinen tilanne

- Kehityksessä

Tällä hetkellä projekti koostuu kahdesta eri workflow:sta.

Jira-pohjainen test case -generointi:
- Hakee Jira API:sta käyttäjätarinan
- Generoi testitapaukset LLM:n (Gemini) avulla
- Luo Jiraan Task-issuet testitapauksista ja linkittää ne alkuperäiseen käyttäjätarinaan
- Hakee käyttäjätarinan testitapaukset ja generoi niiden sekä alkuperäisen käyttäjätarinan pohjalta käytettävyystestit
- Luo käytettävyystesteistä Jiraan Task-issuet ja linkittää ne alkuperäiseen käyttäjätarinaan
- Käytettävyystestien generointi voidaan käynnistää käyttöliittymästä tai suoraan FastAPI-endpointin kautta

[Katso projektin nykyinen tila](docs/Results.md) 

---
Kehitystä ja testausta varten projekti sisältää myös CSV-pohjaisen generointityönkulun.

CSV-pohjainen testidatan generointi:
- Lukee käyttäjätarinat CSV-tiedostosta
- Käyttää MockLLM-komponenttia testidatan generointiin
- Tuottaa:
      - `test_cases.csv`
      - `usability_tests.csv`
      - `generated_tests.robot`

## Projektirakenne

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

## Teknologiat

### Backend

- Python
- FastAPI
- Requests (Jira API)

### AI

Nykyinen:
- Google Gemini API
- MockLLM (Kehitys ja testaus)

### Data

Nykyinen:
- CSV (testaus)
- JSON

Suunnitteilla:
- PostgreSQL

### Frontend

- TypeScript
- React
- Vite

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

#### Yksittäisen käyttäjätarinan käsittely
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
#### Automaattinen Jira-synkronointi
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

- Valmisteltu endpoint Jira-automaatiota varten.
- Tarkoituksena käsitellä uudet käyttäjätarinat automaattisesti.

---

**Jira Sync**

```http
POST /jira/sync
```

- Synkronoi käsittelemättömät käyttäjätarinat Jirasta.
- Luo testitapaukset automaattisesti uusille käyttäjätarinoille.

---

**Testitapausten hakeminen**

```http
GET /test-cases/{issue_key}
```

- Hakee käyttäjätarinaan linkitetyt testitapaukset annetun tunnuksen perusteella.

---

**Testitapausten generointi**

```http
POST /generate/test-cases/{issue_key}
```

- Hakee käyttäjätarinan Jira API:sta annetun tunnuksen perusteella.
- Generoi testitapaukset käyttäjätarinan perusteella LLMn avulla.
- Luo generoiduista testitapauksista Jiraan Task-issuet.
- Linkittää testitapaukset alkuperäiseen käyttäjätarinaan.

---

**Käytettävyystestien generointi**

```http
POST /generate/usability-tests/{issue_key}
```

- Hakee käyttäjätarinan Jira API annetun issue keyn perusteella.
- Hakee käyttäjätarinaan linkitetyt testitapaukset.
- Generoi käytettävyystestit käyttäjätarinan ja testitapausten perusteella LLM avulla.
- Palauttaa generoidut käytettävyystestit käyttöliittymälle tarkistettavaksi.
- Generoituja testejä ei tässä vaiheessa vielä luoda Jiraan.

---

**Käytettävyystestien lähettäminen Jiraan**

```http
POST /push/usability-tests/{issue_key}
```

- Vastaanottaa käyttöliittymässä tarkistetut käytettävyystestit.
- Välittää vain käyttäjän hyväksymät testit Jiraan.
- Luo hyväksytyistä käytettävyystesteistä Jira Task -issuet.
- **Ei vielä aseta testille käyttäjän määrittämää prioriteettia.**
- Linkittää luodut käytettävyystestit alkuperäiseen käyttäjätarinaan.

---

**Jira-käyttäjätarinoiden haku**

```http
GET /jira/stories/search?q={query}&limit={limit}
```

- Hakee Jira-projektista käyttäjätarinoita hakusanan tai issue keyn perusteella.
- Rajaa haun vain Story-tyyppisiin issueihin.
- Palauttaa löydettyjen käyttäjätarinoiden issue keyt ja otsikot API-vastauksena.
- Käyttöliittymä hyödyntää endpointia käyttäjätarinan valintaan.

---

## Setup

### 1. Kloonataan repositorio

### 2. Luodaan virtuaaliympäristö

```bash
python -m venv .venv
```

Aktivointi:

```bash
. .venv/scripts/activate
```


### 3. Asennetaan riippuvuudet /backend

```bash
pip install fastapi uvicorn requests python-dotenv google-genai
```


#### Vain Jira-workflow:
```bash
pip install requests python-dotenv google-genai
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

### Käynnistetään FastAPI /backend

```bash
uvicorn app.main:app --reload
```
- Käynnistyksen yhteydessä sovellus aloittaa automaattisen Jira-synkronoinnin.
- Synkronointi suoritetaan minuutin välein taustalla.
---

### Käynnistetään /frontend

```bash
npm install
npm run dev
```

---

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

### Ajetaan batch-ajona /backend (testaus)

#### CSV

```bash
python -m app.csv_pipeline.generate_from_csv
```

---

