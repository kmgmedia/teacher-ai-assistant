"""
Shared utility functions for the AI Teaching Assistant.
Includes Google Gemini API wrapper, file operations, logging, and text processing.
"""
import os
import logging
from datetime import datetime
from google import genai
import time
import random
from config import settings


def setup_logger(name):
    """
    Set up a logger with file and console handlers.
    
    Args:
        name (str): Logger name (usually __name__ of the calling module)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Avoid adding duplicate handlers
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def call_openai(prompt, system_message=None, temperature=None, max_tokens=None):
    """
    Call Google Gemini API with error handling and retry logic.
    (Function name kept as call_openai for backward compatibility)
    
    Args:
        prompt (str): The user prompt to send
        system_message (str): Optional system message to set context
        temperature (float): Sampling temperature (0-2). Higher = more creative
        max_tokens (int): Maximum tokens in response
    
    Returns:
        str: Generated text response
    
    Raises:
        Exception: If API call fails after retries
    """
    logger = setup_logger(__name__)
    
    # Use settings defaults if not specified
    temperature = temperature if temperature is not None else settings.GOOGLE_TEMPERATURE
    max_tokens = max_tokens if max_tokens is not None else settings.GOOGLE_MAX_TOKENS
    
    if not settings.GOOGLE_API_KEY:
        raise Exception("Missing GOOGLE_API_KEY. Set it in environment variables before calling the model.")

    # Rate limiting: enforce 15-second cooldown between API calls for free tier
    if not hasattr(call_openai, "_last_call_time"):
        call_openai._last_call_time = 0
    
    time_since_last_call = time.time() - call_openai._last_call_time
    if time_since_last_call < 15:
        wait_time = 15 - time_since_last_call
        logger.info(f"Rate limiting: waiting {wait_time:.1f}s before next API call")
        time.sleep(wait_time)
    
    call_openai._last_call_time = time.time()
    logger.debug(f"Calling Google Gemini API with model: {settings.GOOGLE_MODEL}")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    full_prompt = prompt
    if system_message:
        full_prompt = f"{system_message}\n\n{prompt}"

    retries = 3
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=settings.GOOGLE_MODEL,
                contents=full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )

            generated_text = (response.text or "").strip()
            logger.debug(f"Google Gemini API response received ({len(generated_text)} chars)")
            return generated_text

        except Exception as e:
            message = str(e)
            upper = message.upper()
            if "API_KEY" in upper or "401" in upper:
                raise Exception("Invalid API key. Please check your GOOGLE_API_KEY in .env")
            if "QUOTA" in upper or "RATE" in upper or "429" in upper:
                if attempt < retries - 1:
                    # Free tier: wait longer between retries (30s, 60s)
                    delay = 30 * (attempt + 1)
                    logger.warning(f"Rate limit hit. Waiting {delay}s before retry {attempt+2}/{retries}")
                    time.sleep(delay)
                    continue
                raise Exception("⚠️ Free tier rate limit reached. Wait 60 seconds and try again, or upgrade your API plan.")
            logger.error(f"Google Gemini API error: {message}")
            raise Exception(f"Google Gemini API failed: {message}")


def save_to_file(content, filename, folder=""):
    """
    Save generated content to a timestamped file.
    
    Args:
        content (str): Content to save
        filename (str): Base filename (without extension)
        folder (str): Subfolder within OUTPUT_DIR (e.g., "lessons", "reports")
    
    Returns:
        str: Full path to saved file
    """
    logger = setup_logger(__name__)
    
    # Create output directory structure
    output_dir = os.path.join(settings.OUTPUT_DIR, folder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Add timestamp to filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.txt"
    filepath = os.path.join(output_dir, full_filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Content saved to: {filepath}")
        return filepath
    
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise


def clean_text(text):
    """
    Clean and format text output.
    
    Args:
        text (str): Raw text to clean
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Remove multiple consecutive blank lines
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    
    return text.strip()


def format_student_data(data_dict):
    """
    Format student data dictionary into readable string.
    Used when pulling data from Google Sheets.
    
    Args:
        data_dict (dict): Student data from sheets
    
    Returns:
        str: Formatted string representation
    """
    if not data_dict:
        return "No data available"
    
    formatted_lines = []
    for key, value in data_dict.items():
        # Convert keys from snake_case to Title Case
        readable_key = key.replace("_", " ").title()
        formatted_lines.append(f"{readable_key}: {value}")
    
    return "\n".join(formatted_lines)
