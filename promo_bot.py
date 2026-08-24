import os
import re
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

# Delay Cycle (Minutes me)
DELAY_CYCLE = [18, 22, 19, 24, 21] 

# ================= 7-DAY SCHEDULING PATTERN =================
# N = Normal Message, G = Golden Message
DAY_PATTERNS = {
    1: [3, 'G', 4, 'G', 2, 'G', 5, 'G', 3, 'G', 4, 'G', 2, 'G', 5, 'G', 3, 'G', 4, 'G', 8, 'G'],
    2: [2, 'G', 5, 'G', 3, 'G', 4, 'G', 2, 'G', 4, 'G', 3, 'G', 5, 'G', 2, 'G', 4, 'G', 9, 'G'],
    3: [5, 'G', 2, 'G', 4, 'G', 3, 'G', 5, 'G', 2, 'G', 3, 'G', 4, 'G', 2, 'G', 5, 'G', 8, 'G'],
    4: [4, 'G', 2, 'G', 5, 'G', 3, 'G', 4, 'G', 2, 'G', 5, 'G', 3, 'G', 4, 'G', 2, 'G', 9, 'G'],
    5: [2, 'G', 3, 'G', 5, 'G', 2, 'G', 4, 'G', 5, 'G', 3, 'G', 2, 'G', 4, 'G', 3, 'G', 10, 'G'],
    6: [3, 'G', 5, 'G', 2, 'G', 4, 'G', 3, 'G', 2, 'G', 5, 'G', 4, 'G', 3, 'G', 4, 'G', 8, 'G'],
    7: [5, 'G', 3, 'G', 2, 'G', 4, 'G', 5, 'G', 2, 'G', 3, 'G', 4, 'G', 3, 'G', 5, 'G', 7, 'G'],
}


# ================= RAW DATA (YAHAN COPY PASTE KAREIN) =================
# Bhai, aage se jab bhi nayi list aaye, bas purani delete karke yahan nayi paste kar dena bina kisi formatting ke!

