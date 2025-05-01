import os
import re
import asyncio
import logging
from telethon import events, TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz

# إعدادات API (يجب تغييرها!)
api_id = 23240929
api_hash = 'c86e205a2bca8d6381b30a0d7681bba0'

# قائمة المسموح لهم باستخدام أوامر الاسم الوقتي (أضف أرقام المستخدمين الخاص بك)
allowed_users = ['123456789', '987654321']  # غيرها إلى أرقامك!

finalll = TelegramClient(session=None, api_id=api_id, api_hash=api_hash) 
finalll.start()

# متغيرات الاسم الوقتي
timezone = pytz.timezone('Asia/Baghdad')
running_first = False
running_last = False
final = False  # متغير النشر التلقائي (من الكود الأصلي)

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
            await finalll(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            print(f"تم تحديث الاسم الوقتي: {decorated_time}")
        except Exception as e:
            print(f"خطأ في تحديث الاسم: {e}")
        
        await asyncio.sleep(10)

def is_allowed(user_id):
    return str(user_id) in allowed_users

# ========= أوامر الاسم الوقتي =========
@finalll.on(events.NewMessage(outgoing=True, pattern='^.اسم وقتي$'))
async def activate_first_name(event):
    global running_first
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    if not running_first:
        running_first = True
        asyncio.create_task(update_names())
        await event.edit("**✓ تم تفعيل الاسم الوقتي (الاسم الأول)**")
    else:
        await event.edit("**⚠️ الاسم الوقتي مفعل بالفعل!**")

@finalll.on(events.NewMessage(outgoing=True, pattern='^.اسم وقتي2$'))
async def activate_last_name(event):
    global running_last
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    if not running_last:
        running_last = True
        asyncio.create_task(update_names())
        await event.edit("**✓ تم تفعيل الاسم الوقتي (اسم العائلة)**")
    else:
        await event.edit("**⚠️ اسم العائلة الوقتي مفعل بالفعل!**")

@finalll.on(events.NewMessage(outgoing=True, pattern='^.تعطيل اسم وقتي$'))
async def deactivate_all(event):
    global running_first, running_last
    if not is_allowed(event.sender_id):
        return await event.edit("**⚠️ ليس لديك صلاحية استخدام هذا الأمر!**")
    
    running_first = running_last = False
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
    await event.edit("**  ︙ تم ايقاف النشر التلقائي بنجاح ✓  ** ")


@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.(الاوامر|فحص|م1|م2)$"))
async def final_handler(event):
    await event.delete()
    if event.pattern_match.group(1) == "م1":
        final_commands = """**
   قـائمة اوامر النشر التلقائي 

===== F i n a L=====

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
        await event.reply(file='https://graph.org/file/bc08fcf7de6be2a88057a-76431830a0d3ffd01d.jpg', message=final_commands)
    elif event.pattern_match.group(1) == "فحص":
        final_check = "**سورس F IN A L يعمل \nلعرض قائمة الاوامر أرسل `.الاوامر`**"
        await event.reply(file='https://graph.org/file/bc08fcf7de6be2a88057a-76431830a0d3ffd01d.jpg', message=final_check)
    elif event.pattern_match.group(1) == "الاوامر":
        final_nshr = """
 
        ⋆┄─┄F I N A L─┄┄⋆
       ` .م1 ` ➪ اوامــر النشــر التلقــائي
       ` .م2 ` ➪ اوامــر الـذاتيــة
        ⋆┄─┄ @i0i0ii┄┄┄⋆
"""
        await event.reply(message=final_nshr)
    elif event.pattern_match.group(1) == "م2":
        final_wgt = """
 
        ~ .ذاتية
يستخدم لحفظ الصور والفيديوهات المؤقتة (بالرد على الصورة).

       ~ .حفظ الذاتية
سيقوم هذا الامر بعد تفعيلة بحفظ الصور والفيديوهات المؤقته تلقائيا .
"""
        await event.reply(message=final_wgt)


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
        # الانضمام التلقائي للقناة
        try:
            await finalll(JoinChannelRequest('@B_a_r'))
            await asyncio.sleep(2)  # انتظار 2 ثانية بعد الانضمام
        except Exception as e:
            print(f"حدث خطأ في الانضمام للقناة: {e}")

        # إرسال الطلب إلى بوت الموسيقى
        await event.edit("**⌛ جاري البحث عن الأغنية...**")
        await finalll.send_message('@BaarxXxbot', f'يوت {query}')
        
        # الانتظار 5 ثواني قبل التحقق من الرد
        await asyncio.sleep(5)

        # استلام الرد من البوت
        async with finalll.conversation('@BaarxXxbot', timeout=15) as conv:
            try:
                response = await conv.get_response()
                
                # إذا كانت هناك ميديا (أغنية)
                if response.media:
                    await event.delete()  # حذف رسالة "جاري البحث"
                    await event.client.send_file(
                        event.chat_id,
                        response.media,
                        caption="",
                        reply_to=event.message.reply_to_msg_id if event.message.reply_to_msg_id else None
                    )
                    return  # إنهاء الوظيفة بعد إرسال الميديا بنجاح
                
                # إذا كان نص فقط
                if response.text:
                    await event.edit(response.text)
                
            except Exception as e:
                print(f"حدث خطأ في معالجة الرد: {e}")

    except asyncio.TimeoutError:
        await event.edit("**⏳ انتهى وقت الانتظار للرد من البوت**")
    except Exception as e:
        # لا تعرض رسالة الخطأ إذا تم إرسال الميديا بنجاح
        if "No message was sent previously" not in str(e):
            await event.edit(f"**❌ حدث خطأ: {str(e)}**")
        print(f"Error in search_music: {e}")

@finalll.on(events.NewMessage(outgoing=True, pattern=r"^\.وسبام$"))
async def word_spam_handler(event):
    await event.delete()
    message = await event.get_reply_message()
    if not message or not message.text:
        return await event.reply("   يجب الرد على رسالة نصية لاستخدام هذا الأمر.")

    words = message.text.split()
    for word in words:
        await event.respond(word)
        await asyncio.sleep(1)


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


print('تم تشغيل النشر التلقائي لسورس')
finalll.run_until_disconnected()
