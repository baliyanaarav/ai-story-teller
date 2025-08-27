import os
import pyttsx3
import tempfile
import uuid
from gtts import gTTS
from typing import Tuple
import time
from app.settings import settings

class TTSService:
    def __init__(self):
        self.engine = None
        self.audio_dir = settings.AUDIO_DIR
        self._ensure_audio_dir()
    
    def _get_engine(self):
        if self.engine is None:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                print(f"Failed to initialize pyttsx3: {e}")
                self.engine = None
        return self.engine
        
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
            print(f"gTTS failed, using pyttsx3: {e}")
            return self._narrate_with_pyttsx3(text, 'en')
    
    def _narrate_hindi(self, text: str) -> Tuple[str, float]:
        try:
            filename = f"{self.audio_dir}/story_{uuid.uuid4().hex}.mp3"
            
            tts = gTTS(text=text, lang='hi', slow=False)
            tts.save(filename)
            
            duration = self._estimate_duration(text)
            return filename, duration
            
        except Exception as e:
            print(f"gTTS Hindi failed, using pyttsx3: {e}")
            return self._narrate_with_pyttsx3(text, 'hi')
    
    def _narrate_with_pyttsx3(self, text: str, language: str) -> Tuple[str, float]:
        try:
            engine = self._get_engine()
            if engine is None:
                raise Exception("pyttsx3 engine not available")
            
            filename = f"{self.audio_dir}/story_{uuid.uuid4().hex}.wav"
            
            if language == "hi":
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'hindi' in voice.name.lower() or 'indian' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            engine.setProperty('rate', settings.TTS_RATE)
            engine.setProperty('volume', settings.TTS_VOLUME)
            
            engine.save_to_file(text, filename)
            engine.runAndWait()
            
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
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(self.audio_dir):
            filepath = os.path.join(self.audio_dir, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    try:
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Failed to delete {filepath}: {e}")
