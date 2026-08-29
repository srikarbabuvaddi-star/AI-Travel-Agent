import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    DEFAULT_CURRENCY = "₹"
    REQUEST_TIMEOUT = 10  # seconds for HTTP calls
    
    # Supported LLM model
    DEFAULT_MODEL = "gemini-2.0-flash"
    FALLBACK_MODEL = "gemini-1.5-flash"
