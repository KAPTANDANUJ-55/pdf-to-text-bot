import os
import tempfile
import pdfplumber
from flask import Flask, request
import telebot

TOKEN = "YOUR_TOKEN"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "🤖 DANUJ PDF BOT is running... Danuj style!"

@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 YO! A VERY WARM WELCOME TO DANUJSIR BOT. PLS SIR/MADAM FORWARD THE PDF AND SEE THE MAGIC!")

@bot.message_handler(content_types=['document'])
def pdf_handler(message):
    if not message.document.file_name.endswith('.pdf'):
        bot.reply_to(message, "GIVE ME PDFFFFFF!")
        return

    bot.reply_to(message, "I FOUND OUT THE PDF HELL YEAH!!!!")

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf.write(downloaded_file)
        temp_pdf.close()

        temp_txt = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        temp_txt.close()

        with pdfplumber.open(temp_pdf.name) as pdf:
            with open(temp_txt.name, "w", encoding="utf-8") as f:
                f.write("------ YO WELCOME TO DANUJ PDF TO TXT CONVERTER ------\n\n")
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        f.write(f"\n--- Page {page_num} ---\n{text}\n")
                    else:
                        f.write(f"\n--- Page {page_num} ---\n[No text found - Might be scanned]\n")

        with open(temp_txt.name, "rb") as txt_file:
            bot.send_document(message.chat.id, txt_file)

        os.remove(temp_pdf.name)
        os.remove(temp_txt.name)

    except Exception as e:
        bot.reply_to(message, f"❌ Oops! Error aaya: {e}")

def set_webhook():
  webhook_url = f"https://danuj-pdf-bot.onrender.com/{TOKEN}"
  success = bot.set_webhook(webhook_url)
  if success:
        print(f"Webhook set to {webhook_url}")
  else:
        print("Webhook setup failed")

if __name__ == '__main__':
    set_webhook()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




