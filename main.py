import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_URL = os.getenv("BOT_URL")  # URL pública de tu app en Render

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola mundo!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot funcionando en Render", 200

if __name__ == "__main__":
    import asyncio
    from telegram import Bot
    bot = Bot(TOKEN)
    asyncio.run(bot.set_webhook(f"{BOT_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
