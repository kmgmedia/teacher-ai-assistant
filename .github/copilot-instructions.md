# AI Teaching Assistant - Copilot Instructions

## Project Overview

This is an AI-powered teaching assistant that automates repetitive writing tasks for teachers:

- **Lesson Note Generator**: Creates structured lesson plans (intro, main activity, conclusion, evaluation)
- **Student Report Generator**: Writes professional progress reports from behavioral/performance data
- **Parent Communication Writer**: Drafts parent messages (reminders, feedback, appreciation)
- **Google Sheets Integration**: Syncs student data, scores, and attendance for automation

**Goal**: Free teachers from repetitive writing while maintaining consistent, professional tone.

## Tech Stack

- **Backend**: Flask (serves API endpoints and orchestrates generators)
- **AI**: OpenAI GPT-4 API (text generation via `openai` Python library)
- **Data Source**: Google Sheets API (`gspread` + `google-auth`)
- **Optional Frontend**: React.js or Streamlit dashboard

## Architecture: 4-Module Design

### 1. Core Logic (`core/logic/`)

Each generator module follows this pattern:

1. Load prompt template from `core/prompts/*.txt`
2. Inject user inputs (subject, student name, etc.) into template
3. Call OpenAI API with structured prompt
4. Return formatted response

**Key files**:

- `lesson_generator.py` - Inputs: subject, topic, age group, objectives, duration
- `report_generator.py` - Inputs: student name, behavior notes, performance metrics
- `parent_writer.py` - Inputs: purpose (reminder/appreciation/feedback), student name

**Pattern**: All generators use `utils.helpers.call_openai()` wrapper for API calls.

### 2. Prompt Engineering (`core/prompts/`)

Prompt templates use `{variable}` placeholders for dynamic content:

- `lesson_prompt.txt` - "You are a professional early childhood educator..."
- `report_prompt.txt` - "Write a progress report for student {name}..."
- `parent_prompt.txt` - "Draft a {purpose} message to parents about {child_name}..."

**Convention**: Prompts define tone, structure, and output format. Always preserve the system role instruction.

### 3. Google Sheets Integration (`integrations/google_sheets.py`)

- Authenticates via service account JSON (path in `.env`)
- **Read operations**: Fetch student rosters, scores, attendance
- **Write operations**: Save generated reports back to designated sheet tabs
- Sheet structure: Expect columns like `Name`, `Subject`, `Score`, `Notes`

**Critical**: Always use `gspread.authorize()` with credentials from `GOOGLE_SHEETS_CREDENTIALS` env var.

### 4. Configuration (`config/settings.py`)

Centralizes environment variables:

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
```

Never hardcode API keys. Use `.env` file (excluded from Git).

## Development Workflows

### Running the Application

```powershell
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run Flask server
python main.py
```

Starts server on `http://localhost:5000`. Endpoints:

- `POST /generate/lesson` - Create lesson note
- `POST /generate/report` - Create student report
- `POST /generate/parent-message` - Draft parent communication

### Testing Generators Independently

```powershell
# Test lesson generator
python -c "from core.logic.lesson_generator import generate_lesson; print(generate_lesson(subject='Math', topic='Addition', age_group='5-6 years'))"
```

### Google Sheets Setup

1. Create service account in Google Cloud Console
2. Download JSON credentials
3. Share target Google Sheet with service account email
4. Set `GOOGLE_SHEETS_CREDENTIALS` to JSON file path in `.env`

## Project-Specific Conventions

### File Naming

- Generators: `{feature}_generator.py` (e.g., `lesson_generator.py`)
- Prompts: `{feature}_prompt.txt` (matches generator name)
- Outputs saved to `data/output/{feature}_{timestamp}.txt`

### Error Handling

All API calls wrapped in try-except:

```python
try:
    response = openai.ChatCompletion.create(...)
except openai.error.OpenAIError as e:
    logger.error(f"OpenAI API failed: {e}")
    return {"error": "Generation failed"}
```

### Logging

Use `utils.helpers.setup_logger()` in all modules. Logs saved to `logs/app.log`.

### Data Flow Pattern

```
User Input → Flask Endpoint → Generator Module → Prompt Template + OpenAI API → Response Formatting → Output File/API Response
                                ↓
                         Google Sheets (optional data source)
```

## Key Files & Their Roles

- `main.py` - Flask app initialization, route definitions
- `config/settings.py` - Environment config, API client setup
- `core/prompts/*.txt` - Prompt engineering templates (edit these to change tone/structure)
- `integrations/google_sheets.py` - Sheet read/write operations
- `utils/helpers.py` - Shared utilities: `call_openai()`, `save_to_file()`, `clean_text()`

## Adding New Features

1. Create prompt template in `core/prompts/{feature}_prompt.txt`
2. Implement generator in `core/logic/{feature}_generator.py`
3. Add Flask route in `main.py` (e.g., `POST /generate/{feature}`)
4. Update `README.md` with new endpoint documentation

## Common Pitfalls

- **Forgetting to load .env**: Use `python-dotenv` in `settings.py`
- **Sheet permissions**: Service account must have editor access to target sheets
- **Token limits**: Long reports may exceed GPT-4 context window - chunk if needed
- **Rate limiting**: Implement retry logic in `call_openai()` for 429 errors
