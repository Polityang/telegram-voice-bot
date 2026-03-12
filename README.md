# Telegram Voice Bot

A Telegram bot that automatically recognizes voice messages using Whisper and responds with the transcribed text.

## Features

- 🎤 Voice message recognition
- 🇨🇳 Chinese language support (default)
- 🔄 Automatic response with transcribed text
- ⚡ Fast inference using Whisper

## Prerequisites

- Python 3.8+
- Telegram Bot Token (get from @BotFather)
- OpenAI Whisper model (or use local installation)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-voice-bot.git
cd telegram-voice-bot

# Install dependencies
pip install -r requirements.txt

# Download Whisper model (optional - will download on first run)
# The base model will be downloaded automatically
```

## Configuration

1. Get your Telegram Bot Token from [@BotFather](https://t.me/BotFather)

2. Set environment variable:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

Or create a `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Usage

```bash
# Run the bot
python bot.py
```

The bot will:
1. Start polling for new messages
2. When a voice message is received, it will:
   - Download the voice file
   - Transcribe it using Whisper
   - Send the transcribed text back to the user

## Configuration Options

### Change Language

Edit `bot.py` to change the transcription language:

```python
result = model.transcribe(temp_path, language="zh")  # Chinese
# or
result = model.transcribe(temp_path, language="en")  # English
```

### Use Different Whisper Model

Edit `bot.py` to use a different model:

```python
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
```

### Change Response Format

Edit the `send_message` function in `bot.py` to customize the.

## Project Structure response format

```
telegram-voice-bot/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env.example       # Environment variables template
```

## Troubleshooting

### Bot not receiving messages

Make sure you've started the bot by sending `/start` command.

### Whisper download taking too long

Use a smaller model:
```python
model = whisper.load_model("tiny")  # Fastest, ~75MB
```

### Rate limiting

Telegram has rate limits. The bot includes basic error handling but you may need to add delays for high-volume usage.

## Security Notes

- Never commit your Bot Token to version control
- Add `.env` to your `.gitignore`
- The bot only processes voice messages, not text messages
- All voice processing is done locally

## License

MIT License

## Contributing

Pull requests are welcome!
