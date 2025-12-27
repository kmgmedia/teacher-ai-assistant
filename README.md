# AI Teaching Assistant

An AI-powered teaching assistant that automates repetitive writing tasks for early childhood educators.

## 🎯 Features

- **📝 Lesson Note Generator**: Creates structured, age-appropriate lesson plans
- **📊 Student Report Generator**: Writes professional progress reports from performance data
- **💌 Parent Communication Writer**: Drafts personalized messages for parent engagement
- **📈 Google Sheets Integration**: Syncs with student data for automated report generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Google Cloud service account (for Sheets integration)

### Installation

1. **Clone the repository**

   ```powershell
   git clone <repository-url>
   cd ai_assistant_for_teachers
   ```

2. **Create virtual environment**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```powershell
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:

   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GOOGLE_SHEETS_CREDENTIALS`: Path to your service account JSON file
   - `GOOGLE_SHEET_ID`: ID from your Google Sheet URL

### Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create a service account and download the JSON credentials
5. Share your Google Sheet with the service account email
6. Set the credentials path in `.env`

### Running the Application

```powershell
python main.py
```

The Flask server will start on `http://localhost:5000`

## 📡 API Endpoints

### Generate Lesson Note

```bash
POST /generate/lesson
Content-Type: application/json

{
  "subject": "Mathematics",
  "topic": "Introduction to Addition",
  "age_group": "5-6 years",
  "objectives": "Students will understand combining groups",
  "duration": 45
}
```

### Generate Student Report

```bash
POST /generate/report
Content-Type: application/json

{
  "student_name": "Emma Johnson",
  "period": "Term 1",
  "subject": "Overall Progress",
  "performance_notes": "Strong literacy skills...",
  "behavior_notes": "Works well with peers...",
  "save_to_sheets": false
}
```

### Generate Parent Message

```bash
POST /generate/parent-message
Content-Type: application/json

{
  "purpose": "appreciation",
  "child_name": "Liam Chen",
  "context": "Showed exceptional kindness...",
  "teacher_name": "Ms. Thompson"
}
```

### Get All Students

```bash
GET /students
```

### Get Specific Student

```bash
GET /students/<student_name>
```

## 📁 Project Structure

```
ai_assistant_for_teachers/
├── .github/
│   └── copilot-instructions.md    # AI agent guidelines
├── config/
│   └── settings.py                # Environment configuration
├── core/
│   ├── prompts/                   # AI prompt templates
│   │   ├── lesson_prompt.txt
│   │   ├── report_prompt.txt
│   │   └── parent_prompt.txt
│   └── logic/                     # Generator modules
│       ├── lesson_generator.py
│       ├── report_generator.py
│       └── parent_writer.py
├── integrations/
│   └── google_sheets.py           # Google Sheets API integration
├── utils/
│   └── helpers.py                 # Shared utilities
├── data/
│   ├── templates/                 # Example templates
│   └── output/                    # Generated files
├── main.py                        # Flask application
├── requirements.txt               # Python dependencies
└── .env.example                   # Environment template
```

## 🧪 Testing Individual Generators

Test generators without running the Flask server:

```powershell
# Test lesson generator
python -c "from core.logic.lesson_generator import generate_lesson; print(generate_lesson(subject='Math', topic='Addition', age_group='5-6 years', objectives='Learn to add', duration=45))"

# Test report generator
python core\logic\report_generator.py

# Test parent message writer
python core\logic\parent_writer.py

# Test Google Sheets connection
python integrations\google_sheets.py
```

## 🔧 Configuration

### Prompt Customization

Edit prompt templates in `core/prompts/*.txt` to change:

- Tone and style
- Output structure
- Educational approach

### OpenAI Settings

Adjust in `.env`:

- `OPENAI_MODEL`: Model version (gpt-4, gpt-3.5-turbo)
- `OPENAI_TEMPERATURE`: Creativity level (0.0-2.0)
- `OPENAI_MAX_TOKENS`: Response length limit

## 📝 Google Sheet Format

Expected columns in your Google Sheet:

| Name         | Subject | Score | Notes                | Behavior              |
| ------------ | ------- | ----- | -------------------- | --------------------- |
| Emma Johnson | Math    | 85    | Strong understanding | Participates actively |
| Liam Chen    | Reading | 90    | Excellent progress   | Very focused          |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ⚠️ Common Issues

**Import errors**: Make sure virtual environment is activated

```powershell
.\venv\Scripts\Activate.ps1
```

**Google Sheets authentication failed**:

- Check credentials file path in `.env`
- Verify service account has access to the sheet
- Ensure Google Sheets API is enabled

**OpenAI rate limit**: Implement retry logic or upgrade API plan

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

For issues and questions, please open a GitHub issue or contact the maintainers.

---

Built with ❤️ for educators
