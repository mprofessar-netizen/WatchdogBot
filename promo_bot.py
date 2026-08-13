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

TARGET_CHANNEL = '@LootRadarIndia'
BUTTON_LINK = 'https://t.me/Youtube20Sub_bot'

# IST Timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Naya Delay Cycle (Minutes me) - Average ~21 mins.
DELAY_CYCLE = [18, 22, 19, 24, 21] 

# ================= PROOF DATA (NEW LIST) =================
PROOF_DATA = [
    {"name": "Raju Hembram", "total": "200", "link": "https://youtube.com/@onlyaisong10k?si=Uq9nqunf7tmL1IT6"},
    {"name": "Mukesh Prasad", "total": "100", "link": "https://youtube.com/@mukeshprasad2.0?si=XmeWWQAYws0mbJrU"},
    {"name": "Kailash Chaudhary", "total": "200", "link": "https://www.youtube.com/@kailashchaudhary9221"},
    {"name": "Dhakad ji Dhakad ji", "total": "200", "link": "https://youtube.com/@preetlover987rj?si=rk96H0AErv0bnrU2"},
    {"name": "YT tecnical", "total": "100", "link": "https://youtube.com/@infinityfactx07?si=bthHyjsYFn7SpAW_"},
    {"name": "Aliya Khan", "total": "100", "link": "https://www.youtube.com/@funnyfever8"},
    {"name": "SRT X XEROX", "total": "200", "link": "https://youtube.com/@srtxxerox?si=4s6qulLp7ql2wygD"},
    {"name": "NITIN Kumar", "total": "200", "link": "https://youtube.com/@safarnama-e-engineer?si=N8-sbVAva3pmUQYB"},
    {"name": "N A Y A N ツ", "total": "100", "link": "https://www.youtube.com/@NAYANGAMING1-full"},
    {"name": "Sahib Gosal", "total": "100", "link": "https://youtube.com/@fastclipshq-1?si=b7-9asXM4V3DrIKY"},
    {"name": "System Jack", "total": "100", "link": "https://www.youtube.com/@codinguruji8686"},
    {"name": "Siddhu", "total": "100", "link": "https://youtube.com/@animexworld-c1l?si=WPlSL6eDmAdZk52k"},
    {"name": "Prince Kumar Sharma", "total": "100", "link": "https://youtube.com/@priteeofficial703?si=AVjGuziGuVUpgM6j"},
    {"name": "Devil's Queen 😈😈😈", "total": "200", "link": "https://youtube.com/@thebhaktirasofficial?si=QVlvZZnH5VgmYWkJ"},
    {"name": "Manish Mahiya", "total": "100", "link": "https://youtube.com/@genzasmr-7?si=1KEvfUa7V7kmGHSt"},
    {"name": "$âk$hî 🍁", "total": "100", "link": "https://youtube.com/@aiventra1234?si=bIgMjymVQhlfDxGi"},
    {"name": "Akash Yadav", "total": "100", "link": "https://youtube.com/@factzonehindi-1234?si=ZOptnU9IAcWckaMZ"},
    {"name": "Mohd Mohsin", "total": "200", "link": "https://youtube.com/@mdmohsin-o7p9o?si=PM4bWGtFrXskuQ6H"},
    {"name": "Gulashan Kumar", "total": "100", "link": "https://www.youtube.com/@AiEditorvideo-s4p"},
    {"name": "Sonu Kumar", "total": "100", "link": "https://www.youtube.com/@Sonukumarx1234"},
    {"name": "Gulashan Kumar (2)", "total": "100", "link": "https://www.youtube.com/@AiEditorvideo-s4p"},
    {"name": "Puja Srivastava", "total": "200", "link": "https://youtube.com/@koreandrama11k?si=Tj4d77S9-XNYaITT"},
    {"name": "Tuhin Hossain", "total": "100", "link": "https://youtube.com/@tuhinhossainvlogs?feature=shared"},
    {"name": "Vakil Ahmad", "total": "200", "link": "https://youtube.com/@dailywithvakil-m7t?si=yF6DjRO4p0eiwZhR"},
    {"name": "JY", "total": "100", "link": "https://youtube.com/@hurrycurryrecipes?si=CzWSEYp9bnHgZvWe"},
    {"name": "akc Musical Brand", "total": "200", "link": "https://youtube.com/@akcmusicalbrand?si=Q-e60expJmdYfS56"},
    {"name": "𝐈𝐬𝐭𝐢𝐲𝐚𝐤 𝐞𝐝𝐢𝐭𝐳", "total": "100", "link": "https://youtube.com/@istyartx?si=80BfnaVqhpHxmxB7"},
    {"name": "Shiva Earth", "total": "200", "link": "https://youtube.com/@beingshivarth?si=bnRlvGWJc6bOgOHM"},
    {"name": "Gora Gora", "total": "100", "link": "https://youtube.com/@harryart-z4i?si=G0nxEz7xvFYhVOK1"},
    {"name": "No Name", "total": "200", "link": "https://youtube.com/@gkhackergamer?si=Czoj4DjNojTd8k8J"},
    {"name": "Shiva Earth (2)", "total": "200", "link": "https://youtube.com/@beingshivarth?si=wZGmCAncWPCB138M"},
    {"name": "Asgar Ali", "total": "200", "link": "https://www.youtube.com/@Vejitebalkindom1"},
    {"name": "Satish Kumar", "total": "200", "link": "https://youtube.com/@bhaktiganga369?si=SDvAD07punSy8rC1"},
    {"name": "Amar Magat", "total": "200", "link": "https://youtube.com/@susmitaashik?si=ePiKDktVDblHMmOU"},
    {"name": "Vijay", "total": "100", "link": "https://www.youtube.com/@HNNmotivation"},
    {"name": "Guru Ji", "total": "100", "link": "https://youtube.com/@anilkaka1?si=MCjXjds3jDo1z2EH"},
    {"name": "AK", "total": "200", "link": "https://youtube.com/@sanatangyandeep1k?si=SREvO-89S-PIlZE2"},
    {"name": "Ajay verma", "total": "100", "link": "https://www.youtube.com/@medenrgy"},
    {"name": "Amrit", "total": "200", "link": "https://youtube.com/@theeternaljournal-s8p?si=ADyKfxsJoJUNZsbh"},
    {"name": "ᴀᴅɪᴛyᴀ ᴋᴜᴍᴀʀ", "total": "200", "link": "https://youtube.com/@primeaditya1k?si=OWFFDtxdFI7YTL1z"},
    {"name": "akc Musical Brand (2)", "total": "200", "link": "https://youtube.com/@akcmusicalbrand?si=YrZz4M7dqEXvULh6"},
    {"name": "Anushka Rai", "total": "200", "link": "https://youtube.com/@anushkarai5719?si=RRvDCqZYpDSQ-5if"},
    {"name": "A G", "total": "100", "link": "https://www.youtube.com/@AshK-b1w"},
    {"name": "Debjani Bhakat", "total": "200", "link": "https://youtube.com/@cartoonworld4x?si=NmpYzLD90XigiXsA"},
    {"name": "Grace Of God", "total": "200", "link": "https://youtube.com/@dreamyjc"},
    {"name": "K K", "total": "200", "link": "https://www.youtube.com/@LifeUnfiltered-Sk"},
    {"name": "Suresh Dancer", "total": "100", "link": "https://youtube.com/@sbnepal-s1s2?si=e7mCkT8CT1yogXfp"},
    {"name": "Kavanng", "total": "200", "link": "https://www.youtube.com/@gopalpipalva"},
    {"name": "Ibran Khan", "total": "200", "link": "https://www.youtube.com/@RaktickEditz"}
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
def generate_message(proof):
    return f"""🎉 Congratulations {proof['name']} 🎉

✅ Aapke YouTube channel par {proof['total']} Subscribers Successfully Add ho gaye hain! 🎯

🔗 Aapki Link:   Please chack

{proof['link']}

🚀Apne YouTube Channel par aur Subscribers badhane ke liye abhi click karein 👇🏻"""

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
                # Button ko waise hi 100 par fix kar diya hai
                Button.url("📈 100 Subscribers", BUTTON_LINK)
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

        if current_day != now.date():
            reset_daily_queue()

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

    await send_proof(client)

    await asyncio.gather(
        scheduler(client),
        keep_alive()
    )

if __name__ == "__main__":
    asyncio.run(main())