GOLDEN_RAW_TEXT = """
funny adda
https://www.youtube.com/@funny_adda_123-p2h
mono MOTO
https://www.youtube.com/@MonoMoto
MT official
https://www.youtube.com/@manukutadingi
Music
https://www.youtube.com/@myfusion
EL mono
https://www.youtube.com/@ELMONONK250
Tips 2T
https://www.youtube.com/@juqui
THE black MT
https://www.youtube.com/@TheBlackMT
B1 Moto
https://www.youtube.com/@b1.motoadv
48 central
https://www.youtube.com/@48central76
Citi hikers
https://www.youtube.com/channel/UCfU0mnTG2ixQmSDxzXXxHKg
Mood of sad song
https://www.youtube.com/@SK_99_CREATION
motos
https://www.youtube.com/@losdelasmotos
my 11 collection
https://www.youtube.com/@My112collection
kk modifiy
https://www.youtube.com/@kkmodification3212
starz TV
https://www.youtube.com/@MotostarzTV
VB
https://www.youtube.com/@VbPalmeiras-j4m
midia rara
https://www.youtube.com/@raramedia26420
Rick
https://www.youtube.com/@RickandAndreaGetOutside
pedal frinds
https://www.youtube.com/@PedalFriends
manish official
https://www.youtube.com/@Manishofficialertainment
Manoj
https://www.youtube.com/@Manishmanojofficial
entertanment
https://www.youtube.com/@manojentertainment9935
kuwara kawaii 
https://www.youtube.com/@kuwarakwahitv4275
Youtube pintu
https://www.youtube.com/@PintuIsLivee
kayla art
https://www.youtube.com/@ArtsyKayla
rani
https://www.youtube.com/@RaniCreativeCorner-v6i
Frensh
https://www.youtube.com/@FrenchFlairCorner
Nilesh alawa 
https://youtube.com/@nileshalave6?si=513dq8Kqx27i_s1K
Treders life 
https://youtube.com/@tradewithlaksh99?si=mXIokPl2dg4fyfob
Crypto log
https://youtube.com/@cryptolog1?si=p1MyYV3sukFt-DU8
Vassu
https://youtube.com/@vassuislive?si=J6Jyzy4CiK4CcjCJ
Tips with Barsa
https://youtube.com/@tipswithbarsha?si=8zBndLnNQ5qySFr7
Motivation by hussain 
https://youtube.com/@mha2211?si=H0COJyDYv6Qvuev_
All things 
https://youtube.com/@faizangillani-z7h?si=A7VVtZPaOdpNdVPy
KEB automation 
https://youtube.com/@kebautomation?si=6mlPY77klUMpXP1Q
Window treatments 
https://youtube.com/@wtmarketingpros?si=MAW3awnl1_9M_BzF
Alayna coocking 
https://youtube.com/@sharrykhan1766?si=1G2DjbhWLn6rHXE4
Tip earning 
https://youtube.com/@tipearning?si=W73_ykcDiXDVKYdr
Moe's meme
https://youtube.com/@moesmemes?si=fzmxxP3MvD5jkxSW
Rexis CPM 
https://youtube.com/@cpm.rexiss?si=pjQBThH5vUgGrF1m
Motivation hour
https://youtube.com/@motivationhourrecipes?si=D9vsjazATmGPkV42
Let's cook
https://youtube.com/@letscookwithhoney?si=aVMy6P2xrj4B6RN_
F HOQUE
https://youtube.com/@fhoque?si=qAw73hY3tJHbSWZK
PHESTO
https://youtube.com/@phestotech?si=SKxNAxUduQWnBRxc
Guide Tech pro
https://youtube.com/@guidetechpro?si=_RLtux-mWn6LzZUk
Itz hars editz
https://youtube.com/@itzhrsheditz9000?si=w2W2VbEoLOHXNFGR
Babu edit
https://youtube.com/@babueditz-sp6uy?si=MEU2upJJLOqNwud4
Read book class 10th
https://youtube.com/@readbook199?si=hNnTHSLmkE1AbDxl
Money video 
https://youtube.com/@monkeyai_video2?si=HRtPnBXBFKv7_gUU
Mood mod
https://youtube.com/@moodmode?si=_5PW5mno2TZuLBON
Timmy talk
https://youtube.com/@timmytalkstoday?si=xjCABxfa_FoxwYgp
Rizlaw bits
https://youtube.com/@prod.rizlaw?si=4PRS2_DAi15EnjDR
English with asima ali
https://youtube.com/@englishwithasimaali?si=1LHuHAHtJeH-Vluw
Saqlain tech
https://youtube.com/@saqlaintech-h9w?si=YMljYilexefOxcRM
Ai plus mod
https://youtube.com/@aiplusmore?si=a1O7VzM1BKm5Bi7U
Short PK
https://youtube.com/@aishortspk1?si=lSFDK4STbtzUj4MT
Jace' real
https://youtube.com/@jacesrealreviews?si=up6EfuQKauO_Ky7t
Offical monkey treck 
https://youtube.com/@elvishtech?si=Risf5f7UIIqlb3Rx
Review central 
https://youtube.com/@yourreviewcentral?si=cZPvXtocA0h10FsY
Wealth without wall strict 
https://youtube.com/@wealthwithoutwallstreet?si=YdTE0Nmlr1yb9MXE
BeamNG Toro
https://youtube.com/@beamngtoro?si=0fotlhdABdiArd7w
Deadlox
https://youtube.com/@deadloxgamingu?si=lAKin111YtvcLI9x
Vikas shorts
https://youtube.com/@vikas_shorts_15?si=ToM9loxTVAsh6iD5
999 gari Gamer 
https://youtube.com/@999garigamer?si=Aggt7d469yi7UR20
Umraw meena
https://youtube.com/@umravmeena9?si=qL32jvf72tIjYDr7
Tips and tricks 
https://youtube.com/@tipstricks-e7o?si=-QzLW-TJLMfC9MbL
Game store 
https://youtube.com/@realgamestore?si=yFmQYMsmDtK7Etav
Variant investor
https://youtube.com/@variantinvestor?si=m0aMCwrU2ixu-FDs
To The Bank 
https://youtube.com/@tothepointbanking1938?si=_vHcddhP8IxzPH8t
VK vinay
https://youtube.com/@vkvinaystreetfood?si=0q66RpzIpjg0Lb_9
Lokesh meena
https://youtube.com/@lokeshmeena2469?si=cDVjBvOWdLMcS1DT
Snake rescue 
https://youtube.com/@snakerescueteamhardoi?si=GHz-IdTIV9oOCZtx
Online gaming 
https://youtube.com/@onlinegaming-786?si=eY4GCQpmyssoLoU6
Deep boutique
https://youtube.com/@deepboutiquecollection?si=wCDP6BlUmOmgOgJM
Vivian 
https://youtube.com/@viviancurates?si=0azRWWVrw8Mh6SJT
Bass magzine 
https://youtube.com/@bassmagazine?si=m5bkbLLNnAtR04Fs
Amrita Vishwa 
https://youtube.com/@coimbatorecampus?si=9B8J-L1lOCCh7sPH
"""

