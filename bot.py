#!/usr/bin/env python3
"""
Telegram bot that automatically leaves any group or channel it is added to.

Usage:
- Set the environment variable BOT_TOKEN to your bot token.
- Run: python bot.py
- On Heroku: set BOT_TOKEN in Config Vars and use the provided Procfile (worker).
"""
import os
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8433683728:AAEvdlqbOsEBdgCSS5AdhqiZMB_UuYIAqEU")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set. Exiting.")
    raise SystemExit("BOT_TOKEN environment variable not set")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple /start reply for private chats."""
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "Hello! I will automatically leave any group or channel I'm added to. 😊"
        )

async def my_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle my_chat_member updates (changes to the bot's status in chats).
    If the bot is added to a group/channel (status becomes 'member' or 'administrator'),
    the bot will leave immediately.
    """
    try:
        chat = update.effective_chat
        # The ChatMemberHandler gives us update.my_chat_member
        if update.my_chat_member is None:
            return

        old_status = update.my_chat_member.old_chat_member.status
        new_status = update.my_chat_member.new_chat_member.status

        logger.info("Chat %s (%s): status changed %s -> %s", chat.id, chat.title or chat.type, old_status, new_status)

        # If the bot was added (became member or admin) from left/kicked, leave immediately.
        if new_status in ("member", "administrator"):
            # optionally you could send a message here, but it's polite to leave silently
            await context.bot.leave_chat(chat.id)
            logger.info("Left chat %s (%s) after being added.", chat.id, chat.title or chat.type)

    except Exception as e:
        logger.exception("Error handling my_chat_member update: %s", e)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start handler for private chats
    app.add_handler(CommandHandler("start", start_cmd))

    # ChatMemberHandler for updates about the bot's own membership status
    app.add_handler(ChatMemberHandler(my_chat_member_update, chat_member_types=None, block=False))

    logger.info("Starting bot (polling)...")
    app.run_polling()

if __name__ == "__main__":
    main()
