import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MAX_DURATION = 5
    MIN_DURATION = 1
    DEFAULT_DURATION = 2
    WORDS_PER_MINUTE = 150
    HINDI_WORDS_PER_MINUTE = 120
    MAX_LENGTH = 500
    TEMPERATURE = 0.8
    TTS_RATE = 150
    TTS_VOLUME = 0.9
    AUDIO_DIR = "audio_files"
    MAX_AUDIO_FILE_AGE_HOURS = 24
    PORT = 5716
    
    SUPPORTED_LANGUAGES = {
        "en": {"name": "English", "code": "en", "tts_lang": "en"},
        "hi": {"name": "Hindi", "code": "hi", "tts_lang": "hi"}
    }
    
    @classmethod
    def validate_duration(cls, duration: int) -> bool:
        return cls.MIN_DURATION <= duration <= cls.MAX_DURATION
    
    @classmethod
    def get_word_count(cls, duration: int, language: str = "en") -> int:
        if language == "hi":
            return duration * cls.HINDI_WORDS_PER_MINUTE
        return duration * cls.WORDS_PER_MINUTE

settings = Settings()
