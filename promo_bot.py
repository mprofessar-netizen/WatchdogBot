import os
import re
import json
import asyncio
import random
from datetime import datetime, timedelta, timezone

from telethon import TelegramClient, Button
from telethon.sessions import MemorySession

# ================= CONFIG =================
API_ID = 37236703
API_HASH = 'a6d70fd6d0f99283ec4eea089e0ea397'
BOT_TOKEN = '7721954754:AAFSNi7iBj--zCGxJI6zE-TTypJ052yG14c'

TARGET_CHANNEL = '@LootRadarIndia'
BUTTON_LINK = 'https://t.me/Youtube20Sub_bot'

IST = timezone(timedelta(hours=5, minutes=30))
STATE_FILE = "bot_state.json"

# ================= RAW DATA (YAHAN COPY PASTE KAREIN) =================
GOLDEN_RAW_TEXT = """
[AAPKI GOLDEN LIST YAHAN HOGI - Purana wala hi rehne dena]
"""

NORMAL_RAW_TEXT = """
[AAPKI NORMAL LIST YAHAN HOGI - Purana wala hi rehne dena]
"""

# ================= DATA PARSERS =================
def load_golden_data(raw_text):
    results = []
    pattern = re.compile(r'([^\n]+)\n+(https?://[^\n]+)')
    for m in pattern.finditer(raw_text):
        results.append({'name': m.group(1).strip(), 'total': '1000', 'link': m.group(2).strip()})
    return results

def load_normal_data(raw_text):
    results = []
    pattern1 = re.compile(r'👤 (?:User:\s*)?([^\n]+)\n+🎯 (?:Target:\s*)?(\d+)\s*Subs\n+🔗 (?:Link:\s*)?(https?://[^\n]+)', re.IGNORECASE)
    for m in pattern1.finditer(raw_text):
        results.append({'name': m.group(1).strip(), 'total': m.group(2).strip(), 'link': m.group(3).strip()})
    
    clean_text = pattern1.sub('', raw_text)
    pattern2 = re.compile(r'([^\n]+)\n+(100|120|200)\n+(https?://[^\n]+)')
    for m in pattern2.finditer(clean_text):
        results.append({'name': m.group(1).strip(), 'total': m.group(2).strip(), 'link': m.group(3).strip()})
    
    return results

GOLDEN_DATA = load_golden_data(GOLDEN_RAW_TEXT)
NORMAL_DATA = load_normal_data(NORMAL_RAW_TEXT)

# ================= STATE MANAGEMENT (NO REPEATS) =================
state = {
    "current_day_str": None,
    "daily_queue": [],
    "normal_pool": [],
    "golden_pool": []
}

def load_state():
    global state
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                saved_state = json.load(f)
                state.update(saved_state)
                print("📂 Previous state loaded! Continuing exactly from where we left off.")
        except Exception as e:
            print("⚠️ Could not load state file, starting fresh.", e)

def save_state():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print("⚠️ Failed to save state:", e)

def reset_daily_queue():
    now = datetime.now(IST)
    today_str = str(now.date())
    
    # 377 RULE: Check if BOTH pools are fully exhausted
    if not state["normal_pool"] and not state["golden_pool"]:
        print("🔄 All 377 messages exhausted! Starting a brand new cycle.")
        state["normal_pool"] = NORMAL_DATA.copy()
        random.shuffle(state["normal_pool"])
        state["golden_pool"] = GOLDEN_DATA.copy()
        random.shuffle(state["golden_pool"])
        
    # Failsafe: if only one got empty slightly early due to division
    if not state["normal_pool"]:
        state["normal_pool"] = NORMAL_DATA.copy()
        random.shuffle(state["normal_pool"])
    if not state["golden_pool"]:
        state["golden_pool"] = GOLDEN_DATA.copy()
        random.shuffle(state["golden_pool"])

    # Din ki limit nikalna: ~43 Normal aur ~11 Golden
    normals_for_today = []
    for _ in range(min(43, len(state["normal_pool"]))):
        proof = state["normal_pool"].pop(0).copy()
        proof['type'] = 'N'
        normals_for_today.append(proof)
        
    goldens_for_today = []
    for _ in range(min(11, len(state["golden_pool"]))):
        proof = state["golden_pool"].pop(0).copy()
        proof['type'] = 'G'
        goldens_for_today.append(proof)

    # UNPREDICTABLE PATTERN MIXING: Har 2, 3, 4 ya 5 normal ke baad 1 golden
    daily_queue = []
    n_idx = 0
    while n_idx < len(normals_for_today) or goldens_for_today:
        # Random gap 2 se 5 messages ka
        gap = random.randint(2, 5) 
        for _ in range(gap):
            if n_idx < len(normals_for_today):
                daily_queue.append(normals_for_today[n_idx])
                n_idx += 1
        
        if goldens_for_today:
            daily_queue.append(goldens_for_today.pop(0))

    state["daily_queue"] = daily_queue
    state["current_day_str"] = today_str
    save_state()
    print(f"✅ Today's queue generated: {len(state['daily_queue'])} messages ready.")

