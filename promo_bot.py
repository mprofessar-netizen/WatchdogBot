import os
import asyncio
import random
from datetime import datetime, timedelta, timezone

from telethon import TelegramClient, Button
from telethon.sessions import MemorySession

# ================= CONFIG =================
API_ID = 37236703
API_HASH = 'a6d70fd6d0f99283ec4eea089e0ea397'
BOT_TOKEN = '7721954754:AAFSNi7iBj--zCGxJI6zE-TTypJ052yG14c'

# Yahan aapka naya channel update kar diya gaya hai 👇
TARGET_CHANNEL = '@LootRadarIndia'
BUTTON_LINK = 'https://t.me/Youtube20Sub_bot'

# IST Timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Naya Delay Cycle (Minutes me) - Average ~30 mins.
# Total 32 channels hain, toh 17 ghante (6 AM - 11 PM) me aaram se send ho jayenge.
DELAY_CYCLE = [27, 33, 24, 35, 29] 

# ================= PROOF DATA (Total 32 Channels) =================
PROOF_DATA = [
    # Puraane 17 Channels
    {"name": "Bakchodi Vines", "total": "200+", "link": "https://youtube.com/@the_bakchodi_vines?si=RFxkMXOR67yHP3jn"},
    {"name": "Rahul Creative Hub", "total": "600+", "link": "https://youtube.com/channel/UCQFrQc49Ab-aOPtvBk6PaPQ?si=_tST4RAJnS-pT1eZ"},
    {"name": "Adarsh Vlogs", "total": "1K+", "link": "https://youtube.com/@adarshvlogs-r15?si=3nMPY5ehsvtyyryO"},
    {"name": "Rajendra Official", "total": "4K+", "link": "https://youtube.com/@rajendraofficia?si=535yQI0S_shA8451"},
    {"name": "Akash Naik", "total": "100+", "link": "https://youtube.com/@akashnaik-r8y?si=OKjfKAmWEytT6yx4"},
    {"name": "Suraj Kasder", "total": "200+", "link": "https://youtube.com/@surajkasder-x4q?si=Q0ZTkJU4n-YcKTt3"},
    {"name": "VJ Kohli", "total": "400+", "link": "https://youtube.com/@imvjkohli?si=oJw3nuui-9Ylrs5D"},
    {"name": "Tasty Food Shorts Gupta", "total": "500+", "link": "https://youtube.com/@tastyfoodshortsgupta?si=XL1POkbwHvMohZRd"},
    {"name": "Gaming & Funny Video", "total": "200+", "link": "https://youtube.com/@gamingandfunnyvideo-m8h?si=KXf1-d3WDidvgv2_"},
    {"name": "Naman Editz", "total": "1K+", "link": "https://youtube.com/@naman_editz30?si=Ig16Laqa_8udfBML"},
    {"name": "Gangster FFX", "total": "1K+", "link": "https://youtube.com/@gangster_ffx62?si=SVjoij2Ce0jzyCwt"},
    {"name": "Sonali Singh Vlogs", "total": "2K+", "link": "https://youtube.com/@sonalisinghvlogs-----?si=EWq7V4Dj8JIGDp0_"},
    {"name": "Daily Anime Shots", "total": "2K+", "link": "https://youtube.com/@dailyanimeshots?si=aWn_XrQ08qYtdYNP"},
    {"name": "The Happy Place", "total": "400+", "link": "https://youtube.com/@thehappyplace2.0?si=LXXLCbbUbTzh6fm8"},
    {"name": "Sanaya Jain", "total": "1K+", "link": "https://youtube.com/@sanyamjain8488?si=1to0FqQx_y1f2WFx"},
    {"name": "Alone Music", "total": "300+", "link": "https://youtube.com/@alonemusic55?si=oKyc4UP5OdPAU9Jz"},
    {"name": "NK Ronix", "total": "1K+", "link": "https://youtube.com/@nk_ronix?si=L90bCh87qQvRVqwi"},
    
    # Naye 15 Channels
    {"name": "Indian tractor", "total": "500+", "link": "https://youtube.com/@amitkumaramitkumarm5u?si=Wg1kmdES63Sw5KeW"},
    {"name": "Durgesh", "total": "300+", "link": "https://youtube.com/@durgeshdangi3167?si=-Fsr079nfEv8dNxO"},
    {"name": "Yadav funny club", "total": "100+", "link": "https://youtube.com/@yadavfunnyclub?si=sSG7k0o9G59limCz"},
    {"name": "The viral", "total": "5K+", "link": "https://youtube.com/@theviralnews61?si=-iNW6WScJE6FAfoB"},
    {"name": "RD tecnical", "total": "3K+", "link": "https://youtube.com/@rdtechnical88?si=u0Kmi7d3S8po5oHK"},
    {"name": "UBC news Hindi", "total": "3K+", "link": "https://youtube.com/@ubchindi?si=DUwI12KgE3Wrqvdt"},
    {"name": "English guru", "total": "18K+", "link": "https://youtube.com/@englishgurucampus?si=8IuzTsp-0JNR3WxK"},
    {"name": "NCRT class", "total": "6K+", "link": "https://youtube.com/@gravity_guru?si=1MUeWHoOXmiiWZvb"},
    {"name": "Wegot Guru", "total": "7K+", "link": "https://youtube.com/@wegotguru?si=QugmQhk35w6UQCSo"},
    {"name": "Sangam education", "total": "2K+", "link": "https://youtube.com/@sangamsangrameducation?si=6DYqUPoUdSvmhd6f"},
    {"name": "Hemanta book", "total": "200+", "link": "https://youtube.com/@hemantabookpedia?si=gtK_Xo3Yx3mNEAN1"},
    {"name": "Sahil rokhri", "total": "200+", "link": "https://youtube.com/@sahilrokhriproearning?si=cE_lv6b9eVPSJrq8"},
    {"name": "Rubis cartoon", "total": "400+", "link": "https://youtube.com/@rubiscartoon-f4n?si=UmEgLeCL9X2Elo08"},
    {"name": "Payal dancer", "total": "5K+", "link": "https://youtube.com/@payal_dancer_18?si=NAwjQgSUZ4dSQaiI"},
    {"name": "Oxygen for education", "total": "100+", "link": "https://youtube.com/@oxygenforeducators?si=PkHJzh6ITxDt20ak"}
]

