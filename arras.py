from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.messages import EditMessageRequest
from datetime import datetime
import pytz
import asyncio
import os

api_id = 23725562
api_hash = 'f72417e564acce43e1143e2b797c73fb'
session_string = "YOUR_SESSION_STRING_HERE"

aRRaS_USER_IDS = ['7872828412', '6349091574']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

timezone = pytz.timezone('Asia/Baghdad')
running_first = False
running_last = False

def decorate_time(time_str):
    number_mapping = {
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰',
        '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    return ''.join([number_mapping.get(char, char) for char in time_str])

async def update_names():
    while running_first or running_last:
        now = datetime.now(timezone).strftime("%I:%M")
        decorated_time = decorate_time(now)
        
        first_name = decorated_time if running_first else None
        last_name = decorated_time if running_last else None
        
        try:
            await client(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            print(f"تم التحديث: الاسم الأول ({first_name}) | العائلة ({last_name})")
        except Exception as e:
            print(f"خطأ: {e}")
        
        await asyncio.sleep(10)

def is_allowed(user_id):
    return str(user_id) in aRRaS_USER_IDS

async def edit_command_message(event, new_text):
    try:
        await client.edit_message(
            await event.get_input_chat(),
            event.message.id,
            new_text
        )
    except Exception as e:
        print(f"خطأ في تعديل الرسالة: {e}")

@client.on(events.NewMessage(pattern='^.اسم وقتي$'))
async def activate_first_name(event):
    global running_first
    if not is_allowed(event.sender_id):
        return
    
    if not running_first:
        running_first = True
        asyncio.create_task(update_names())
        await edit_command_message(event, "✓ تم تفعيل الاسم الوقتي  ¹")
    else:
        await edit_command_message(event, "⚠ الاسم الوقتي  ¹ مفعل مسبقا .")

@client.on(events.NewMessage(pattern='^.الاوامر$'))
async def show_commands(event):
    if not is_allowed(event.sender_id):
        return
    
    commands = """
⚡️ قائمة الأوامر :

1. `.اسم وقتي` - تفعيل الاسم الأول الوقتى
2. `.اسم وقتي2` - تفعيل اسم العائلة الوقتى
3. `.تعطيل اسم وقتي` - إيقاف كلا الاسمين
"""
    await edit_command_message(event, commands)

@client.on(events.NewMessage(pattern='^.اسم وقتي2$'))
async def activate_last_name(event):
    global running_last
    if not is_allowed(event.sender_id):
        return
    
    if not running_last:
        running_last = True
        asyncio.create_task(update_names())
        await edit_command_message(event, "✓ تم تفعيل الاسم الوقتي ²")
    else:
        await edit_command_message(event, "⚠ اسم الوقتي ² مفعل مسبقا .")

@client.on(events.NewMessage(pattern='^.تعطيل اسم وقتي$'))
async def deactivate_all(event):
    global running_first, running_last
    if not is_allowed(event.sender_id):
        return
    
    running_first = running_last = False
    await edit_command_message(event, "✗ تم تعطيل كافة الأسماء الوقتية")



async def main():
    await client.start()
    print("✅ البوت يعمل الآن")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
