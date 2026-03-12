# Telegram Voice Bot Skill

使用 Whisper 自动识别 Telegram 语音消息的技能。

## 功能
- 🎤 自动识别语音消息
- 🇨🇳 支持中文语音识别（默认）
- ⚡ 使用 Whisper 本地识别，保护隐私

## 依赖
- Python 3.8+
- openai-whisper
- requests
- Telegram Bot Token

## 配置
1. 从 @BotFather 获取 Telegram Bot Token
2. 设置环境变量或直接在代码中配置

## 使用方法
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your_token"
python bot.py
```

## 模型选择
支持多种 Whisper 模型：
- tiny (最快，~75MB)
- base (默认，~74MB)  
- small (~244MB)
- medium (~769MB)
- large (~1550MB)

## 许可证
MIT-0
