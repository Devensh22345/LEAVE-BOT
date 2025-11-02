# telegram-auto-leaver-repo (Pyrogram)

Minimal repo: a Telegram bot that **automatically leaves** any group, supergroup, or channel it is added to.

Files included:
- pyrogram_bot.py  (Pyrogram implementation)
- bot.py           (python-telegram-bot implementation, reference)
- requirements.txt
- .env.example
- Dockerfile
- Procfile
- LICENSE (MIT)

Instructions:
1. Copy `.env.example` to `.env` and set BOT_TOKEN (and optionally OWNER_ID).
2. Install deps: `pip install -r requirements.txt`
3. Run: `python pyrogram_bot.py`