# ================= DAILY PROOF QUEUE =================
daily_queue = []
current_day = None

def reset_daily_queue():
    global daily_queue, current_day

    current_day = datetime.now(IST).date()
    daily_queue = PROOF_DATA.copy()
    random.shuffle(daily_queue)

    print(f"🔄 Daily proof queue refreshed ({len(daily_queue)} entries) for {current_day}")

def get_next_proof():
    global daily_queue, current_day

    today = datetime.now(IST).date()

    if current_day != today:
        reset_daily_queue()

    if not daily_queue:
        return None

    return daily_queue.pop(0)

# ================= MESSAGE =================
def generate_message():
    proof = get_next_proof()

    if proof is None:
        return None

    return f"""Congratulations 🎉👏🏻 **{proof['name']}**

Apki link 🖇️
Par 100 subscribers successful add hogye he please chack 👇🏻

{proof['link']}

          Total send {proof['total']} subscribers

Or subscribe badane ke liye abhi click kre 👇🏻"""

# ================= BOT =================
async def send_proof(client):
    try:
        message = generate_message()

        if message is None:
            print("📭 All proofs exhausted for today. Waiting for next day...")
            return False

        await client.send_message(
            TARGET_CHANNEL,
            message,
            buttons=[
                Button.url("📈 100 subscribers", BUTTON_LINK)
            ]
        )

        remaining = len(daily_queue)
        print(f"✅ Message sent | Remaining proofs today: {remaining}")
        return True

    except Exception as e:
        print("❌ Error:", e)
        return False

# ================= SCHEDULER =================
async def scheduler(client):
    index = 0

    while True:
        now = datetime.now(IST)

        # Auto refresh queue at new IST day
        if current_day != now.date():
            reset_daily_queue()

        # Active hours: Subah 6 baje se Raat 11 baje (23:00) tak
        if 6 <= now.hour < 23:

            if daily_queue:
                await send_proof(client)

                delay = DELAY_CYCLE[index]
                index = (index + 1) % len(DELAY_CYCLE)

                print(f"⏳ Next message in {delay} minutes")
                await asyncio.sleep(delay * 60)

            else:
                tomorrow = datetime.combine(
                    now.date() + timedelta(days=1),
                    datetime.min.time(),
                    tzinfo=IST
                )

                wait_seconds = (tomorrow - now).total_seconds()
                print(f"📭 All proofs used today. Sleeping until next IST day ({int(wait_seconds)} sec)")
                await asyncio.sleep(max(60, wait_seconds))

        else:
            print("🌙 Night mode sleeping...")
            await asyncio.sleep(1800)

# ================= KEEP ALIVE =================
async def keep_alive():
    from aiohttp import web

    async def handle(request):
        return web.Response(text="Bot is alive")

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
    reset_daily_queue()

    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    print("🤖 Bot started successfully")

    # First message instantly
    await send_proof(client)

    await asyncio.gather(
        scheduler(client),
        keep_alive()
    )

if __name__ == "__main__":
    asyncio.run(main())
