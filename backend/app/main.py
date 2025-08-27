from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import aiofiles
from app.models import StoryRequest, StoryResponse, NarrateRequest, NarrateResponse
from app.services.story_generator import StoryGenerator
from app.services.tts_service import TTSService
from app.utils.helpers import validate_input, clean_text
from app.settings import settings

app = FastAPI(title="AI Story Teller", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

story_generator = StoryGenerator()
tts_service = TTSService()

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return {"message": "AI Story Teller API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Story Teller"}

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    if not settings.validate_duration(request.duration):
        raise HTTPException(status_code=400, detail=f"Duration must be between {settings.MIN_DURATION} and {settings.MAX_DURATION} minutes")
    
    is_valid, error_message = validate_input(request.character, request.theme)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    try:
        story = story_generator.generate_story(
            character=request.character,
            theme=request.theme,
            duration=request.duration,
            language=request.language.value
        )
        
        story = clean_text(story)
        
        audio_file, audio_duration = tts_service.narrate_text(
            story, request.language.value
        )
        
        return StoryResponse(
            story=story,
            duration=request.duration,
            language=request.language.value,
            audio_url=f"/audio/{os.path.basename(audio_file)}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

@app.post("/narrate", response_model=NarrateResponse)
async def narrate_text(request: NarrateRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        audio_file, duration = tts_service.narrate_text(
            request.text, request.language.value
        )
        
        return NarrateResponse(
            audio_url=f"/audio/{os.path.basename(audio_file)}",
            duration=duration
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error narrating text: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    audio_path = os.path.join(settings.AUDIO_DIR, filename)
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if filename.endswith('.txt'):
        async with aiofiles.open(audio_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        return {"content": content, "type": "text"}
    
    return FileResponse(audio_path, media_type="audio/mpeg")

@app.on_event("startup")
async def startup_event():
    tts_service.cleanup_old_files()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
