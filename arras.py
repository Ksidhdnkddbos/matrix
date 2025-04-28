from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from datetime import datetime
import asyncio
import pytz

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
session_string = 'YOUR_SESSION_STRING'

number_map = {
    '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰',
    '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
}

def get_current_timezone():
    return pytz.timezone('Asia/Baghdad')

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# arras
updating_firstname = False
updating_lastname = False

async def update_firstname_loop():
    global updating_firstname
    while updating_firstname:
        now = datetime.now(get_current_timezone())
        current_time = now.strftime("%I:%M")
        fancy_time = ''.join(number_map.get(ch, ch) for ch in current_time)
        try:
            # تحديث الاسم الأول فقط مع الحفاظ على الاسم الأخير الحالي
            full = await client(functions.users.GetFullUserRequest('me'))
            current_last_name = full.user.last_name or None

            await client(functions.account.UpdateProfileRequest(
                first_name=fancy_time,
                last_name=current_last_name
            ))
            print(f"تم تحديث الاسم الأول إلى: {fancy_time}")
        except Exception as e:
            print(f"خطأ بتحديث الاسم الأول: {e}")
        await asyncio.sleep(60)

async def update_lastname_loop():
    global updating_lastname
    while updating_lastname:
        now = datetime.now(get_current_timezone())
        current_time = now.strftime("%I:%M")
        fancy_time = ''.join(number_map.get(ch, ch) for ch in current_time)
        try:
            # تحديث الاسم الأخير فقط مع الحفاظ على الاسم الأول الحالي | arras
            full = await client(functions.users.GetFullUserRequest('me'))
            current_first_name = full.user.first_name or " "

            await client(functions.account.UpdateProfileRequest(
                first_name=current_first_name,
                last_name=fancy_time
            ))
            print(f"تم تحديث اسم العائلة إلى: {fancy_time}")
        except Exception as e:
            print(f"خطأ بتحديث اسم العائلة: {e}")
        await asyncio.sleep(60)

@client.on(events.NewMessage(pattern=r'^\.اسم وقتي$'))
async def start_firstname(event):
    global updating_firstname
    if not updating_firstname:
        updating_firstname = True
        await event.reply("✅ تم تشغيل تحديث الاسم الأول بالوقت")
        client.loop.create_task(update_firstname_loop())
    else:
        await event.reply("⚠️ تحديث الاسم الأول يعمل بالفعل")

@client.on(events.NewMessage(pattern=r'^\.تعطيل اسم وقتي$'))
async def stop_firstname(event):
    global updating_firstname
    if updating_firstname:
        updating_firstname = False
        #arras
        try:
            full = await client(functions.users.GetFullUserRequest('me'))
            current_last_name = full.user.last_name or None
            await client(functions.account.UpdateProfileRequest(first_name=None, last_name=current_last_name))
        except Exception as e:
            print(f"خطأ بإعادة الاسم الأول: {e}")
        await event.reply("🛑 تم إيقاف تحديث الاسم الأول")
    else:
        await event.reply("⚠️ تحديث الاسم الأول موقوف أصلاً")

@client.on(events.NewMessage(pattern=r'^\.اسم وقتي2$'))
async def start_lastname(event):
    global updating_lastname
    if not updating_lastname:
        updating_lastname = True
        await event.reply("✅ تم تشغيل تحديث اسم العائلة بالوقت")
        client.loop.create_task(update_lastname_loop())
    else:
        await event.reply("⚠️ تحديث اسم العائلة يعمل بالفعل")

@client.on(events.NewMessage(pattern=r'^\.تعطيل اسم وقتي2$'))
async def stop_lastname(event):
    global updating_lastname
    if updating_lastname:
        updating_lastname = False
        try:
            full = await client(functions.users.GetFullUserRequest('me'))
            current_first_name = full.user.first_name or " "
            await client(functions.account.UpdateProfileRequest(last_name=None, first_name=current_first_name))
        except Exception as e:
            print(f"خطأ بإعادة اسم العائلة: {e}")
        await event.reply("🛑 تم إيقاف تحديث اسم العائلة")
    else:
        await event.reply("⚠️ تحديث اسم العائلة موقوف أصلاً")

async def main():
    await client.start()
    print("بوت الاسم الوقتي شغال...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
          