NORMAL_RAW_TEXT = """
🚨 NEW WITHDRAWAL!
👤 Raju Hembram
🎯 200 Subs
🔗 https://youtube.com/@onlyaisong10k?si=Uq9nqunf7tmL1IT6

🚨 NEW WITHDRAWAL!
👤 Mukesh Prasad
🎯 100 Subs
🔗 https://youtube.com/@mukeshprasad2.0?si=XmeWWQAYws0mbJrU

🚨 NEW WITHDRAWAL!
👤 Kailash Chaudhary
🎯 200 Subs
🔗 https://www.youtube.com/@kailashchaudhary9221

savita
100
https://www.youtube.com/@savita2182

EL padre
100
https://www.youtube.com/@ElPadreCoreano

🚨 NEW WITHDRAWAL REQUEST!
👤 User: 10vs10
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@anni-i7b?si=IscGwAV1v8NgOCbM

colour prediction 
200
https://www.youtube.com/@Colourpredictionhacktricks

guru jii
100
https://www.youtube.com/@vaibhavtripathi015
"""
# Note: Maine Normal raw text thoda short rakha hai display ke liye, aap apni puri list direct iske andar paste kar dena bina kisi tension ke!


# ================= DATA PARSERS =================
def load_golden_data(raw_text):
    results = []
    # Automatically extracts Name and Link
    pattern = re.compile(r'([^\n]+)\n+(https?://[^\n]+)')
    for m in pattern.finditer(raw_text):
        results.append({'name': m.group(1).strip(), 'total': '1000', 'link': m.group(2).strip()})
    return results

def load_normal_data(raw_text):
    results = []
    # Matches the 🚨 format
    pattern1 = re.compile(r'👤 (?:User:\s*)?([^\n]+)\n+🎯 (?:Target:\s*)?(\d+)\s*Subs\n+🔗 (?:Link:\s*)?(https?://[^\n]+)', re.IGNORECASE)
    for m in pattern1.finditer(raw_text):
        results.append({'name': m.group(1).strip(), 'total': m.group(2).strip(), 'link': m.group(3).strip()})
    
    clean_text = pattern1.sub('', raw_text)
    
    # Matches the plain text format (Name, 100/200, Link)
    pattern2 = re.compile(r'([^\n]+)\n+(100|120|200)\n+(https?://[^\n]+)')
    for m in pattern2.finditer(clean_text):
        results.append({'name': m.group(1).strip(), 'total': m.group(2).strip(), 'link': m.group(3).strip()})
    
    return results

GOLDEN_DATA = load_golden_data(GOLDEN_RAW_TEXT)
NORMAL_DATA = load_normal_data(NORMAL_RAW_TEXT)

# ================= DAILY SCHEDULING SYSTEM =================
daily_queue = []
current_day = None
normal_pool = []
golden_pool = []

def reset_daily_queue():
    global daily_queue, current_day, normal_pool, golden_pool

    now = datetime.now(IST)
    current_day = now.date()
    
    # Python me isoweekday: Monday=1, Tuesday=2 ... Sunday=7
    day_number = now.isoweekday() 
    pattern = DAY_PATTERNS[day_number]

    daily_queue = []

    for item in pattern:
        if item == 'G':
            if not golden_pool:
                golden_pool = GOLDEN_DATA.copy()
                random.shuffle(golden_pool)
            proof = golden_pool.pop(0).copy()
            proof['type'] = 'G'
            daily_queue.append(proof)
        else:
            for _ in range(item):
                if not normal_pool:
                    normal_pool = NORMAL_DATA.copy()
                    random.shuffle(normal_pool)
                proof = normal_pool.pop(0).copy()
                proof['type'] = 'N'
                daily_queue.append(proof)

    print(f"🔄 Day {day_number} queue generated: {len(daily_queue)} messages for today.")

def get_next_proof():
    global daily_queue, current_day

    if current_day != datetime.now(IST).date():
        reset_daily_queue()

    if not daily_queue:
        return None

    return daily_queue.pop(0)

# ================= MESSAGE FORMATTING =================
def generate_message(proof):
    if proof['type'] == 'G':
        # Golden Message (Fully Bold)
        return f"""**🏆 GOLDEN MEMBER 🏆**
**🎉 Congratulations, {proof['name']}! 🎉**
**✅ Aapke YouTube Channel par 1,000 Subscribers successfully add ho gaye hain! 🚀**
**🔗 Aapki Channel Link: 👇🏻**
**{proof['link']}**
**📈 Aur Subscribers badhane ke liye**
**👇🏻 Abhi yahan click karein 👇🏻**"""
    else:
        # Normal Message
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

        remaining = len(daily_queue)
        print(f"✅ Message sent ({proof['type']}) | Remaining today: {remaining}")
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
                print(f"📭 Today's queue empty. Sleeping for {int(wait_seconds)} sec")
                await asyncio.sleep(max(60, wait_seconds))
        else:
            print("🌙 Night mode sleeping...")
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
    reset_daily_queue()
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("🤖 Bot started successfully with new 7-Day pattern!")
    
    await send_proof(client)

    await asyncio.gather(
        scheduler(client),
        keep_alive()
    )

if __name__ == "__main__":
    asyncio.run(main())
