import asyncio
from pytgcalls import idle
from config import call_py
from MusicMatrix.التشغيل import arq

        
async def main():
    await call_py.start()
    print(
        """
    🥢------------------🥢
🥡 | تم تشغيل ميوزك ماتركس | 🥡
    🥢------------------🥢
"""
    )
    await idle()
    await arq.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
