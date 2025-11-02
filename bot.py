# bot.py (python-telegram-bot reference)
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")  # optional

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat = update.effective_chat
        if not chat:
            return

        new_status = update.my_chat_member.new_chat_member.status

        if new_status in ("member", "administrator"):
            if chat.type in ("group", "supergroup", "channel"):
                logger.info("Auto-leaving chat: %s (%s)", chat.title or chat.id, chat.id)
                await context.bot.leave_chat(chat.id)

                if OWNER_ID:
                    try:
                        await context.bot.send_message(
                            chat_id=int(OWNER_ID),
                            text=f"Auto-left chat: {chat.title or chat.id} (id: {chat.id})",
                        )
                    except Exception:
                        logger.exception("Failed to notify owner")

    except Exception:
        logger.exception("Error in my_chat_member handler")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set. Copy .env.example to .env and set BOT_TOKEN")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    logger.info("Starting auto-leaver bot")
    app.run_polling()


if __name__ == "__main__":
    main()
