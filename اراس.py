import os
import re
import asyncio
import logging
from telethon import events, TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import GetParticipantRequest, JoinChannelRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from datetime import datetime
import pytz

# إعدادات API (يجب تغييرها!)
api_id = 23240929
api_hash = 'c86e205a2bca8d6381b30a0d7681bba0'

# قائمة المسموح لهم باستخدام أوامر الاسم الوقتي (أضف أرقام المستخدمين الخاص بك)
aRRaS_users = ['123456789', '987654321']  

finalll = TelegramClient(session=None, api_id=api_id, api_hash=api_hash) 
finalll.start()

timezone = pytz.timezone('Asia/Baghdad')
arras_first = False
arras_last = False
final = False  
def decorate_time(time_str):
    number_mapping = {
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰',
        '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    return ''.join([number_mapping.get(char, char) for char in time_str])

async def update_names():
    while arras_first or arras_last:
        now = datetime.now(timezone).strftime("%I:%M")
        decorated_time = decorate_time(now)
        
        first_name = decorated_time if arras_first else None
        last_name = decorated_time if arras_last else None
        
        try:
            await finalll(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            print(f"تم تحديث الاسم الوقتي: {decorated_time}")
        except Exception as e:
            print(f"خطأ في تحديث الاسم: {e}")
        
        await asyncio.sleep(10)

def is_allowed(user_id):
    return str(user_id) in aRRaS_users

@finalll.on(events.NewMessage(outgoing=True, pattern='^.اسم وقتي$'))
async def activate_first_name(event):
    global arras_first
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    if not arras_first:
        arras_first = True
        asyncio.create_task(update_names())
        await event.edit("**✓ تم تفعيل الاسم الوقتي ¹**")
    else:
        await event.edit("**⚠️ الاسم الوقتي مفعل بالفعل!**")

@finalll.on(events.NewMessage(outgoing=True, pattern='^.اسم وقتي2$'))
async def activate_last_name(event):
    global arras_last
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    if not arras_last:
        arras_last = True
        asyncio.create_task(update_names())
        await event.edit("**✓ تم تفعيل الاسم الوقتي ²**")
    else:
        await event.edit("**⚠️ اسم العائلة الوقتي مفعل بالفعل!**")

@finalll.on(events.NewMessage(outgoing=True, pattern='^.تعطيل اسم وقتي$'))
async def deactivate_all(event):
    global arras_first, arras_last
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    arras_first = arras_last = False
    await event.edit("**✗ تم إيقاف الاسم الوقتي بنجاح**")


async def final_nshr(finalll, sleeptimet, chat, message, seconds):
    global final
    final = True
    while final:
        if message.media:
            sent_message = await finalll.send_file(chat, message.media, caption=message.text)
        else:
            sent_message = await finalll.send_message(chat, message.text)
        await asyncio.sleep(sleeptimet)


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.نشر (\d+) (@?\S+)$"))
async def final_handler(event):
    await event.delete()
    parameters = re.split(r'\s+', event.text.strip(), maxsplit=2)
    if len(parameters) != 3:
        return await event.reply("   يجب استخدام كتابة صحيحة الرجاء التاكد من الامر اولا   ")
    seconds = int(parameters[1])
    chat_usernames = parameters[2].split()
    finalll = event.client
    global final
    final = True
    message = await event.get_reply_message()
    for chat_username in chat_usernames:
        try:
            chat = await finalll.get_entity(chat_username)
            await final_nshr(finalll, seconds, chat.id, message, seconds)
        except Exception as e:
            await event.reply(f"   لا يمكن العثور على المجموعة أو الدردشة {chat_username}: {str(e)}")
        await asyncio.sleep(1)


async def final_allnshr(finalll, sleeptimet, message):
    global final
    final = True
    final_chats = await finalll.get_dialogs()
    while final:
        for chat in final_chats:
            if chat.is_group:
                try:
                    if message.media:
                        await finalll.send_file(chat.id, message.media, caption=message.text)
                    else:
                        await finalll.send_message(chat.id, message.text)
                except Exception as e:
                    print(f"Error in sending message to chat {chat.id}: {e}")
        await asyncio.sleep(sleeptimet)


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.نشر_كروبات (\d+)$"))
async def final_handler(event):
    await event.delete()
    seconds = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    message = await event.get_reply_message()
    try:
        sleeptimet = int(seconds[0])
    except Exception:
        return await event.reply("   يجب استخدام كتابة صحيحة الرجاء التاكد من الامر اولا   ")
    finalll = event.client
    global final
    final = True
    await final_allnshr(finalll, sleeptimet, message)


super_groups = ["super", "سوبر"]


async def final_supernshr(finalll, sleeptimet, message):
    global final
    final = True
    final_chats = await finalll.get_dialogs()
    while final:
        for chat in final_chats:
            chat_title_lower = chat.title.lower()
            if chat.is_group and any(keyword in chat_title_lower for keyword in super_groups):
                try:
                    if message.media:
                        await finalll.send_file(chat.id, message.media, caption=message.text)
                    else:
                        await finalll.send_message(chat.id, message.text)
                except Exception as e:
                    print(f"Error in sending message to chat {chat.id}: {e}")
        await asyncio.sleep(sleeptimet)


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.سوبر (\d+)$"))
async def final_handler(event):
    await event.delete()
    seconds = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    message = await event.get_reply_message()
    try:
        sleeptimet = int(seconds[0])
    except Exception:
        return await event.reply("   يجب استخدام كتابة صحيحة الرجاء التاكد من الامر   اولا")
    finalll = event.client
    global final
    final = True
    await final_supernshr(finalll, sleeptimet, message)


@finalll.on(events.NewMessage(outgoing=True, pattern='.ايقاف النشر'))
async def stop_final(event):
    global final
    final = False
    await event.edit("**✧︙ تم ايقاف النشر التلقائي بنجاح ✓  ** ")


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.(الاوامر|فحص|م1|م2|م3|م4)$"))
async def final_handler(event):
    await event.delete()
    cmd = event.pattern_match.group(1)
    if cmd == "م1":
        final_commands = """**
   قـائمة اوامر النشر التلقائي 

=====a R R a S=====

`.نشر` عدد الثواني معرف الكروب :
 - للنشر في المجموعة التي وضعت معرفها مع عدد الثواني

`.نشر_كروبات` عدد الثواني : 
- للنشر في جميع المجموعات الموجوده في حسابك
 
`.سوبر` عدد الثواني : 
- للنشر بكافة المجموعات السوبر التي منظم اليها 

`.تناوب` عدد الثواني : 
- للنشر في جميع المجموعات بالتناوب وحسب الوقت المحدد 

`.خاص` : 
- للنشر في جميع المحادثات الخاصة مرة واحدة فقط

`.نقط` عدد الثواني : 
- للرد على نفس الرسالة ب (.) وحسب الوقت المحدد 

`.مكرر` عدد الثواني : 
- لتكرار نفس الرسالة وحسب الوقت المحدد 

`.سبام` : 
- يرسل الجملة حرف بعد حرف الى ان تنتهي الجملة .

`.وسبام` :
- يرسل الجملة كلمة بعد كلمة

`.ايقاف النشر` :
- لأيقاف جميع انواع النشر اعلاه


• مُـلاحظة : جميع الأوامر اعلاه تستخدم بالرد على الرسالة او الكليشة المُراد نشرها

• مُـلاحظة : جميع الأوامر اعلاه تستقبل صورة واحدة موصوفة بنص وليس اكثر من ذلك 



    **"""
        await event.reply(file='https://graph.org/file/c9f39810c2c98bc40cb8f-1dc0013fad004d4667.jpg', message=final_commands)

    elif cmd == "م2":
        final_wgt = """
 
        ~ .ذاتية
يستخدم لحفظ الصور والفيديوهات المؤقتة (بالرد على الصورة).

       ~ .حفظ الذاتية
سيقوم هذا الامر بعد تفعيلة بحفظ الصور والفيديوهات المؤقته تلقائيا .
"""
        await event.reply(message=final_wgt)

    elif cmd == "م3":
        time_name_commands = """
        **اوامـر الأسـم الوقـتـي**

`.اسم وقتي` 
- تفعيل تحديث الاسم الأول بشكل وقتي.

`.اسم وقتي2` 
- تفعيل تحديث الاسم الأخير بشكل وقتي.

`.تعطيل اسم وقتي` 
- ايقاف الاسم الوقتي.

• الأوامر تعمل فقط للمستخدمين المسموح لهم.
"""
        await event.reply(message=time_name_commands)

    elif cmd == "م4":
        search_download_commands = """
        **او مـر البـحث والتحـميل**

`.بحث <اسم الأغنية أو الفيديو>` 
- للبحث عن أغنية .

~ الشرح: استخدم الأمر بالرد على رسالة أو لوحده مع اسم ما تريد البحث عنه.

"""
        await event.reply(message=search_download_commands)

    elif cmd == "فحص":
        final_check = "**سورس aRRaS يعمل \nلعرض قائمة الاوامر أرسل `.الاوامر`**"
        await event.reply(file='https://graph.org/file/ae3f77349a9a7c5c3627c-fd40a37dff94a02eae.jpg', message=final_check)

    elif cmd == "الاوامر":
        final_nshr = """
 
        ⋆┄─┄a R R a S─┄┄⋆
       ` .م1 ` ➪ اوامــر النشــر التلقــائي
       ` .م2 ` ➪ اوامــر الـذاتيــة
       ` .م3 ` ➪ اوامـر الأسـم الوقـتـي
       ` .م4 ` ➪ اوامر البحث والتحـميل
        ⋆┄─┄ @Lx5x5┄┄┄⋆
"""
        await event.reply(message=final_nshr)
      


from os import remove

auto_save_enabled = False

@finalll.on(events.NewMessage(outgoing=True, pattern=r'\.واو|\.حفظ الذاتية'))
async def rundrc(event):
    await event.delete()
    if event.pattern_match.group(0) == ".ذاتية":
        try:
            getrestrictedcontent = await event.get_reply_message()
            downloadrestrictedcontent = await getrestrictedcontent.download_media()
            await event.client.send_file("me", downloadrestrictedcontent)
            remove(downloadrestrictedcontent)
        except:
            pass
    elif event.pattern_match.group(0) == ".حفظ الذاتية":
        global auto_save_enabled
        auto_save_enabled = not auto_save_enabled
        if auto_save_enabled:
            await event.respond("تم تفعيل حفظ الوسائط ذاتية التدمير تلقائيًا.")
        else:
            await event.respond("تم إيقاف حفظ الوسائط ذاتية التدمير تلقائيًا.")

@finalll.on(events.NewMessage)
async def auto_save_media(event):
    if auto_save_enabled:
        try:
            if event.media and event.media.ttl_seconds:
                downloadrestrictedcontent = await event.download_media()
                await event.client.send_file("me", downloadrestrictedcontent)
                remove(downloadrestrictedcontent)
        except:
            pass


@finalll.on(events.NewMessage(outgoing=True, pattern=r'^\.بحث (.*)'))
async def search_music(event):
    # الحصول على النص بعد الأمر
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("**⚠️ يرجى كتابة ما تريد البحث عنه بعد الأمر .بحث**")
        return
    
    try:
        
        try:
            await finalll(GetParticipantRequest('@B_a_r', await finalll.get_me()))
            
        except UserNotParticipantError:
            
            try:
                await finalll(JoinChannelRequest('@B_a_r'))
                await asyncio.sleep(2)  
            except Exception as e:
                print(f"حدث خطأ في الانضمام للقناة: {e}")

        
        msg = await event.edit("**⌛ جاري البحث عن الأغنية...**")
        await finalll.send_message('@BaarxXxbot', f'يوت {query}')
        
        await asyncio.sleep(4)
        
        async for message in finalll.iter_messages('@BaarxXxbot', limit=1):
            if message.media:
                
                await msg.delete()  
                await finalll.send_file(
                    event.chat_id,
                    message.media,
                    caption="• uploader @Lx5x5",
                    reply_to=event.message.reply_to_msg_id
                )
                
                await finalll(DeleteHistoryRequest(peer='@BaarxXxbot', max_id=0, just_clear=True))
                
            elif message.text:
                await event.edit(f"{message.text}")
            else:
                await event.edit("**❌ لم يتم العثور على نتيجة**")

    except Exception as e:
        await event.edit(f"**❌ حدث خطأ: {str(e)}**")
        print(f"Error in search_music: {e}")


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.تناوب (\d+)$"))
async def rotate_handler(event):
    await event.delete()
    seconds = int(event.pattern_match.group(1))
    message = await event.get_reply_message()
    if not message:
        return await event.reply("   يجب الرد على رسالة لاستخدام هذا الأمر.")

    global final
    final = True
    chats = await finalll.get_dialogs()
    groups = [chat for chat in chats if chat.is_group]
    num_groups = len(groups)
    current_group_index = 0

    while final:
        try:
            if message.media:
                await finalll.send_file(groups[current_group_index].id, message.media, caption=message.text)
            else:
                await finalll.send_message(groups[current_group_index].id, message.text)
        except Exception as e:
            print(f"Error in sending message to chat {groups[current_group_index].id}: {e}")

        current_group_index = (current_group_index + 1) % num_groups
        await asyncio.sleep(seconds)


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.خاص$"))
async def private_handler(event):
    await event.delete()
    message = await event.get_reply_message()
    if not message:
        return await event.reply("   يجب الرد على رسالة لاستخدام هذا الأمر.")

    chats = await finalll.get_dialogs()
    private_chats = [chat for chat in chats if chat.is_user]

    for chat in private_chats:
        try:
            if message.media:
                await finalll.send_file(chat.id, message.media, caption=message.text)
            else:
                await finalll.send_message(chat.id, message.text)
        except Exception as e:
            print(f"Error in sending message to chat {chat.id}: {e}")


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.نقط (\d+)$"))
async def dot_handler(event):
    await event.delete()
    seconds = int(event.pattern_match.group(1))
    reply_to_msg = await event.get_reply_message()
    if not reply_to_msg:
        return await event.reply("   يجب الرد على رسالة لاستخدام هذا الأمر.")

    global final
    final = True

    while final:
        await reply_to_msg.reply(".")
        await asyncio.sleep(seconds)


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.مكرر (\d+)$"))
async def repeat_handler(event):
    await event.delete()
    seconds = int(event.pattern_match.group(1))
    message = await event.get_reply_message()
    if not message:
        return await event.reply("   يجب الرد على رسالة لاستخدام هذا الأمر.")

    global final
    final = True

    while final:
        await message.respond(message)
        await asyncio.sleep(seconds)


print('تم تشغيل السورس  | تعديل arras')
finalll.run_until_disconnected()
      
