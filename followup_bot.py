import asyncio
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from telethon import TelegramClient, events

# --- CONFIG ---
API_ID = 37236703
API_HASH = 'a6d70fd6d0f99283ec4eea089e0ea397'
BOT_TOKEN = '8684849367:AAGkmccGzBk0MGZqdz04oP7k-5JsQBXN8c0'

MSG_TEXT = """Hello Sir,
Aapke 100 Subscribers pending status mein hain. Kripya 100 coins complete kar lijiye, uske baad aap apne 100 Permanent Subscribers turant collect kar sakte hain.
Thank you. 💝"""

# --- FIREBASE SETUP ---
cred = credentials.Certificate("planning-with-ai-33791-firebase-adminsdk-fbsvc-e2afdebd7b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://planning-with-ai-33791-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
db_ref = db.reference('youtube20_bot_users')

bot = TelegramClient('youtube20sub_session', API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/start', func=lambda e: e.is_private))
async def start_handler(event):
    user_id = str(event.sender_id)
    # TEST MODE: Jab bhi koi /start dabayega, timer fresh zero se start hoga
    db_ref.child(user_id).set({
        'start_time': datetime.now().timestamp(),
        'msg1': False, 
        'msg2': False
    })
    print(f"Test Mode: Timer reset for user {user_id}")

async def checker():
    while True:
        users = db_ref.get() or {}
        now = datetime.now().timestamp()
        
        for uid, data in users.items():
            start_time = data.get('start_time', now)
            # Time ko ab ghante ki jagah minutes me check kar rahe hain
            diff_minutes = (now - start_time) / 60 
            
            # 1 Minute baad pehla msg
            if diff_minutes >= 1 and not data.get('msg1'):
                try:
                    await bot.send_message(int(uid), MSG_TEXT)
                    db_ref.child(uid).update({'msg1': True})
                    print(f"Test: 1 Min wala msg sent to {uid}")
                except Exception as e:
                    print(f"Error {uid}: {e}")
            
            # 2 Minute baad dusra msg
            if diff_minutes >= 2 and not data.get('msg2'):
                try:
                    await bot.send_message(int(uid), MSG_TEXT)
                    db_ref.child(uid).update({'msg2': True})
                    print(f"Test: 2 Min wala msg sent to {uid}")
                except Exception as e:
                    pass
                    
        # Jaldi check karne ke liye 5 min ki jagah ab har 15 second mein check karega
        await asyncio.sleep(15) 

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("✅ Bot Test Mode Mein Start Ho Gaya Hai!")
    bot.loop.create_task(checker())
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
