# 📁 Project Structure

```
ai_assistant_for_teachers/
│
├── 📄 dashboard.py              # Main Streamlit app (START HERE)
├── 🚀 launch_dashboard.ps1      # Quick launch script (double-click to run)
├── 📋 requirements.txt          # Python dependencies
├── 🔐 .env                      # API keys (DO NOT SHARE)
│
├── config/                      # Configuration files
│   ├── __init__.py
│   └── settings.py              # Environment variable loader
│
├── core/                        # AI generation logic
│   ├── logic/
│   │   ├── lesson_generator.py  # Lesson note generation
│   │   ├── report_generator.py  # Student report generation
│   │   └── parent_writer.py     # Parent message generation
│   └── prompts/                 # AI prompt templates
│       ├── lesson_prompt.txt
│       ├── report_prompt.txt
│       └── parent_prompt.txt
│
├── integrations/                # External integrations
│   ├── __init__.py
│   └── google_sheets.py         # Google Sheets data access
│
├── utils/                       # Helper functions
│   ├── __init__.py
│   └── helpers.py               # API calls, file operations
│
├── credentials/                 # Google service account
│   └── service-account.json     # DO NOT SHARE
│
├── data/                        # Data storage
│   └── templates/               # Document templates
│
└── logs/                        # Application logs
    └── app.log                  # Runtime logs

```

## 🎯 Essential Files Only

**Core Application:**

- `dashboard.py` - Main Streamlit interface
- `config/settings.py` - Configuration loader
- `core/logic/*.py` - AI generators
- `core/prompts/*.txt` - AI prompts
- `integrations/google_sheets.py` - Google Sheets integration
- `utils/helpers.py` - Utility functions

**Configuration:**

- `.env` - API keys and settings
- `requirements.txt` - Python packages
- `credentials/service-account.json` - Google credentials

**Launch:**

- `launch_dashboard.ps1` - Quick startup script

## 🗑️ Cleaned Up

The following temporary/debug files have been removed:

- `check_*.py` - Debug scripts
- `create_*.py` - One-time setup scripts
- `fix_*.py` - Temporary fix scripts
- `populate_sheet.py` - Data population script
- `google_sheet_data.txt` - Temporary data file
- `__pycache__/` - Python cache folders
- `.pytest_cache/` - Test cache

## ⚡ Performance Optimizations

1. **Caching**: Student data cached for 5 minutes
2. **Clean Structure**: Only essential files remain
3. **Fast Startup**: Simplified launch script
4. **No Redundancy**: Removed duplicate/temporary files
