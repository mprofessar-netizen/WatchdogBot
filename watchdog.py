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
    # Jaise hi ALIVE message aata hai
    if event.raw_text == "ALIVE":
        last_ping_time = datetime.now()
        
        # Agar pehle offline tha, toh ab ek baar 'Back Online' message bhejega
        if is_offline:
            is_offline = False
            try:
                await bot.send_message(OWNER_ID, "✅ Badi Achi Khabar! Termux Code wapas chalu ho gaya hai!")
            except Exception:
                pass

async def watchdog_task():
    global is_offline

    # Startup delay taaki bot properly start ho jaye
    await asyncio.sleep(60) 

    while True:
        try:
            await asyncio.sleep(15) 
            
            time_diff = (datetime.now() - last_ping_time).total_seconds()
            
            # Debugging ke liye: Render Logs me dikhega ki watchdog chal raha hai
            print(f"time_diff = {time_diff}")
            
            # Agar 90 seconds tak ALIVE nahi aaya, toh OFFLINE maan lo
            if time_diff > 90:
                
                # Sirf ek baar OFFLINE mark karega
                if not is_offline:
                    is_offline = True
                    print("Bot is OFFLINE")
                
                current_time = datetime.now().strftime("%I:%M:%S %p")
                alert_msg = f"🚨 WAKE UP PROFESSOR! 🚨\n\nTermux me code band ho gaya hai ya internet chala gaya hai!\n\n⏳ Time: {current_time}"
                
                await bot.send_message(OWNER_ID, alert_msg)
                print(f"Alert sent at {current_time}")
                
                # Alert bhejne ke baad 45 seconds rukega (total ~60 sec loop), taaki spam na ho
                await asyncio.sleep(45) 
                
        except Exception as e:
            # Agar koi error aaye toh task crash nahi hoga, bas print karke continue karega
            print(f"Watchdog Error: {e}")
            await asyncio.sleep(5)

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
    
    try: 
        await bot.send_message(OWNER_ID, "🐶 Watchdog system ON! Main nigrani rakh raha hu...")
    except: 
        pass
    
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
