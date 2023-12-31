import os
import schedule
import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events

api_id = 'YOUR_API_ID'  # جایگزینی با شناسه API خود
api_hash = 'YOUR_API_HASH'  # جایگزینی با هش API خود
bot_token = 'YOUR_BOT_TOKEN'  # جایگزینی با توکن ربات خود

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

domain = 'f2l.daboot.tk'  # جایگزینی با دامنه خود

download_path = '/var/www/html/downloads'
if not os.path.exists(download_path):
    os.makedirs(download_path)

def delete_old_files():
    now = datetime.now()

    for filename in os.listdir(download_path):
        file_path = os.path.join(download_path, filename)
        if os.path.getmtime(file_path) < (now - timedelta(hours=24)).timestamp():
            os.remove(file_path)

schedule.every().day.at("00:00").do(delete_old_files)

@bot.on(events.NewMessage)
async def handler(event):
    if event.message.file:
        file = await bot.download_media(event.message, download_path)
        # با استفاده از دامنه خود، URL دانلود را ایجاد می کنیم
        file_name = os.path.basename(file)
        download_url = f'https://{domain}/downloads/{file_name}'
        await event.respond(download_url)

while True:
    bot.run_until_disconnected()
    schedule.run_pending()
    time.sleep(1)
