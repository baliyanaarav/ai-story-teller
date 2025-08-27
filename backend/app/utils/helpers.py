import re
from typing import Tuple

def validate_input(character: str = None, theme: str = None) -> Tuple[bool, str]:
    if not character and not theme:
        return False, "Either character or theme must be provided"
    
    if character and len(character.strip()) < 2:
        return False, "Character must be at least 2 characters long"
    
    if theme and len(theme.strip()) < 2:
        return False, "Theme must be at least 2 characters long"
    
    return True, ""

def estimate_word_count(duration: int) -> int:
    words_per_minute = 150
    return duration * words_per_minute

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def get_language_code(language: str) -> str:
    language_map = {
        "en": "en",
        "hi": "hi-IN"
    }
    return language_map.get(language, "en")
