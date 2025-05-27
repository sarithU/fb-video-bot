from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

import os
TOKEN = os.getenv('7930864892:AAEnEgr80sWZQWQV1IXU97QqhzDVmtxV3k4')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me a Facebook video link!')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('Downloading video...')

    ydl_opts = {
        'outtmpl': 'fb_video.%(ext)s',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith('fb_video'):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)

    except Exception as e:
        await update.message.reply_text(f'Failed to download video: {e}')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()

if __name__ == '__main__':
    main()
