from telethon import TelegramClient, events

api_id = 'YOUR_API_ID'  # جایگزینی با شناسه API خود
api_hash = 'YOUR_API_HASH'  # جایگزینی با هش API خود
bot_token = 'YOUR_BOT_TOKEN'  # جایگزینی با توکن ربات خود

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage)
async def handler(event):
    if event.message.file:
        from_user = event.message.sender_id
        await bot.forward_messages(from_user, event.message, event.chat_id)

with bot:
    bot.run_until_disconnected()￼Enter