def get_next_proof():
    now = datetime.now(IST)
    today_str = str(now.date())

    if state["current_day_str"] != today_str:
        reset_daily_queue()

    if not state["daily_queue"]:
        return None

    # Pop message and save state immediately
    proof = state["daily_queue"].pop(0)
    save_state()
    return proof

# ================= MESSAGE FORMATTING =================
def generate_message(proof):
    if proof['type'] == 'G':
        return f"""**🏆 GOLDEN MEMBER 🏆**
**🎉 Congratulations, {proof['name']}! 🎉**
**✅ Aapke YouTube Channel par 1,000 Subscribers successfully add ho gaye hain! 🚀**
**🔗 Aapki Channel Link: 👇🏻**
**{proof['link']}**
**📈 Aur Subscribers badhane ke liye**
**👇🏻 Abhi yahan click karein 👇🏻**"""
    else:
        return f"""🎉 Congratulations {proof['name']}🎉

✅ Aapke YouTube Channel par {proof['total']} Subscribers Successfully Add ho gaye hain! 🎯

🔗 Aapki Channel Link: 👇🏻
{proof['link']}

🚀 Aur Subscribers badhane ke liye abhi click karein 👇🏻"""

# ================= BOT =================
async def send_proof(client):
    try:
        proof = get_next_proof()

        if proof is None:
            print("📭 All proofs exhausted for today. Waiting for next day...")
            return False
            
        message = generate_message(proof)

        await client.send_message(
            TARGET_CHANNEL,
            message,
            buttons=[
                Button.url("📈 100 Subscribers", BUTTON_LINK)
            ]
        )

        print(f"✅ Message sent ({proof['type']}) | Remaining today: {len(state['daily_queue'])}")
        return True

    except Exception as e:
        print("❌ Error:", e)
        return False

# ================= SCHEDULER =================
async def scheduler(client):
    while True:
        now = datetime.now(IST)
        today_str = str(now.date())

        if state["current_day_str"] != today_str:
            reset_daily_queue()

        # Timing strict: Subah 6 baje se raat 10 baje tak (6:00 to 21:59)
        if 6 <= now.hour < 22:
            if state["daily_queue"]:
                await send_proof(client)

                # Random delay between 16 to 19 minutes (Natural lagta hai aur 16 ghante me sahi fit baithta hai)
                delay = random.randint(16, 19)
                
                print(f"⏳ Next message in {delay} minutes")
                await asyncio.sleep(delay * 60)
            else:
                tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time(), tzinfo=IST)
                wait_seconds = (tomorrow - now).total_seconds()
                print(f"📭 Today's queue empty. Sleeping for {int(wait_seconds)} sec")
                await asyncio.sleep(max(60, wait_seconds))
        else:
            print("🌙 Night mode sleeping... Wait till 6 AM.")
            # Raat me har aadhe ghante me check karega subah hui ya nahi
            await asyncio.sleep(1800)

# ================= KEEP ALIVE =================
async def keep_alive():
    from aiohttp import web
    async def handle(request):
        return web.Response(text="Bot is running smoothly")
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Server running on port {port}")

# ================= MAIN =================
async def main():
    load_state() 
    
    if not state["current_day_str"]:
        reset_daily_queue()

    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("🤖 Bot started successfully! 377 Rules Active 🛡️")
    
    await asyncio.gather(
        scheduler(client),
        keep_alive()
    )

if __name__ == "__main__":
    asyncio.run(main())
