import os
import telebot
import pytesseract
from pdf2image import convert_from_path

# Load Telegram Bot Token from Environment Variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Directory to store uploaded PDFs
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Handle start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a PDF with MCQ questions or answers.")

# Handle PDF files
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # Download the PDF
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        # Save the file locally
        file_name = os.path.join(UPLOAD_FOLDER, message.document.file_name)
        with open(file_name, "wb") as f:
            f.write(downloaded_file)

        # Convert PDF to images and extract text
        text = extract_text_from_pdf(file_name)
        bot.reply_to(message, "Extracted text:\n" + text[:4000])  # Telegram limit
    except Exception as e:
        bot.reply_to(message, f"Error processing the PDF: {str(e)}")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"
    return extracted_text

# Start polling
bot.polling()
