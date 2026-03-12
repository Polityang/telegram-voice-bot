"""
Telegram Voice Bot
Automatically recognizes voice messages and responds with transcribed text.

Usage:
    python bot.py
    
Environment variables:
    TELEGRAM_BOT_TOKEN - Your Telegram Bot Token (get from @BotFather)
"""
import os
import time
import requests
import whisper
import tempfile
import uuid
from pathlib import Path

# Configuration - Set your token here or use environment variable
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Whisper model - options: tiny, base, small, medium, large
# tiny: fastest, ~75MB
# base: ~75M parameters, ~74MB
# small: ~244M parameters, ~244MB
MODEL_NAME = "base"

def load_model():
    """Load Whisper model"""
    print(f"Loading Whisper model: {MODEL_NAME}...")
    model = whisper.load_model(MODEL_NAME)
    print("Model loaded!")
    return model

def get_updates(offset=0):
    """Get updates from Telegram"""
    try:
        resp = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": offset, "timeout": 30},
            timeout=35
        )
        return resp.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return {"ok": False, "error": str(e)}

def download_file(file_id):
    """Download voice file from Telegram"""
    try:
        # Get file info
        resp = requests.get(f"{BASE_URL}/getFile", params={"file_id": file_id}, timeout=10)
        data = resp.json()
        
        if not data.get("ok"):
            print(f"Error getting file info: {data}")
            return None
        
        file_path = data["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        
        # Download file
        resp = requests.get(file_url, timeout=30)
        return resp.content
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def transcribe_audio(audio_data):
    """Transcribe audio using Whisper"""
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        f.write(audio_data)
        temp_path = f.name
    
    try:
        # Transcribe
        result = model.transcribe(temp_path, language="zh")
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return None
    finally:
        # Clean up
        try:
            os.remove(temp_path)
        except:
            pass

def send_message(chat_id, text):
    """Send message to user"""
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )
    except Exception as e:
        print(f"Error sending message: {e}")

def process_voice_message(chat_id, file_id):
    """Process a voice message"""
    print(f"Received voice from {chat_id}")
    
    # Download audio
    audio_data = download_file(file_id)
    if not audio_data:
        send_message(chat_id, "Sorry, couldn't download the voice file.")
        return
    
    # Transcribe
    text = transcribe_audio(audio_data)
    if text:
        print(f"Transcribed: {text}")
        send_message(chat_id, f"You said: {text}")
    else:
        send_message(chat_id, "Sorry, couldn't recognize the voice.")

def main():
    """Main loop"""
    global model
    
    # Validate token
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        print("Please set your Telegram Bot Token:")
        print("  export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("Or set it in the code:")
        print("  TELEGRAM_BOT_TOKEN = 'your_token_here'")
        return
    
    # Test API
    try:
        resp = requests.get(f"{BASE_URL}/getMe", timeout=10)
        if not resp.json().get("ok"):
            print("Error: Invalid bot token!")
            return
        print(f"Bot connected: @{resp.json()['result']['username']}")
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")
        return
    
    # Load model
    model = load_model()
    
    # Main loop
    print("Bot started! Waiting for voice messages...")
    offset = 0
    
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    
                    message = update.get("message", {})
                    voice = message.get("voice")
                    
                    if voice:
                        chat_id = message["chat"]["id"]
                        file_id = voice["file_id"]
                        process_voice_message(chat_id, file_id)
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nBot stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    model = None
    main()
