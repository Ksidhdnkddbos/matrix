import os
import sys
from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from config import MATRIXTM, SUDO_USERS, OWNER_NAME, CHANNEL

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("الأحد", 60 * 60 * 24 * 7),
    ("يوم", 60 * 60 * 24),
    ("الساعة", 60 * 60),
    ("الدقيقة", 60),
    ("الثانيه", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.command(["بنك"], prefixes=f"{MATRIXTM}"))
async def ping(client, m: Message):
    await m.delete()
    start = time()
    current_time = datetime.utcnow()
    m_reply = await m.reply_text("🥢")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit(
        f"<b>🏓 بـنـك/b> `{delta_ping * 1000:.3f} بالثانيه` \n<b>⏳ شغال</b> - `{uptime}`"
    )


@Client.on_message(
    filters.user(SUDO_USERS) & filters.command(["اعادة تشغيل"], prefixes=f"{MATRIXTM}")
)
async def restart(client, m: Message):
    await m.delete()
    MUSICTTMATRIX = await m.reply("1")
    await MUSICTTMATRIX.edit("2")
    await MUSICTTMATRIX.edit("3")
    await MUSICTTMATRIX.edit("4")
    await MUSICTTMATRIX.edit("5")
    await MUSICTTMATRIX.edit("6")
    await MUSICTTMATRIX.edit("7")
    await MUSICTTMATRIX.edit("8")
    await MUSICTTMATRIX.edit("9")
    await MUSICTTMATRIX.edit("**تم اعادة تشغيل سورس ماتركس ميوزك ميوزك بنجاح ✓**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@Client.on_message(filters.command(["الاوامر"], prefixes=f"{MATRIXTM}"))
async def help(client, m: Message):
    await m.delete()
    MATRIX = f"""
👋 اهلا {m.from_user.mention}!
[ {OWNER_NAME} ](t.me/{CHANNEL})
——————×—————
🥡 | لتشغيل صوتية في المكالمة أرسل ⇦ [ `{MATRIXTM}تشغيل  + اسم الاغنية` ]
🥡 | لتشغيل فيديو في المكالمة  ⇦ [ `{MATRIXTM}تشغيل_فيديو  + اسم الاغنية` ]
———————×———————
🥡 | لأيقاف الاغنية او الفيديو مؤقتآ  ⇦ [ `{MATRIXTM}استئناف` ] 
🥡 | لأعاده تشغيل الاغنية ⇦  [ `{MATRIXTM}ايقاف_الاستئناف` ]
🥡 | لأيقاف الاغنية  ⇦ [ `{MATRIXTM}ايقاف` ] 
🥡 | لتغطي الاغنية الحالية و تشغيل الاغنية التالية ⇦ [ `{MATRIXTM}تخطي` ]
🥡 | لتشغيل الاغنية عشوائية من قناة او مجموعة  ⇦ [ `{MATRIXTM}اغنيه عشوائية` ]
———————×———————
🥡 | لتحميل صوتية أرسل ⇦ [ `{MATRIXTM}تحميل + اسم الاغنية او الرابط` ]
🥡 | لتحميل فيديو  ⇦  [ `{MATRIXTM}تحميل_فيديو + اسم الاغنية او الرابط` ]
———————×———————
🥡 | لأعاده تشغيل التنصيب أرسل ⇦  [ `{MATRIXTM}ريستارت` ]
———————×———————
المطور : @RNRYR
القناة : @MUSICTTMATRIX
"""
    await m.reply(MATRIX)


@Client.on_message(filters.command(["السورس"], prefixes=f"{MATRIXTM}"))
async def repo(client, m: Message):
    await m.delete()
    MATRIX = f"""
    <b>- اهَـلا {m.from_user.mention}!
🥡 | أެخِتَصِأެصِ هِذِأެ أެݪبَٰۅٛتَ ݪتَشِغِيَݪ مِقِأެطَعَ صِۅٛتَيَة أެۅٛ مِقِأެطَعَ أެݪفَيَدَيَۅٛ فَيَ أެݪمِڪَأެݪمِأެتَ أެݪصِۅٛتَيَة
🥡 | ݪعَࢪضِ أެۅٛأެمِࢪ أެݪسِۅٛࢪسِ أެࢪسِݪ  {MATRIXTM}أެݪأެۅٛأެمِࢪ
🥡 | قِڼِأެة أެݪسِۅٛࢪسِ  : @MUSICTTMATRIX</b>
"""
    await m.reply(MATRIX, disable_web_page_preview=True)