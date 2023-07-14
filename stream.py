import os
from telethon.sync import TelegramClient, events
from instaloader import Instaloader, Post, Profile

API_ID = 'your_telegram_api_id'  # replace with your API ID
API_HASH = 'your_telegram_api_hash'  # replace with your API Hash
BOT_TOKEN = 'your_bot_token'  # replace with your Bot Token

# create a instaloader instance
L = Instaloader()

# create a telegram client instance
with TelegramClient('anon', API_ID, API_HASH).start(bot_token=BOT_TOKEN) as client:

    @client.on(events.NewMessage)
    async def my_event_handler(event):
        if 'instagram.com' in event.raw_text:
            url = event.raw_text
            is_story = 'stories' in url

            if is_story:
                username, story_id = url.split('/')[-3], url.split('/')[-2]
                profile = Profile.from_username(L.context, username)

                for story in L.get_stories(userids=[profile.userid]):
                    for item in story.get_items():
                        if str(item.mediaid) == story_id and item.is_video:
                            video_url = item.video_url
                            await client.send_file(event.chat_id, video_url)
                            break
            else:
                shortcode = url.split('/')[-2]
                post = Post.from_shortcode(L.context, shortcode)

                if post.is_video:
                    video_url = post.video_url
                    await client.send_file(event.chat_id, video_url)

    client.run_until_disconnected()
