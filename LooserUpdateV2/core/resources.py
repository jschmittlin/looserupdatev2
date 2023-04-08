import discord

# List of activities
ACTIVITIES = [
    discord.Activity(type=discord.ActivityType.watching, name="you"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi put pressure on"),
    discord.Activity(type=discord.ActivityType.watching, name="Medhi be shadow ban"),
    discord.Activity(type=discord.ActivityType.watching, name="botlane feed"),
    discord.Activity(type=discord.ActivityType.watching, name="Jérôme farmer these jungle camps"),
    discord.Activity(type=discord.ActivityType.listening, name="Valentin raging"),
    discord.Activity(type=discord.ActivityType.listening, name="La déprime"),
    discord.Game(name="for /help"),
    discord.Game(name="at tracking down losers"),
    discord.Game(name="Blitzcrank's Poro Roundup"),
    discord.Game(name="Doom Bots"),
    discord.Game(name="to support KCorp !"),
]

class Icon:
    emrata = 'https://cdn.discordapp.com/attachments/598865284786552852/1037836694327672952/EMRATA_008a.jpg'
    nav_profile = 'https://cdn.discordapp.com/attachments/598865284786552852/1039235266428284948/nav-icon-profile.png'
    error = 'https://cdn.discordapp.com/attachments/598865284786552852/1039234765355761755/alpha_watermark_vector.png'
    error_image = 'https://cdn.discordapp.com/attachments/1039594104759271428/1063602226729340928/EMRATA_024a.jpg'
    poro_mission = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064310061083656203/missiontracker_poro2.png'
    poro_voice = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064310061314347078/voice-poro2.png'
    poro_error = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064310060815229008/error_poro2.png'
    ha_victory = 'https://cdn.discordapp.com/attachments/1039594104759271428/1042110183339479100/icon-ha-victory.png'
    ha_defeat = 'https://cdn.discordapp.com/attachments/1039594104759271428/1042110182844547082/icon-ha-defeat.png'
    sr_victory = 'https://cdn.discordapp.com/attachments/1039594104759271428/1042110182534164501/icon-sr-victory.png'
    sr_defeat = 'https://cdn.discordapp.com/attachments/1039594104759271428/1042110183771488276/icon-sr-defeat.png'
    setting = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064249149589032991/icon_settings.png'
    book = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064248147246842007/npe-rewards-book.png'
    search = 'https://cdn.discordapp.com/attachments/1039594104759271428/1064303925014044832/search-icon.png'

    transfer = {
        'BR':'<:br:1064310835511558174>',
        'EUNE':'<:eune:1064310837755519007>',
        'EUW':'https://cdn.discordapp.com/attachments/1039594104759271428/1064314656203751454/euw.jpg',
        'JP':'<:jp:1064310840779616358>',
        'KR':'<:transfer:1064311427520807013>',
        'LAN':'<:lan:1064310842608336966>',
        'LAS':'<:las:1064310843929538660>',
        'NA':'<:na:1064310844881653782>',
        'OCE':'<:oce:1064310847184310292>',
        'RU':'<:ru:1064310848543281253>',
        'TR':'<:tr:1064310849830924291>',
        'PH':'<:transfer:1064311427520807013>',
        'SG':'<:transfer:1064311427520807013>',
        'TH':'<:transfer:1064311427520807013>',
        'TW':'<:transfer:1064311427520807013>',
        'VN':'<:transfer:1064311427520807013>'
    }


class Color:
    default = 0x715248
    victory = 0x0f93ad
    defeat = 0xa42f3f
    error = 0xc8181b
    success = 0x017846


class Emoji:
    blank = '<:__:1039602543711506554>'

    tier = {
        'UNRANKED':'<:unranked:1039599336901853195>',
        'IRON':'<:iron:1039599357961453668>',
        'BRONZE':'<:bronze:1039599374923214878>',
        'SILVER':'<:silver:1039599394066018327>',
        'GOLD':'<:gold:1039599411854053428>',
        'PLATINUM':'<:platinum:1039599426144059432>',
        'DIAMOND':'<:diamond:1039599441507778661>',
        'MASTER':'<:master:1039599494548955176>',
        'GRANDMASTER':'<:grandmaster:1039599509539393648>',
        'CHALLENGER':'<:challenger:1039599527142899754>',
    }

    position = {
        'TOP':'<:top:1039599155561119884>',
        'JUNGLE':'<:jungle:1039599138616135740>',
        'MIDDLE':'<:mid:1039599123474690108>',
        'BOTTOM':'<:bottom:1039599103610466375>',
        'UTILITY':'<:support:1039599010622742610>',
        'FILL':'<:fill:1039599006847877232>',
    }

    mastery = {
        'default':'<:mastery:1040643274748199012>',
        'Level_7':'<:mastery7:1040643283870822471>',
        'Level_6':'<:mastery6:1040643282616725504>',
        'Level_5':'<:mastery5:1040643281391976489>',
        'Level_4':'<:mastery4:1040643280112734348>',
        'Level_3':'<:mastery3:1040643278904762368>',
        'Level_2':'<:mastery2:1040643277554208798>',
        'Level_1':'<:mastery1:1040643276073603082>',
        'Level_0':'<:default:1040643273410232350>',
    }

    aram = {
        'defeat': '<:ha_defeat:1041775274125176913>',
        'victory': '<:ha_victory:1041775275618349066>',
    }

    sr = {
        'defeat':'<:sr_defeat:1041775277119901706>',
        'victory':'<:sr_victory:1041775278621478992>',
    }

    history = {
        'cs':'<:maskcs:1041806238335389786>',
        'gold':'<:maskgold:1041806240080212128>',
        'kda':'<:maskkda:1041806241346891886>',
        'tower':'<:tower100:1043700612010868827>',
        'inhibitor':'<:inhibitor100:1043700610953912401>',
        'baron':'<:baron100:1043700607040634890>',
        'dragon':'<:dragon100:1043700608152129588>',
        'herald':'<:herald100:1043700609854996480>',
    }

    rune = {
        'Arcane Comet':'<:ArcaneComet:1042199944737599542>',
        'Conqueror':'<:Conqueror:1042199946360786976>',
        'Dark Harvest':'<:DarkHarvest:1042199948353097768>',
        'Electrocute':'<:Electrocute:1042199950508970084>',
        'First Strike':'<:FirstStrike:1042199960399126658>',
        'Fleet Footwork':'<:FleetFootwork:1042199962001358878>',
        'Glacial Augment':'<:GlacialAugment:1042199963825877042>',
        'Grasp of the Undying':'<:GraspOfTheUndying:1042199965432299680>',
        'Guardian':'<:Guardian:1042199967189696602>',
        'Hail of Blades':'<:HailOfBlades:1042199968489930854>',
        'Lethal Tempo':'<:LethalTempoTemp:1042199970402537512>',
        'Phase Rush':'<:PhaseRush:1042199971732148225>',
        'Predator':'<:Predator:1042199973862850661>',
        'Press the Attack':'<:PressTheAttack:1042199975720910959>',
        'Summon Aery':'<:SummonAery:1042199978724036668>',
        'Unsealed Spellbook':'<:UnsealedSpellbook:1042199980791844894>',
        'Aftershock':'<:VeteranAftershock:1042199982549237800>',
        'Runes':'<:RunesIcon:1042199976995979274>'
    }

    summoner = {
        'SummonerBarrier':'<:SummonerBarrier:1041777999562932335>',
        'SummonerBoost':'<:SummonerBoost:1041778000800256070>',
        'SummonerDot':'<:SummonerDot:1041778001970479155>',
        'SummonerExhaust':'<:SummonerExhaust:1041778003396538420>',
        'SummonerFlash':'<:SummonerFlash:1041778004847755325>',
        'SummonerHaste':'<:SummonerHaste:1041778006072492113>',
        'SummonerHeal':'<:SummonerHeal:1041778007444033607>',
        'SummonerMana':'<:SummonerMana:1041778008681369620>',
        'SummonerPoroRecall':'<:SummonerPoroRecall:1041778009897709688>',
        'SummonerPoroThrow':'<:SummonerPoroThrow:1041778011449593897>',
        'SummonerSmite':'<:SummonerSmite:1041778013056016434>',
        'SummonerSnowURFSnowball_Mark':'<:SummonerSnowURFSnowball_Mark:1041778015312564365>',
        'SummonerSnowball':'<:SummonerSnowball:1041778014196871219>',
        'SummonerTeleport':'<:SummonerTeleport:1041778016411471882>',
        'Summoner_UltBookPlaceholder':'<:Summoner_UltBookPlaceholder:1041777996429799495>',
        'Summoner_UltBookSmitePlaceholder':'<:Summoner_UltBookSmitePlaceholder:1041777998321426442>'
    }

    champion = {
        'None':'<:none:1043970313454628904>',
        'Aatrox':'<:Aatrox:1039637423124136126>',
        'Ahri':'<:Ahri:1039637424164319334>',
        'Akali':'<:Akali:1039637425259036723>',
        'Akshan':'<:Akshan:1039637427528138802>',
        'Alistar':'<:Alistar:1039637429025517609>',
        'Amumu':'<:Amumu:1039637430187331676>',
        'Anivia':'<:Anivia:1039637431890231306>',
        'Annie':'<:Annie:1039637433102376970>',
        'Aphelios':'<:Aphelios:1039637434373247067>',
        'Ashe':'<:Ashe:1039637435618951280>',
        'Aurelion Sol':'<:AurelionSol:1039637437011468348>',
        'Azir':'<:Azir:1039637438492061757>',
        'Bard':'<:Bard:1039637439599349770>',
        "Bel'veth":'<:Belveth:1039637440719241276>',
        'Blitzcrank':'<:Blitzcrank:1039637441923006534>',
        'Brand':'<:Brand:1039637443181281350>',
        'Braum':'<:Braum:1039637444385054780>',
        'Caitlyn':'<:Caitlyn:1039637445853069322>',
        'Camille':'<:Camille:1039637447392378900>',
        'Cassiopeia':'<:Cassiopeia:1039637449112043571>',
        "Cho'Gath":'<:Chogath:1039637450462605422>',
        'Corki':'<:Corki:1039637451637014548>',
        'Darius':'<:Darius:1039637452819812472>',
        'Diana':'<:Diana:1039637454212313108>',
        'Draven':'<:Draven:1039637455684501584>',
        'Dr. Mundo':'<:DrMundo:1039637456712110171>',
        'Ekko':'<:Ekko:1039637458272403527>',
        'Elise':'<:Elise:1039637459467784314>',
        'Evelynn':'<:Evelynn:1039637461640425552>',
        'Ezreal':'<:Ezreal:1039637462621900891>',
        'FiddleSticks':'<:Fiddlesticks:1039637464010211439>',
        'Fiora':'<:Fiora:1039637465520144414>',
        'Fizz':'<:Fizz:1039637466744889375>',
        'Galio':'<:Galio:1039637468175155240>',
        'Gangplank':'<:Gangplank:1039637469387300934>',
        'Garen':'<:Garen:1039637470742073385>',
        'Gnar':'<:Gnar:1039637471794831431>',
        'Gragas':'<:Gragas:1039637473447383090>',
        'Graves':'<:Graves:1039637474399502338>',
        'Gwen':'<:Gwen:1039637476446310543>',
        'Hecarim':'<:Hecarim:1039637477712990238>',
        'Heimerdinger':'<:Heimerdinger:1039637479046787245>',
        'Illaoi':'<:Illaoi:1039638004253331507>',
        'Irelia':'<:Irelia:1039638005486456942>',
        'Ivern':'<:Ivern:1039638007185149993>',
        'Janna':'<:Janna:1039638008518942730>',
        'Jarvan IV':'<:JarvanIV:1039638009512996986>',
        'Jax':'<:Jax:1039638011077460078>',
        'Jayce':'<:Jayce:1039638013216571415>',
        'Jhin':'<:Jhin:1039638014630043658>',
        'Jinx':'<:Jinx:1039638016102240406>',
        "Kai'Sa":'<:Kaisa:1039638017461202954>',
        'Kalista':'<:Kalista:1039638018832736266>',
        'Karma':'<:Karma:1039638020711784488>',
        'Karthus':'<:Karthus:1039638021693247550>',
        'Kassadin':'<:Kassadin:1039638023178047588>',
        'Katarina':'<:Katarina:1039638024390193183>',
        'Kayle':'<:Kayle:1039638025736573020>',
        'Kayn':'<:Kayn:1039638027435249674>',
        'Kennen':'<:Kennen:1039638028764840006>',
        "Kha'Zix":'<:Khazix:1039638029645648107>',
        'Kindred':'<:Kindred:1039638031126241302>',
        'Kled':'<:Kled:1039638033001107566>',
        "Kog'Maw":'<:KogMaw:1039638034532016168>',
        "K'Sante":'<:KSante:1039638035282796575>',
        'LeBlanc':'<:Leblanc:1039638036817915944>',
        'Lee Sin':'<:LeeSin:1039638038306893944>',
        'Leona':'<:Leona:1039638039732961300>',
        'Lillia':'<:Lillia:1039638041146437712>',
        'Lissandra':'<:Lissandra:1039638042492817621>',
        'Lucian':'<:Lucian:1039638043977588815>',
        'Lulu':'<:Lulu:1039638045768560810>',
        'Lux':'<:Lux:1039638047500808214>',
        'Malphite':'<:Malphite:1039638048587141200>',
        'Malzahar':'<:Malzahar:1039638049765720194>',
        'Maokai':'<:Maokai:1039638050663317516>',
        'Master Yi':'<:MasterYi:1039638052156481586>',
        'Miss Fortune':'<:MissFortune:1039638053326704671>',
        'Mordekaiser':'<:Mordekaiser:1039638055864246362>',
        'Morgana':'<:Morgana:1039638057277735023>',
        'Nami':'<:Nami:1039638059119030303>',
        'Nasus':'<:Nasus:1039638060163403870>',
        'Nautilus':'<:Nautilus:1039638061522366504>',
        'Neeko':'<:Neeko:1039638062713544876>',
        'Nidalee':'<:Nidalee:1039638064143798482>',
        'Nilah':'<:Nilah:1039638065427267634>',
        'Nocturne':'<:Nocturne:1039638067104993392>',
        'Nunu & Willump':'<:Nunu:1039638068493291650>',
        'Olaf':'<:Olaf:1039638395766448160>',
        'Orianna':'<:Orianna:1039638397100228680>',
        'Ornn':'<:Ornn:1039638398517911593>',
        'Pantheon':'<:Pantheon:1039638399667154965>',
        'Poppy':'<:Poppy:1039638400753479741>',
        'Pyke':'<:Pyke:1039638403861467176>',
        'Qiyana':'<:Qiyana:1039638405547577424>',
        'Quinn':'<:Quinn:1039638406755516496>',
        'Rakan':'<:Rakan:1039638408097693736>',
        'Rammus':'<:Rammus:1039638409406332938>',
        "Rek'Sai":'<:RekSai:1039638410538786816>',
        'Rell':'<:Rell:1039638411780300800>',
        'Renata':'<:Renata:1039638413235720244>',
        'Renekton':'<:Renekton:1039638414519193730>',
        'Rengar':'<:Rengar:1039638416024928367>',
        'Riven':'<:Riven:1039638417530703902>',
        'Rumble':'<:Rumble:1039638418856099871>',
        'Ryze':'<:Ryze:1039638420135366677>',
        'Samira':'<:Samira:1039638421544636508>',
        'Sejuani':'<:Sejuani:1039638423356592198>',
        'Senna':'<:Senna:1039638424581312592>',
        'Seraphine':'<:Seraphine:1039638425944469554>',
        'Sett':'<:Sett:1039638427152416939>',
        'Shaco':'<:Shaco:1039638428666560652>',
        'Shen':'<:Shen:1039638430696624158>',
        'Shyvana':'<:Shyvana:1039638432407900171>',
        'Singed':'<:Singed:1039638434144337972>',
        'Sion':'<:Sion:1039638438024065135>',
        'Sivir':'<:Sivir:1039638439185875105>',
        'Skarner':'<:Skarner:1039638440477728908>',
        'Sona':'<:Sona:1039638441513717782>',
        'Soraka':'<:Soraka:1039638442931408976>',
        'Swain':'<:Swain:1039638445766750338>',
        'Sylas':'<:Sylas:1039638446974713916>',
        'Syndra':'<:Syndra:1039638448258170921>',
        'Tahm Kench':'<:TahmKench:1039638449596137512>',
        'Taliyah':'<:Taliyah:1039638450858639420>',
        'Talon':'<:Talon:1039638452074983484>',
        'Taric':'<:Taric:1039638453362622535>',
        'Teemo':'<:Teemo:1039638454503493744>',
        'Thresh':'<:Thresh:1039638456990711832>',
        'Tristana':'<:Tristana:1039638461600235570>',
        'Trundle':'<:Trundle:1039638463085039677>',
        'Tryndamere':'<:Tryndamere:1039638464704041050>',
        'Twisted Fate':'<:TwistedFate:1039638465798738050>',
        'Twitch':'<:Twitch:1039638466943795231>',
        'Udyr':'<:Udyr:1039659308293554288>',
        'Urgot':'<:Urgot:1039638691745890405>',
        'Varus':'<:Varus:1039638692999987240>',
        'Vayne':'<:Vayne:1039638694547693648>',
        'Veigar':'<:Veigar:1039638695805993012>',
        "Vel'Koz":'<:Velkoz:1039638697257209867>',
        'Vex':'<:Vex:1039638698884608112>',
        'Vi':'<:Vi:1039638700570710017>',
        'Viego':'<:Viego:1039638702068092978>',
        'Viktor':'<:Viktor:1039638703229902868>',
        'Vladimir':'<:Vladimir:1039638704500772924>',
        'Volibear':'<:Volibear:1039638706665037844>',
        'Warwick':'<:Warwick:1039638707923325019>',
        'Wukong':'<:MonkeyKing:1039638054572392468>',
        'Xayah':'<:Xayah:1039638709122912318>',
        'Xerath':'<:Xerath:1039638710137925733>',
        'Xin Zhao':'<:XinZhao:1039638712562241586>',
        'Yasuo':'<:Yasuo:1039638713719865374>',
        'Yone':'<:Yone:1039638715095588974>',
        'Yorick':'<:Yorick:1039638716261613578>',
        'Yuumi':'<:Yuumi:1039638717670883338>',
        'Zac':'<:Zac:1039638718497165323>',
        'Zed':'<:Zed:1039638720342655036>',
        'Zeri':'<:Zeri:1039638721470930965>',
        'Ziggs':'<:Ziggs:1039638723203186738>',
        'Zilean':'<:Zilean:1039638724914466868>',
        'Zoe':'<:Zoe:1039638726449582102>',
        'Zyra':'<:Zyra:1039638727833694228>'
    }
