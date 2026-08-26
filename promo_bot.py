import os
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

# IST Timezone
IST = timezone(timedelta(hours=5, minutes=30))
QUEUE_FILE = "message_queue.json"

# ================= RAW DATA =================
RAW_GOLDEN = """
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
chelshi lakhpati
https://www.youtube.com/@chelsilakhpati
tred hunt
https://www.youtube.com/@tradehuntofficial
old coin
https://www.youtube.com/@oldcoinandnote6777
sunara odisha
https://www.youtube.com/@SUNARAODISHA-x6k
money ki pathshala
https://www.youtube.com/@MoneykiPathshala1
mayank foodie
https://www.youtube.com/@mayankfoodie8669
CA Karan seth
https://www.youtube.com/@cakaransheth
public servies point 
https://www.youtube.com/@PublicServicepoint
gulshan babu official 
https://www.youtube.com/@gulshan_babu_Offical
khan
https://www.youtube.com/@Gulshan.khan786
shivam Singh 
https://www.youtube.com/@totaltransformationwithshivam
sharwan komal
https://www.youtube.com/@sharwan.komal85
Dr.  Satish
https://www.youtube.com/@dr.satishgajera8597
sufi ashan
https://www.youtube.com/@SufiAhsanSaifiOfficial
K sharwan
https://www.youtube.com/@sharwankdubey4047
max priyanshu Ji
https://www.youtube.com/@maxpriyanshuji
parmila
https://www.youtube.com/@ItsParimalaSatish
munna bhaiya vlog
https://www.youtube.com/@munnabhaiyavlogs854
uniq DJ system
https://www.youtube.com/@uniqued.jsystem5016
dil SE mohan
https://www.youtube.com/@Dil_se_mohan
akib
https://www.youtube.com/@akibsaifiuk18
santosh sing
https://www.youtube.com/@SantoshSingh-l1i
sunny evening studio
https://www.youtube.com/@Evening13
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

RAW_NORMAL = """
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
🚨 NEW WITHDRAWAL!
👤 Dhakad ji Dhakad ji
🎯 200 Subs
🔗 https://youtube.com/@preetlover987rj?si=rk96H0AErv0bnrU2
🚨 NEW WITHDRAWAL!
👤 YT tecnical 
🎯 100 Subs
🔗 https://youtube.com/@infinityfactx07?si=bthHyjsYFn7SpAW_
🚨 NEW WITHDRAWAL!
👤 Aliya Khan
🎯 100 Subs
🔗 https://www.youtube.com/@funnyfever8
🚨 NEW WITHDRAWAL!
👤 SRT X XEROX
🎯 200 Subs
🔗 https://youtube.com/@srtxxerox?si=4s6qulLp7ql2wygD
🚨 NEW WITHDRAWAL!
👤 NITIN Kumar
🎯 200 Subs
🔗 https://youtube.com/@safarnama-e-engineer?si=N8-sbVAva3pmUQYB
🚨 NEW WITHDRAWAL!
👤 N A Y A N ツ
🎯 100 Subs
🔗 https://www.youtube.com/@NAYANGAMING1-full
🚨 NEW WITHDRAWAL!
👤 Sahib Gosal
🎯 100 Subs
🔗 https://youtube.com/@fastclipshq-1?si=b7-9asXM4V3DrIKY
🚨 NEW WITHDRAWAL!
👤 System Jack
🎯 100 Subs
🔗 https://www.youtube.com/@codinguruji8686
🚨 NEW WITHDRAWAL!
👤 Siddhu
🎯 100 Subs
🔗 https://youtube.com/@animexworld-c1l?si=WPlSL6eDmAdZk52k
🚨 NEW WITHDRAWAL!
👤 Prince Kumar Sharma
🎯 100 Subs
🔗 https://youtube.com/@priteeofficial703?si=AVjGuziGuVUpgM6j
🚨 NEW WITHDRAWAL!
👤 Devil's Queen 😈😈😈
🎯 200 Subs
🔗 https://youtube.com/@thebhaktirasofficial?si=QVlvZZnH5VgmYWkJ
🚨 NEW WITHDRAWAL!
👤 Manish Mahiya
🎯 100 Subs
🔗 https://youtube.com/@genzasmr-7?si=1KEvfUa7V7kmGHSt
🚨 NEW WITHDRAWAL!
👤 $âk$hî 🍁
🎯 100 Subs
🔗 https://youtube.com/@aiventra1234?si=bIgMjymVQhlfDxGi
🚨 NEW WITHDRAWAL!
👤 Akash Yadav
🎯 100 Subs
🔗 https://youtube.com/@factzonehindi-1234?si=ZOptnU9IAcWckaMZ
🚨 NEW WITHDRAWAL!
👤 Mohd Mohsin
🎯 200 Subs
🔗 https://youtube.com/@mdmohsin-o7p9o?si=PM4bWGtFrXskuQ6H
🚨 NEW WITHDRAWAL!
👤 Gulashan Kumar
🎯 100 Subs
🔗 https://www.youtube.com/@AiEditorvideo-s4p
🚨 NEW WITHDRAWAL!
👤 Sonu Kumar
🎯 100 Subs
🔗 https://www.youtube.com/@Sonukumarx1234
🚨 NEW WITHDRAWAL!
👤 Gulashan Kumar
🎯 100 Subs
🔗 https://www.youtube.com/@AiEditorvideo-s4p
🚨 NEW WITHDRAWAL!
👤 Puja Srivastava
🎯 200 Subs
🔗 https://youtube.com/@koreandrama11k?si=Tj4d77S9-XNYaITT
🚨 NEW WITHDRAWAL!
👤 Tuhin Hossain
🎯 100 Subs
🔗 https://youtube.com/@tuhinhossainvlogs?feature=shared
🚨 NEW WITHDRAWAL!
👤 Vakil Ahmad
🎯 200 Subs
🔗 https://youtube.com/@dailywithvakil-m7t?si=yF6DjRO4p0eiwZhR
🚨 NEW WITHDRAWAL!
👤 JY
🎯 100 Subs
🔗 https://youtube.com/@hurrycurryrecipes?si=CzWSEYp9bnHgZvWe
🚨 NEW WITHDRAWAL!
👤 akc Musical Brand
🎯 200 Subs
🔗 https://youtube.com/@akcmusicalbrand?si=Q-e60expJmdYfS56
🚨 NEW WITHDRAWAL!
👤 𝐈𝐬𝐭𝐢𝐲𝐚𝐤 𝐞𝐝𝐢𝐭𝐳
🎯 100 Subs
🔗 https://youtube.com/@istyartx?si=80BfnaVqhpHxmxB7
🚨 NEW WITHDRAWAL!
👤 Shiva Earth
🎯 200 Subs
🔗 https://youtube.com/@beingshivarth?si=bnRlvGWJc6bOgOHM
🚨 NEW WITHDRAWAL!
👤 Gora Gora
🎯 100 Subs
🔗 https://youtube.com/@harryart-z4i?si=G0nxEz7xvFYhVOK1
🚨 NEW WITHDRAWAL!
👤 No Name
🎯 200 Subs
🔗 https://youtube.com/@gkhackergamer?si=Czoj4DjNojTd8k8J
🚨 NEW WITHDRAWAL!
👤 Shiva Earth
🎯 200 Subs
🔗 https://youtube.com/@beingshivarth?si=wZGmCAncWPCB138M
🚨 NEW WITHDRAWAL!
👤 Asgar Ali
🎯 200 Subs
🔗 https://www.youtube.com/@Vejitebalkindom1
🚨 NEW WITHDRAWAL!
👤 Satish Kumar
🎯 200 Subs
🔗 https://youtube.com/@bhaktiganga369?si=SDvAD07punSy8rC1
🚨 NEW WITHDRAWAL!
👤 Amar Magat
🎯 200 Subs
🔗 https://youtube.com/@susmitaashik?si=ePiKDktVDblHMmOU
🚨 NEW WITHDRAWAL!
👤 Vijay
🎯 100 Subs
🔗 https://www.youtube.com/@HNNmotivation
🚨 NEW WITHDRAWAL!
👤 Guru Ji
🎯 100 Subs
🔗 https://youtube.com/@anilkaka1?si=MCjXjds3jDo1z2EH
🚨 NEW WITHDRAWAL!
👤 AK
🎯 200 Subs
🔗 https://youtube.com/@sanatangyandeep1k?si=SREvO-89S-PIlZE2
🚨 NEW WITHDRAWAL!
👤 Ajay verma
🎯 100 Subs
🔗 https://www.youtube.com/@medenrgy
🚨 NEW WITHDRAWAL!
👤 Amrit
🎯 200 Subs
🔗 https://youtube.com/@theeternaljournal-s8p?si=ADyKfxsJoJUNZsbh
🚨 NEW WITHDRAWAL!
👤 ᴀᴅɪᴛyᴀ ᴋᴜᴍᴀʀ
🎯 200 Subs
🔗 https://youtube.com/@primeaditya1k?si=OWFFDtxdFI7YTL1z
🚨 NEW WITHDRAWAL!
👤 akc Musical Brand
🎯 200 Subs
🔗 https://youtube.com/@akcmusicalbrand?si=YrZz4M7dqEXvULh6
🚨 NEW WITHDRAWAL!
👤 Anushka Rai
🎯 200 Subs
🔗 https://youtube.com/@anushkarai5719?si=RRvDCqZYpDSQ-5if
🚨 NEW WITHDRAWAL!
👤 A G
🎯 100 Subs
🔗 https://www.youtube.com/@AshK-b1w
🚨 NEW WITHDRAWAL!
👤 Debjani Bhakat
🎯 200 Subs
🔗 https://youtube.com/@cartoonworld4x?si=NmpYzLD90XigiXsA
🚨 NEW WITHDRAWAL!
👤 Grace Of God
🎯 200 Subs
🔗 https://youtube.com/@dreamyjc
🚨 NEW WITHDRAWAL!
👤 K K
🎯 200 Subs
🔗 https://www.youtube.com/@LifeUnfiltered-Sk
🚨 NEW WITHDRAWAL!
👤 Suresh Dancer
🎯 100 Subs
🔗 https://youtube.com/@sbnepal-s1s2?si=e7mCkT8CT1yogXfp
🚨 NEW WITHDRAWAL!
👤 Kavanng
🎯 200 Subs
🔗 https://www.youtube.com/@gopalpipalva
🚨 NEW WITHDRAWAL!
👤 Ibran Khan
🎯 200 Subs
🔗 https://www.youtube.com/@RaktickEditz
🚨 NEW WITHDRAWAL!
👤 R J RAJU Roy
🎯 100 Subs
🔗 https://www.youtube.com/@RJRaju-vlogs
🚨 NEW WITHDRAWAL!
👤 AB
🎯 100 Subs
🔗 https://youtube.com/@arnavbhaskarvlogs?si=zg9eoSGQlvEK9Xwk
🚨 NEW WITHDRAWAL!
👤 Rishi Raj
🎯 100 Subs
🔗 https://youtube.com/@rpacomedy-y?si=FXiYfqCcZnTDMeKj
🚨 NEW WITHDRAWAL!
👤 Ak stock market
🎯 200 Subs
🔗 https://youtube.com/@akstockmarket78?si=BBZmGIHpVzrpekg9
🚨 NEW WITHDRAWAL!
👤 Suraj Singhania Official
🎯 100 Subs
🔗 https://www.youtube.com/@Surajsinghaniaofficial-z3h
🚨 NEW WITHDRAWAL!
👤 Mahipal 🥠 Choudhary
🎯 200 Subs
🔗 https://www.youtube.com/@Restoration-g1o
🚨 NEW WITHDRAWAL!
👤 Poonia Mast
🎯 100 Subs
🔗 https://www.youtube.com/@desijazbaatshayari
🚨 NEW WITHDRAWAL!
👤 Rupa
🎯 200 Subs
🔗 https://youtube.com/@storygalpo?si=Ef2h4jxAkSE7k8xF
🚨 NEW WITHDRAWAL!
👤 Tackbro
🎯 100 Subs
🔗 https://youtube.com/@jhakaasgopal?si=wyvw2YHhpEljaNK4
🚨 NEW WITHDRAWAL!
👤 Naitik Gujja
🎯 100 Subs
🔗 https://youtube.com/@naitik-success?si=szEmfwHBtwQpCp4o
🚨 NEW WITHDRAWAL!
👤 Jass Preet
🎯 100 Subs
🔗 https://www.youtube.com/@AJaaa-ajeet
🚨 NEW WITHDRAWAL!
👤 Raja Bhai
🎯 200 Subs
🔗 https://www.youtube.com/@ShortsvideoAi-d2h
🚨 NEW WITHDRAWAL!
👤 Sachin
🎯 200 Subs
🔗 https://youtube.com/@sachincomedymaster?si=oeGqjfZLj3ON2rUk
🚨 NEW WITHDRAWAL!
👤 Kalim Kalimullah
🎯 100 Subs
🔗 https://youtube.com/@kalimkhan-ql8tr?si=HYwq-vEKw2hvD7ab
🚨 NEW WITHDRAWAL!
👤 DC Official
🎯 100 Subs
🔗 https://www.youtube.com/@ChecheeEduHub
🚨 NEW WITHDRAWAL!
👤 Lalladevda Lalladevda
🎯 200 Subs
🔗 https://youtube.com/@lofimusic7723.p?si=rjx90yOTXXxKnyrz
🚨 NEW WITHDRAWAL!
👤 S. K
🎯 200 Subs
🔗 https://youtube.com/@raiwarrior10k?si=LhtaLC-5OIyuH2
🚨 NEW WITHDRAWAL REQUEST!
👤 User: My Channel
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@bgmiluckylive?si=Etb7-czgqV98c9qZ
🚨 NEW WITHDRAWAL REQUEST!
👤 User: 10vs10
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@anni-i7b?si=IscGwAV1v8NgOCbM
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Ashoksing
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@djashokthakor-m5f?si=rULj7lMLN0KNxg-L
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Pawan Wagh
🎯 Target: 200 Subs
🔗 Link: https://youtube.com/@yugsakshswarajya?si=gJbIJSJxuvzyDaei
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Karan Kumar
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@nishadgaming2.0-s6f?si=wldPuIyX7fm8UcPB
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Shadow Queen
🎯 Target: 200 Subs
🔗 Link: https://youtube.com/@shadowqueen-u9n?si=7QFfymGmIFcgpdeA
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Nisha
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@nishaisart05?si=EZyFI9Q7oME0dkB-
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Shiv
🎯 Target: 200 Subs
🔗 Link: https://youtube.com/@kingh-gm?si=IrM8xmf3wnrOWD9w
🚨 NEW WITHDRAWAL REQUEST!
👤 User: My Channel
🎯 Target: 200 Subs
🔗 Link: https://youtube.com/@fuccheyvlogger?si=Php-X-RgIMoOS8y-
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Anuj
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@onceupon-plotbloom?si=2Y-RZIYQDsORY066
🚨 NEW WITHDRAWAL REQUEST!
👤 User: My Channel
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@c2video1?si=R6asLssrvjUXIjbK
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Rajnish Raj
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@rrajj777?si=SiGHCwrbnoHYV-vM
🚨 NEW WITHDRAWAL REQUEST!
👤 User: DX DEMOON
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@dxdemoon?si=PSCmJu7GvGQPP5rU
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Akash BL
🎯 Target: 100 Subs
🔗 Link: https://www.youtube.com/@AkashNaik-r8y
🚨 NEW WITHDRAWAL REQUEST!
👤 User: 💕💗
🎯 Target: 100 Subs
🔗 Link: https://youtube.com/@royalpassguru?si=6VtPE8k0fSdLjXRF
🚨 NEW WITHDRAWAL REQUEST!
👤 User: bhola
🎯 Target: 100 Subs
🔗 Link: https://www.youtube.com/@Anurag-beniwal
🚨 NEW WITHDRAWAL REQUEST!
👤 User: My Channel
🎯 Target: 200 Subs
🔗 Link: https://youtube.com/@traditionaltouchart?si=fDFX1L62dzYfWym0
🚨 NEW WITHDRAWAL REQUEST!
👤 User: Rajat ai studio
🎯 Target: 100 Subs
🔗 Link: https://www.youtube.com/@Rajataistudio
colour prediction 
200
https://www.youtube.com/@Colourpredictionhacktricks
Naveen kumar
100
https://www.youtube.com/@shadow-apk07
sharawan mishra
100
https://www.youtube.com/@hackedmodapk101
Rajat mod 
100
https://www.youtube.com/@apkm0d
clore 
100
https://www.youtube.com/@clore_pradctiom
killer
100
https://www.youtube.com/@Killmodapk
Ghost
200
https://www.youtube.com/@GhostModApk/videos
free fire
100
https://www.youtube.com/@firemodapk801
trizal 
100
https://www.youtube.com/@TrillzMods
MJ GURU
100
https://www.youtube.com/@mjmodsapk9812
Vaibhav Tripathi 
200
https://www.youtube.com/@vaibhavias00001
guru jii
100
https://www.youtube.com/@vaibhavtripathi015
coach
200
https://www.youtube.com/@universalvaibhavtripathivo355
badshah
100
https://www.youtube.com/@vaibhavxtripathi
fit 26
100
https://www.youtube.com/@vaibhavspitfire
rajan
200
https://www.youtube.com/@Rajansir_2.O
fitness ka badsah 
100
https://www.youtube.com/@rajanfitnessseries7458
Rajeev guru
100
https://www.youtube.com/@rajeevguru4510
aman yadav
100
https://www.youtube.com/@AMANYADAV-skb12
Rahul raza
200
https://www.youtube.com/@Rahman-s1b9z
bittu Bhai official 
100
https://www.youtube.com/@bittuvhai3673
roahn sah 
200
https://www.youtube.com/@rohanshah_vlogs
rakhal entrepreneur
100
https://www.youtube.com/@YouTubeReaction-p8w
aman cretor
100
https://www.youtube.com/@amancreator-2
Vikash morya vlogging 
100
https://www.youtube.com/@vikashmoryavlog3391
Raju official 
200
https://www.youtube.com/@rajuoffical887
deshi cretor 
100
https://www.youtube.com/@desicreator__11
ecom Rahul dave
100
https://www.youtube.com/@ECOMRAHULDAVE
mehul s
100
https://www.youtube.com/@Desigemar-y6
jash e bran
200
https://www.youtube.com/@jashnebahara1022
Vicky 44
100
https://www.youtube.com/@Vicky44ff
Ramesh babu
200
https://www.youtube.com/@Rameshbabu-d2c2k
nirob gaming YT
100
https://www.youtube.com/@NIROBGAMING-25
xm bittu
100
https://www.youtube.com/@bittu_vlog_97
ahamad Raza official 
100
https://www.youtube.com/@Ahmedrazaofficial22-j8b
my vlog 88 
100
https://www.youtube.com/@ChapaNagarjunareddy
anjalli mishra
200
https://www.youtube.com/@Anjalivlog88
subham modi
100
https://www.youtube.com/@TheShubhamModi
kumar
100
https://www.youtube.com/@kumarshubhammodi1822
dj thakur
200
https://www.youtube.com/@DjMonuThakur-04
bunty official 
200
https://www.youtube.com/@buntyofficial666
bunuuu 07
200
https://www.youtube.com/@Buntyofficial143x2z
shushel 
200
https://www.youtube.com/@susheelbuntyofficial
ashiq creter
100
https://www.youtube.com/@RockStar-bq9uc
aarya patel
100
https://www.youtube.com/@meetpatel8240
Mr. nobady
200
https://www.youtube.com/@Mrnobody-l3s
dancer piyasha
200
https://www.youtube.com/@Dancersingerpiyasha9876
gyan online Wala 
100
https://www.youtube.com/@gyanonlinewala4690
Faizan aviation 
100
https://www.youtube.com/@fizanplayz
APNA Banda 
100
https://www.youtube.com/@TheApnaBanda
vlog factory
100
https://www.youtube.com/@MkVLOG_FACTORY
epic 
100
https://www.youtube.com/@Epic_vlog_factory
just vibing 
200
https://www.youtube.com/@justvibing8264
golu music 
200
https://www.youtube.com/@GoluMusic033
Tecno raju
200
https://www.youtube.com/@TechnoRaju07
one minute change life
100
https://www.youtube.com/@1MinuteChangedLives
depak tasha 2
100
https://www.youtube.com/@DEPAKTASHA2
deshi daxa
200
https://www.youtube.com/@Kritika_Patel_206
Anjali divedi
100
https://www.youtube.com/channel/UC0Z1et4efnY-lA4VRNzzT4g
no name YT
100
https://www.youtube.com/@NONAMEYT-06
babu moshai vlog
200
https://www.youtube.com/@BabuMoshaiVlogs
the local boy
200
https://www.youtube.com/@LOCALboy-w8w
Sagar Singh chohaun 
100
https://www.youtube.com/@YoutuberSagarSinghChouhan
flutter a feeling 
100
https://www.youtube.com/@%E0%A4%B8%E0%A5%8D%E0%A4%AA%E0%A4%82%E0%A4%A6%E0%A4%A8-%E0%A4%8F%E0%A4%95%E0%A4%85%E0%A4%A8%E0%A5%81%E0%A4%AD%E0%A5%82%E0%A4%A4%E0%A4%BF
pintu tiwari
200
https://www.youtube.com/@PintuTiwariVlogs
awara earning 
100
https://www.youtube.com/@AwaraearningWala
official Zoya khan
100
https://www.youtube.com/@amreenkhan9035
crazy chacha AI
100
https://www.youtube.com/@CrazychachaAi
vertex education
100
https://www.youtube.com/@vertexeducation28
daily junction
200
https://www.youtube.com/@DailyJunction-q8k
ananthu rakesh
100
https://www.youtube.com/@ananthurakesh
Mr chil
100
https://www.youtube.com/@ramanyadav8829
Sonu Rajput vlog
100
https://www.youtube.com/@Sonurajputvlogs1704
pais on point
200
https://www.youtube.com/@PaisaonPoint
rocky music
100
https://www.youtube.com/@Rocky_musicworld
random talk
200
https://www.youtube.com/@randamtalkwithom
Neha Gupta
200
https://www.youtube.com/@nehaguptamakeover_
deshi rockstar comedy
200
https://www.youtube.com/@Desi.rockstar.Comedy
Mohit live
100
https://www.youtube.com/@MohitPlays-exe
Kya seen he
100
https://www.youtube.com/@kya.scenehai
jatin 08
100
https://www.youtube.com/@Jatinbasista
Bhai log
100
https://www.youtube.com/@BhaiLog_10
the simple life
100
https://www.youtube.com/@sukhanmann2615
raj official
200
https://www.youtube.com/@RajOfficial97550
chintu vlog
200
https://www.youtube.com/@Chintuu7704
zero to hero prep
100
https://www.youtube.com/@ZeroToHeroPrep
Imran saikh
100
https://www.youtube.com/@imranshaikh1496
only time pass
100
https://www.youtube.com/@Onlytimepass1-teem
backed nepkin
100
https://www.youtube.com/@realbakednapkins
Vicky yadaw fit
100
https://www.youtube.com/@Vikkyyadav06
submit india
100
https://www.youtube.com/@sumitindiawale7250
full paisa
100
https://www.youtube.com/@NS_TEAM-55
neha gupta
100
https://www.youtube.com/@NehaGupta-431
the astrologer
200
https://www.youtube.com/@theunknownastrologer009
unkwon 
100
https://www.youtube.com/@Talha_Imran
aurra999
200
https://www.youtube.com/@lakshmanfect00
bindass bandda
200
https://www.youtube.com/@Bindassbanda-1
vicky official 
200
https://www.youtube.com/@VICKY_OFFICIAL-e6u
life with karan
100
https://www.youtube.com/@LIFEWITHKARAN-G
Priya patel
200
https://www.youtube.com/@Priyasp-11
raju 26
100
https://www.youtube.com/@rd-raju26live
Raju bhai life style 
200
https://www.youtube.com/@SANUBHAILIFESTYLE
pandit shreee
100
https://www.youtube.com/@panditshrinitinsharma
NITIN
100
https://www.youtube.com/@NitinSharma1243
Mona Sharma
100
https://www.youtube.com/@designsbymona
Dishu
100
https://www.youtube.com/@DishuVlogistan
market ka sultan
100
https://www.youtube.com/@MarketKaSultan
Boom style vlog
200
https://www.youtube.com/@boomstylevlog1787
sartaz YT
100
https://www.youtube.com/@Sartajyt_007
cotton
100
https://www.youtube.com/@CottonMeansFai
pasha official 
200
https://www.youtube.com/@Pasha_Official1
XEX1
200
https://www.youtube.com/@ZEX1_FF
Malik imran
100
https://www.youtube.com/@malikimranawan891
T REX CT
200
https://www.youtube.com/@t-rexct1400
MT travels 
100
https://www.youtube.com/@btbt22
EL padre
100
https://www.youtube.com/@ElPadreCoreano
AND showzZ
100
https://www.youtube.com/@andshowzz3507
maham
100
https://www.youtube.com/@MahamvlogsG
suraj Official
100
https://www.youtube.com/@powerplushsg3369
volt 14 open
100
https://www.youtube.com/@Volt14Open25
24 mod
200
https://www.youtube.com/@The24VoltMod
YAQWEEN
200
https://www.youtube.com/@YA-QEEN
ARtera servies
100
https://www.youtube.com/@arteraservices5637
Alice in chains 
100
https://www.youtube.com/channel/UCjtMrcJSQnXyE0rGfQlr8MA
vince
100
https://www.youtube.com/channel/UCJYwelIYjEgx_qmDc7A57bg
hype valleyball
100
https://www.youtube.com/@hypevolleyball7660
Leims
200
https://www.youtube.com/@Liems_X2779
F. Scokttt
200
https://www.youtube.com/channel/UCIwnw465uViefv4kntXabKQ
cows topic 
100
https://www.youtube.com/channel/UC4prk7JyVpdAd0iXB_sBj0A
ALi hassan
100
https://www.youtube.com/channel/UC3uYKDB22l-1o4A43IF4LcQ
supiro
100
https://www.youtube.com/@SuperiorPumpMinneapolis
all-around dad
100
https://www.youtube.com/@TheRealAllAroundDad
army 6x6 llc
100
https://www.youtube.com/@army6x6llc46
beat vlog
100
https://www.youtube.com/@beatvlog9709
luvysbibi
200
https://www.youtube.com/@Ahy_luvys
Aarti patel
200
https://www.youtube.com/@Aarti_official12
St4r
100
https://www.youtube.com/@hey_May.superStarYT
2pac topic
200
https://www.youtube.com/channel/UC5RrGzC-JXglhFW5NhT4r6w
Tony Don
200
https://www.youtube.com/@tonydon5315
Concret
100
https://www.youtube.com/@ConcreteandCampfire
super x power
100
https://www.youtube.com/@superxpowercenter
lucky play
100
https://www.youtube.com/@iamluckyy29
Andy
200
https://www.youtube.com/@ajacobson1567
The royal gaming
100
https://www.youtube.com/@TheRoyalGamingCommunity
Tesla
100
https://www.youtube.com/channel/UCqiudDrtwQfFcoQeE0lIdFQ
sun fall music
100
https://www.youtube.com/@SunFallsMusic
sakha
100
https://www.youtube.com/@SakhaaNR
THE last
200
https://www.youtube.com/@thelastsheltercom2515
Quatro
100
https://www.youtube.com/@QuattroQuattroDos
momine
200
https://www.youtube.com/@MomineNL
hulking 93
100
https://www.youtube.com/@Hulkling93
Ever 
200
https://www.youtube.com/@EverCuriousGeek
sr arman
100
https://www.youtube.com/@sr_arman_6
electronic 2.0
200
https://www.youtube.com/@srelectronic2.017
Tobi on Tor
100
https://www.youtube.com/@VoltventuresHD
DJ sanjib
200
https://www.youtube.com/@djsanjibsrediting5461
sanjay
100
https://www.youtube.com/@sanjaysainisrelectricals783
ZStarr
200
https://www.youtube.com/@zstarr7084
Fox BR
200
https://www.youtube.com/@batphonk..417
vlog techTV
100
https://www.youtube.com/@VlogTechtv
Mr. Utkrash
100
https://www.youtube.com/@utkarshyadav946
senor ledsma
200
https://www.youtube.com/@SE%C3%91ORLEDESMA
ikraGMbh
100
https://www.youtube.com/@ikraGmbH
auto india
200
https://www.youtube.com/@EVolutionautoindia
time Zone
100
https://www.youtube.com/@MikeJackson-r3n
SR inveter
200
https://www.youtube.com/@SRINVENTOR85
Tecnision
100
https://www.youtube.com/@TechnicianNagareYogesh
Rlexhum
200
https://www.youtube.com/@relxum
GiamGhd
100
https://www.youtube.com/@Giaamyy
Blue haze
200
https://www.youtube.com/@tallscreen59
yearbook
200
https://www.youtube.com/@cuhsyearbook9660
mr blue
100
https://www.youtube.com/@Spaghettigalaxy
wild nation
100
https://www.youtube.com/@WildnNation7
BG
100
https://www.youtube.com/@bimalghising-kw8wm
Gotta Experimint
200
https://www.youtube.com/@GotaExperiment
Brak Obama
100
https://www.youtube.com/channel/UC3UfxzNhADJd66euR10kOXg
iknivie
100
https://www.youtube.com/@iKnivie
bts army
100
https://www.youtube.com/@SunilSahani-c3n
canal fechado
200
https://www.youtube.com/@RedeGlobo-mg3kr
D grind
100
https://www.youtube.com/@D-Grind
Kevin Fox filme
200
https://www.youtube.com/@Kevinfoxfilms
KG
100
https://www.youtube.com/@kiraly_gergo
ariveda
100
https://www.youtube.com/@ariveder4i
ham sab sath
200
https://www.youtube.com/@Hamsabsath05
mark 722
100
https://www.youtube.com/@MarkGaming722
The gaming garz
200
https://www.youtube.com/@TheGeminiGarage
star network
200
https://www.youtube.com/@StarnetworkHu
Jupinder soul
100
https://www.youtube.com/@jupindersohal5713
alysaa
200
https://www.youtube.com/@alyssadetorres1243
every thing
100
https://www.youtube.com/@everythingunboxer2584
motar
200
https://www.youtube.com/@dertsizmotor
volt070
100
https://www.youtube.com/@volt070
don
100
https://www.youtube.com/@DonChonggo
king Grego TV
100
https://www.youtube.com/@KINGGEORGETV1223
adelo
100
https://www.youtube.com/@AdeloAngel
JL kapos
100
https://www.youtube.com/@JanmarkAlburo
DJ tatooo
100
https://www.youtube.com/@DjTattooartist
Milky baza
100
https://www.youtube.com/@Milkybaja
Luna JR
100
https://www.youtube.com/@victort.lunajr.2547
dabbing malu
200
https://www.youtube.com/@victort.lunajr.2547
boy sensor
100
https://www.youtube.com/@boysensorcebuphilippines
mishra sir classess
100
https://www.youtube.com/@MishraSirClasses-123
Tamashree
200
https://www.youtube.com/@tamashreemisra
aman vlog
200
https://www.youtube.com/@AmanMisraVlogs
sauraw yadaw
100
https://www.youtube.com/channel/UCmd7VIKMHpOgdme_yZGQLvg
Ujala topic
200
https://www.youtube.com/channel/UCXa-_QeWb-6G5IoElonwVdw
Verma visual 
200
https://www.youtube.com/@VERMAVISUALS
Shivam YT
200
https://www.youtube.com/@shivamvermamt
Krishna mT
200
https://www.youtube.com/@KRISHNAVERMAMT
rathod nikku
200
https://www.youtube.com/@Nikku_2.0
its Suhani video
100
https://www.youtube.com/@itssuhanivideos
thakur 
200
https://www.youtube.com/@Suhanithakur-r4i
mo aman
100
https://www.youtube.com/@kingkhanchannel2558
Travel with rajat
100
https://www.youtube.com/@travelwithrajat1621
rohit
100
https://www.youtube.com/@RohitRajat07
"""

# ================= LIST PARSERS =================
def parse_golden_data(raw_text):
    parsed = []
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            parsed.append({
                "name": lines[i],
                "total": "1,000",
                "link": lines[i+1],
                "is_golden": True
            })
    return parsed

def parse_normal_data(raw_text):
    parsed = []
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    clean_lines = []
    for line in lines:
        if "🚨" in line: continue
        
        line = line.replace("👤 User:", "").replace("👤", "").strip()
        line = line.replace("🎯 Target:", "").replace("🎯", "").replace("Subs", "").strip()
        line = line.replace("🔗 Link:", "").replace("🔗", "").strip()
        
        clean_lines.append(line)
        
    for i in range(0, len(clean_lines), 3):
        if i + 2 < len(clean_lines):
            parsed.append({
                "name": clean_lines[i],
                "total": clean_lines[i+1],
                "link": clean_lines[i+2],
                "is_golden": False
            })
    return parsed

# ================= QUEUE MANAGEMENT (FIXED LOGIC) =================
def generate_fresh_queue():
    normal = parse_normal_data(RAW_NORMAL)
    golden = parse_golden_data(RAW_GOLDEN)
    
    random.shuffle(normal)
    random.shuffle(golden)
    
    queue = []
    consecutive_normal = 0
    
    # Decide initial target gap (1, 2, or 3)
    target_gap = random.randint(1, 3)
    
    while normal or golden:
        if normal and golden:
            if consecutive_normal >= target_gap:
                queue.append(golden.pop(0))
                consecutive_normal = 0
                target_gap = random.randint(1, 3) # Naya gap set karega
            else:
                queue.append(normal.pop(0))
                consecutive_normal += 1
        elif normal:
            # Agar bas normal bache hain
            queue.append(normal.pop(0))
        elif golden:
            # Agar bas golden bache hain
            queue.append(golden.pop(0))
            
    return queue

def get_next_proof():
    queue = []
    
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        except:
            pass
            
    if not queue:
        queue = generate_fresh_queue()
        print(f"🔄 Naya 7-Day Cycle shuru! Total {len(queue)} messages queued.")
        
    proof = queue.pop(0)
    
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=4)
        
    return proof, len(queue)

# ================= MESSAGE BUILDER =================
def generate_message(proof):
    if proof.get("is_golden"):
        return f"""**🏆 GOLDEN MEMBER** 

