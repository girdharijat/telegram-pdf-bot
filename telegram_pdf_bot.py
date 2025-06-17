import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PyPDF2 import PdfMerger

TOKEN = "7788617050:AAF2KHqetgXXgDPbPm5HhaCM0R1YWl0UUzw"  # <-- BotFather से मिला टोकन
DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PDF फ़ाइल डाउनलोड करने पर उसे सेव करता है
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type == 'application/pdf':
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOWNLOAD_DIR, document.file_name)
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"✅ PDF saved: {document.file_name}")
    else:
        await update.message.reply_text("❌ Only PDF files are supported.")

# PDF मर्ज करने का कमांड
async def combine_pdfs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    merger = PdfMerger()
    pdf_files = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.pdf')])

    if not pdf_files:
        await update.message.reply_text("❌ No PDFs found to combine.")
        return

    for pdf in pdf_files:
        merger.append(os.path.join(DOWNLOAD_DIR, pdf))

    output_path = os.path.join(DOWNLOAD_DIR, "combined_output.pdf")
    merger.write(output_path)
    merger.close()

    await update.message.reply_document(document=open(output_path, 'rb'))
    await update.message.reply_text("✅ Combined PDF ready!")

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! मुझे PDF भेजो और फिर /combine लिखो मैं सबको जोड़ दूंगा।")

# मुख्य एप्लीकेशन रनर
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("combine", combine_pdfs))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🤖 Bot is running...")
    app.run_polling()
