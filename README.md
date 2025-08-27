# AI Story Teller

An interactive AI-powered story generation and narration application that creates personalized stories based on user input and narrates them with text-to-speech.

## Features

- **AI Story Generation**: Create unique stories using OpenAI's GPT-3.5-turbo
- **Text-to-Speech Narration**: Automatic story narration in English or Hindi
- **Duration Control**: Customizable story length (1-5 minutes)
- **Language Support**: English and Hindi with optimized word counts
- **Modern Dark UI**: Responsive, stylish frontend with animated backgrounds
- **Interactive Loading**: Lottie animations during story generation
- **Audio Controls**: Play, pause, stop, and download audio files

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript with Lottie animations
- **AI**: OpenAI GPT-3.5-turbo API
- **TTS**: pyttsx3 (Offline) + gTTS (Online backup)
- **Styling**: Modern CSS with glassmorphism effects

## Project Structure

```
ai-story-teller/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── settings.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── story_generator.py
│   │   │   └── tts_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── requirements.txt
│   ├── .env
│   └── audio_files/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-story-teller
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp env.example .env
   # Add your OpenAI API key to .env
   uvicorn app.main:app --reload --port 5716
   ```

3. **Access the Application**:
   - Open `http://localhost:5716` in your browser
   - The frontend is served automatically by the FastAPI server

## API Endpoints

- `GET /`: Serve the main application
- `POST /generate-story`: Generate story based on input
- `POST /narrate`: Convert text to speech
- `GET /audio/{filename}`: Serve generated audio files
- `GET /health`: Health check

## Environment Variables

Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Enter a character name (optional)
2. Enter a theme (optional)
3. Select duration (1-5 minutes)
4. Choose language (English or Hindi)
5. Click "Generate Story"
6. Listen to the narrated story or download the audio

## Features

- **Smart Story Generation**: Uses OpenAI's GPT-3.5-turbo for creative storytelling
- **Language Optimization**: Hindi stories get 50% more words for better narration
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Audio Management**: Automatic cleanup of old audio files
- **Error Handling**: Graceful error handling with user-friendly messages

## License

MIT License