**🎉 Congratulations, {proof['name']}**

**✅ Aapke YouTube Channel par 1,000 Subscribers successfully add ho gaye hain! 🚀**

**🔗 Aapki Channel Link: 👇🏻**
**{proof['link']}**

**📈 Aur Subscribers badhane ke liye**
**👇🏻 Abhi yahan click karein 👇🏻**

**✨ Thank you for being a Golden Member! 💛**"""
    else:
        return f"""🏆Congratulations **{proof['name']}**
✅ Aapke YouTube channel par **{proof['total']}** Subscribers Successfully Add ho gaye hain! 🎯

🔗 Aapki Link:   Please chack

{proof['link']}
🚀Apne YouTube Channel par aur Subscribers badhane ke liye abhi click karein 👇🏻"""

# ================= BOT SEND LOGIC =================
async def send_proof(client):
    try:
        proof, remaining = get_next_proof()
        message = generate_message(proof)

        await client.send_message(
            TARGET_CHANNEL,
            message,
            buttons=[
                Button.url("📈 100 Subscribers", BUTTON_LINK)
            ],
            parse_mode='md'
        )

        msg_type = "GOLDEN" if proof.get("is_golden") else "NORMAL"
        print(f"✅ {msg_type} Message sent | Remaining in cycle: {remaining}")
        return True

    except Exception as e:
        print("❌ Error:", e)
        return False

# ================= SCHEDULER =================
async def scheduler(client):
    while True:
        now = datetime.now(IST)
        hour = now.hour

        if 6 <= hour < 22:
            success = await send_proof(client)
            if success:
                delay = random.choice([16, 17, 18])
                print(f"⏳ Day Mode: Next message in {delay} minutes")
                await asyncio.sleep(delay * 60)
            else:
                await asyncio.sleep(60)

        elif 0 <= hour < 5:
            success = await send_proof(client)
            if success:
                delay = random.choice([35, 40, 45])
                print(f"🌙 Night Mode: Next message in {delay} minutes")
                await asyncio.sleep(delay * 60)
            else:
                await asyncio.sleep(60)

        else:
            print("⏸ Pause Mode: Waiting for next active time window...")
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
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    print("🤖 Bot started successfully")

    await asyncio.gather(
        scheduler(client),
        keep_alive()
    )

if __name__ == "__main__":
    asyncio.run(main())
