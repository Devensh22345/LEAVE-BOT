# Telegram Leave-on-Add Bot

This repository contains a minimal Telegram bot that **automatically leaves any group or channel** it is added to. It's suitable for deployment on Heroku using a worker dyno (or any other hosting that runs long-polling Python apps).

## Features
- When the bot's membership in a chat changes to `member` or `administrator`, it immediately leaves the chat.
- Responds to `/start` in private chats.

## Files
- `bot.py` - main bot code (uses `python-telegram-bot` v20).
- `requirements.txt` - Python dependencies.
- `Procfile` - for Heroku (runs the bot as a worker).
- `README.md` - this file.

## Setup & Deploy to Heroku (GitHub)
1. Create a new GitHub repository and push these files to it (or use the zip provided).
2. Create a new app on Heroku.
3. In Heroku dashboard, go to *Settings → Config Vars* and set:
   - `BOT_TOKEN` = your Telegram bot token (from BotFather)
4. Connect the GitHub repository in the *Deploy* tab and enable automatic deploys or manual deploy.
5. In *Resources* tab, scale the `worker` process to 1 (turn it on).
6. The bot will start and run using polling.

## Local run
1. Create a virtualenv and install deps:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Export your token and run:
```bash
export BOT_TOKEN="123456:ABC-DEF..."
python bot.py
```

## Notes & Security
- The bot leaves chats immediately; it does not store chat data.
- Keep your `BOT_TOKEN` secret (use Heroku Config Vars; don't commit tokens to git).

License: MIT
