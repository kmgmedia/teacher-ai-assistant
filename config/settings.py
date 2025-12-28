"""
Environment configuration and API client setup.
Centralizes all environment variables and credentials.
Supports both local development and Streamlit Cloud deployment.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Check if running on Streamlit Cloud
def get_config_value(key, default=None):
    """Get configuration from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, AttributeError, FileNotFoundError):
        pass
    return os.getenv(key, default)

# Google Gemini Configuration
GOOGLE_API_KEY = get_config_value("GOOGLE_API_KEY")
GOOGLE_MODEL = get_config_value("GOOGLE_MODEL", "gemini-1.5-flash")
GOOGLE_TEMPERATURE = float(get_config_value("GOOGLE_TEMPERATURE", "0.7"))
GOOGLE_MAX_TOKENS = int(get_config_value("GOOGLE_MAX_TOKENS", "1000"))

# Google Sheets Configuration
# GOOGLE_SHEETS_CREDENTIALS is only needed for local development
# On Streamlit Cloud, service account info comes from secrets.gcp_service_account
GOOGLE_SHEETS_CREDENTIALS = get_config_value("GOOGLE_SHEETS_CREDENTIALS")
GOOGLE_SHEET_ID = get_config_value("GOOGLE_SHEET_ID")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/output")

# Validate critical settings lazily: Gemini calls will check at runtime

# Google Sheets validation - only check for SHEET_ID
# Credentials can come from secrets (Streamlit Cloud) or local file
if not GOOGLE_SHEET_ID:
    import warnings
    warnings.warn(
        "Google Sheets integration not configured. "
        "You can still use lesson/report/parent message generators with manual input. "
        "To enable Google Sheets, set GOOGLE_SHEETS_CREDENTIALS and GOOGLE_SHEET_ID in .env",
        UserWarning
    )
