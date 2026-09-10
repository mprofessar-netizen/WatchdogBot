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
    if not db_ref.child(user_id).get():
        db_ref.child(user_id).set({
            'start_time': datetime.now().timestamp(),
            'msg1': False, 
            'msg2': False
        })

async def checker():
    while True:
        users = db_ref.get() or {}
        now = datetime.now().timestamp()
        
        for uid, data in users.items():
            start_time = data.get('start_time', now)
            diff_hours = (now - start_time) / 3600
            
            # 6 Ghante baad pehla msg
            if diff_hours >= 6 and not data.get('msg1'):
                try:
                    await bot.send_message(int(uid), MSG_TEXT)
                    db_ref.child(uid).update({'msg1': True})
                except: pass
            
            # 12 Ghante baad dusra msg
            if diff_hours >= 12 and not data.get('msg2'):
                try:
                    await bot.send_message(int(uid), MSG_TEXT)
                    db_ref.child(uid).update({'msg2': True})
                except: pass
                    
        await asyncio.sleep(300) # Har 5 minute me check karega

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    bot.loop.create_task(checker())
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
