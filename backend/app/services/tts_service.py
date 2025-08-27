import os
import tempfile
import uuid
from gtts import gTTS
from typing import Tuple
import time
from app.settings import settings

class TTSService:
    def __init__(self):
        self.audio_dir = settings.AUDIO_DIR
        self._ensure_audio_dir()
        
    def _ensure_audio_dir(self):
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
    
    def narrate_text(self, text: str, language: str) -> Tuple[str, float]:
        if language == "hi":
            return self._narrate_hindi(text)
        else:
            return self._narrate_english(text)
    
    def _narrate_english(self, text: str) -> Tuple[str, float]:
        try:
            filename = f"{self.audio_dir}/story_{uuid.uuid4().hex}.mp3"
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            
            duration = self._estimate_duration(text)
            return filename, duration
            
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    def _narrate_hindi(self, text: str) -> Tuple[str, float]:
        try:
            filename = f"{self.audio_dir}/story_{uuid.uuid4().hex}.mp3"
            
            tts = gTTS(text=text, lang='hi', slow=False)
            tts.save(filename)
            
            duration = self._estimate_duration(text)
            return filename, duration
            
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    def _estimate_duration(self, text: str) -> float:
        words = len(text.split())
        duration_minutes = words / settings.WORDS_PER_MINUTE
        return round(duration_minutes * 60, 2)
    
    def cleanup_old_files(self, max_age_hours: int = None):
        if max_age_hours is None:
            max_age_hours = settings.MAX_AUDIO_FILE_AGE_HOURS
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        try:
            for filename in os.listdir(self.audio_dir):
                file_path = os.path.join(self.audio_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        print(f"Cleaned up old audio file: {filename}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
