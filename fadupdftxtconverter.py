import pdfplumber
import os
import tempfile
import telebot

TOKEN = "7339710265:AAFkeQdtkOA5B9N4RV6E3JDr-mvgIRfx0zA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 YO! A VERY WARM WELCOME TO DANUJSIR BOT. PLS SIR/MADAM FORWARD THE PDF AND SEE THE MAGIC!")

@bot.message_handler(content_types='document')
def pdf_handler(message):
    # Check karo ki file PDF hai ya nahi
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

print("🤖 DANUJ PDF BOT is running on Telegram...")
bot.infinity_polling()

