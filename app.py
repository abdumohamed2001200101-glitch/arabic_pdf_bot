import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import ocrmypdf

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا بوت تحويل PDF إلى نسخة قابلة للبحث. أرسل لي ملف PDF وسأحوله لك.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي ملف PDF وسأجعله قابل للبحث والنسخ")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("يرجى إرسال ملف PDF.")
        return
    
    document = update.message.document
    if document.mime_type != "application/pdf":
        await update.message.reply_text("يرجى إرسال ملف PDF فقط.")
        return
    
    await update.message.reply_text("جاري معالجة الملف...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            file = await document.get_file()
            input_path = os.path.join(tmp_dir, "input.pdf")
            await file.download_to_drive(input_path)
            
            output_path = os.path.join(tmp_dir, "output.pdf")
            
            ocrmypdf.ocr(input_path, output_path, language="ara", force_ocr=True)
            
            await update.message.reply_document(
                document=open(output_path, 'rb'),
                caption="تم تحويل الملف بنجاح! الآن يمكنك البحث والنسخ من النص."
            )
            
        except Exception as e:
            await update.message.reply_text("حدث خطأ. يرجى المحاولة مرة أخرى.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.run_polling()

if __name__ == "__main__":
    main()
