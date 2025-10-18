import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# Obtener token y URL desde las variables de entorno de Render
TOKEN = os.getenv("7709737711:AAHCN8hgp27p_LSw9rLqjQhw6LffGd0swME")
BOT_URL = os.getenv("BOT_URL")

# Crear la aplicación de Telegram
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Función que responde al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola mundo!")

# Añadir el comando /start
telegram_app.add_handler(CommandHandler("start", start))

# Crear la app de Flask
app = Flask(__name__)

# Ruta para recibir mensajes de Telegram (webhook)
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

# Ruta principal para probar que la app está viva
@app.route("/")
def home():
    return "Bot funcionando en Render", 200

# Arrancar la app y registrar el webhook con Telegram
if __name__ == "__main__":
    bot = Bot(TOKEN)
    asyncio.run(bot.set_webhook(f"{BOT_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
