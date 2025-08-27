import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_generate_story():
    print("Testing story generation...")
    
    test_cases = [
        {
            "character": "brave knight",
            "theme": "friendship",
            "duration": 2,
            "language": "en"
        },
        {
            "character": "wise old man",
            "theme": None,
            "duration": 3,
            "language": "en"
        },
        {
            "character": None,
            "theme": "adventure",
            "duration": 1,
            "language": "en"
        },
        {
            "character": "बहादुर योद्धा",
            "theme": "दोस्ती",
            "duration": 2,
            "language": "hi"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test case {i}: {test_case}")
        try:
            response = requests.post(
                f"{BASE_URL}/generate-story",
                json=test_case,
                timeout=60
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Story length: {len(data['story'])} characters")
                print(f"Audio URL: {data['audio_url']}")
            else:
                print(f"Error: {response.text}")
            print()
        except Exception as e:
            print(f"Exception: {e}")
            print()

def test_narrate():
    print("Testing text-to-speech...")
    
    test_texts = [
        {"text": "Hello, this is a test narration.", "language": "en"},
        {"text": "नमस्ते, यह एक परीक्षण कथा है।", "language": "hi"}
    ]
    
    for test_case in test_texts:
        print(f"Testing: {test_case}")
        try:
            response = requests.post(
                f"{BASE_URL}/narrate",
                json=test_case,
                timeout=30
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Audio URL: {data['audio_url']}")
                print(f"Duration: {data['duration']} seconds")
            else:
                print(f"Error: {response.text}")
            print()
        except Exception as e:
            print(f"Exception: {e}")
            print()

def test_audio_download():
    print("Testing audio file download...")
    try:
        response = requests.get(f"{BASE_URL}/audio/test_file.mp3")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("Expected 404 for non-existent file")
        print()
    except Exception as e:
        print(f"Exception: {e}")
        print()

if __name__ == "__main__":
    print("=== AI Story Teller API Tests ===\n")
    
    test_health()
    test_generate_story()
    test_narrate()
    test_audio_download()
    
    print("=== Tests Complete ===")
