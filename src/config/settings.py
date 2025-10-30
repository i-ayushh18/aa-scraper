# src/config/settings.py
"""
Configuration settings for the AA flight scraper.
"""
import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # Contest Search parameters
    ORIGIN = os.getenv("ORIGIN", "LAX")
    DESTINATION = os.getenv("DESTINATION", "JFK") 
    DATE = os.getenv("DATE", "2025-12-15")
    PASSENGERS = int(os.getenv("PASSENGERS", "1"))
    CABIN_CLASS = os.getenv("CABIN_CLASS", "economy")
    
    # Scraper settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))
    
    # Browser settings
    BROWSER_WIDTH = 1920
    BROWSER_HEIGHT = 1080
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.122 Safari/537.36"
    
    # Strategy settings
    ENABLE_UNDETECTED = os.getenv("ENABLE_UNDETECTED", "true").lower() == "true"
    ENABLE_PLAYWRIGHT = os.getenv("ENABLE_PLAYWRIGHT", "true").lower() == "true"
    ENABLE_FALLBACK = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"
    
    # Cache settings
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    
    # Output settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    SCREENSHOT_ON_ERROR = os.getenv("SCREENSHOT_ON_ERROR", "true").lower() == "true"
    
    # AA.com URLs
    AA_BASE_URL = "https://www.aa.com"
    
    @classmethod
    def get_search_params(cls) -> Dict[str, Any]:
        """Get search parameters as dictionary"""
        return {
            "origin": cls.ORIGIN,
            "destination": cls.DESTINATION,
            "date": cls.DATE,
            "passengers": cls.PASSENGERS,
            "cabin_class": cls.CABIN_CLASS
        }
    
    @classmethod
    def get_cache_key(cls) -> str:
        """Generate cache key for current search"""
        return f"aa_{cls.ORIGIN}_{cls.DESTINATION}_{cls.DATE}_{cls.PASSENGERS}_{cls.CABIN_CLASS}"