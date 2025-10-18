import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cargar variables del archivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Función que responde al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola mundo!")

# Crear la aplicación con el token
app = ApplicationBuilder().token(TOKEN).build()

# Añadir el comando /start
app.add_handler(CommandHandler("start", start))

# Ejecutar el bot
app.run_polling()
