import asyncio
import os
from datetime import datetime
from telethon import TelegramClient, events
from aiohttp import web

# --- CONFIGURATION ---
API_ID = 37236703
API_HASH = 'a6d70fd6d0f99283ec4eea089e0ea397'
WATCHDOG_TOKEN = '8629010489:AAEM8pm6wDQPPVHJjFlYGi3d7-YMWO3TaTs'
OWNER_ID = 2076808668

bot = TelegramClient('watchdog_session', API_ID, API_HASH)
last_ping_time = datetime.now()
is_offline = False

@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def handler(event):
    global last_ping_time, is_offline
    # Jaise hi Termux (Agent 1) se ALIVE aayega, timer reset
    if event.raw_text == "ALIVE":
        last_ping_time = datetime.now()
        if is_offline:
            await bot.send_message(OWNER_ID, "✅ Badi Achi Khabar! Termux Code wapas chalu ho gaya hai!")
            is_offline = False

async def watchdog_task():
    global is_offline
    await bot.wait_until_ready()
    # Code start hone ke baad pehle 60 sec chup rahega
    await asyncio.sleep(60) 
    while True:
        await asyncio.sleep(15) 
        time_diff = (datetime.now() - last_ping_time).total_seconds()
        
        # 90 second tak message nahi aaya toh Alert bajega
        if time_diff > 90:
            is_offline = True
            try:
                await bot.send_message(OWNER_ID, "🚨 WAKE UP PROFESSOR! Termux me code band ho gaya hai ya internet chala gaya hai! Jaldi check karo! 🚨")
            except Exception:
                pass
            await asyncio.sleep(45) # Alert ke baad 45 sec ruk kar fir spam karega

# --- RENDER KE LIYE DUMMY WEB SERVER ---
async def handle(request):
    return web.Response(text="Watchdog is Alive & Running on Render!")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await bot.start(bot_token=WATCHDOG_TOKEN)
    bot.loop.create_task(watchdog_task())
    bot.loop.create_task(web_server())
    print("🐶 Watchdog Cloud Par Jag Raha Hai...")
    
    # Aapke number par message karega ki wo on ho gaya hai
    try: await bot.send_message(OWNER_ID, "🐶 Watchdog system ON! Main nigrani rakh raha hu...")
    except: pass
    
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
