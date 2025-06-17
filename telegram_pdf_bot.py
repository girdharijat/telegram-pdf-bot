from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PyPDF2 import PdfMerger
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7788617050:AAF2KHqetgXXgDPbPm5HhaCM0R1YWl0UUzw"  # ✅ अपना TOKEN यहाँ डालो

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working! Send me PDF files and then /combine")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc.mime_type == "application/pdf":
        file = await context.bot.get_file(doc.file_id)
        path = os.path.join(DOWNLOAD_DIR, doc.file_name)
        await file.download_to_drive(path)
        await update.message.reply_text(f"✅ Saved: {doc.file_name}")
    else:
        await update.message.reply_text("❌ Send only PDF files.")

async def combine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    merger = PdfMerger()
    files = sorted(f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".pdf"))
    if not files:
        await update.message.reply_text("❌ No PDFs found.")
        return
    for pdf in files:
        merger.append(os.path.join(DOWNLOAD_DIR, pdf))
    out = os.path.join(DOWNLOAD_DIR, "combined.pdf")
    merger.write(out); merger.close()
    await update.message.reply_text("🔧 Combining done.")
    await update.message.reply_document(document=open(out, "rb"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(CommandHandler("combine", combine))
    print("Bot started successfully!")
    app.run_polling()
