import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, types

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "7830753415:AAFp5QZjXYZKOPQpTjUjW0cCQ4ExoGFOZK4")
OWNER_ID = os.getenv("OWNER_ID")  # optional

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Client("auto-leaver-bot", bot_token=BOT_TOKEN)


@app.on_my_chat_member()  # ✅ correct decorator
async def on_my_chat_member(client: Client, chat_member: types.ChatMemberUpdated):
    """Triggered when the bot's own chat status changes."""
    try:
        new = chat_member.new_chat_member
        if not new or not new.user:
            return

        # Make sure the update is about the bot itself
        bot = await client.get_me()
        if new.user.id != bot.id:
            return

        status = new.status  # 'member', 'administrator', 'left', etc.

        # Leave any non-private chat when added
        if status in ("member", "administrator"):
            chat = chat_member.chat
            if chat.type in ("group", "supergroup", "channel"):
                logger.info("Auto-leaving chat: %s (%s)", chat.title or chat.id, chat.id)
                await client.leave_chat(chat.id)

                if OWNER_ID:
                    try:
                        await client.send_message(
                            int(OWNER_ID),
                            f"🚪 Auto-left chat: {chat.title or chat.id} (id: {chat.id})",
                        )
                    except Exception:
                        logger.exception("Failed to notify owner")

    except Exception:
        logger.exception("Error in on_my_chat_member handler")


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set. Copy .env.example to .env and set BOT_TOKEN")
    app.run()
