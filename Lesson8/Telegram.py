from telethon import TelegramClient
import time
api_id = 766231
api_hash = '20e0059a476a0472781f6e42c333c084'

client = TelegramClient('test_tg',api_id,api_hash)

async def main():
    # me = await client.get_me()
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.title == 'GU_BigData_327 (20.12.2019)':
            # await dialog.send_message('Привет всем!')
            # async for msg in client.iter_messages(dialog):
            #     if msg.media:
            #         await msg.download_media()
            #     print(msg.date, msg.text)
            #     time.sleep(1)
            members = await client.get_participants(dialog)

    for member in members:
        print(member.first_name, member.last_name)
    pass

with client:
    client.loop.run_until_complete(main())