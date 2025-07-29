import google.generativeai as genai
from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELE_TOKEN_KEY = os.getenv("tele_token_key")
GENAI_TOKEN_KEY = os.getenv("gemini_token_key")

genai.configure(api_key=GENAI_TOKEN_KEY)
model = genai.GenerativeModel("gemini-1.5-flash",
                              generation_config={"max_output_tokens": 500}  
                              )


async def query_gemini(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: Could not connect to Gemini API - {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I'm your Computer Science Q&A bot powered by Gemini. Ask me any CS question!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = await query_gemini(user_message)
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TELE_TOKEN_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()