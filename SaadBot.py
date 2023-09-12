import time
from json import loads
import discord
import discord.ext.commands
import requests
from discord.ext import commands
import random
import datetime
import json
from urllib import parse, request
import humanfriendly
intents = discord.Intents().all()
discord.Intents(guilds=True,members=True,presences=True)






bot = commands.Bot(command_prefix="$", intents=intents, help_command=None, case_insensitive=True)
ingame = False
people = [0, 0]
amountofwords = 3
gamechannel = 0
giphy_api_key = "My Special API Key :)"
link_to_code = "https://gist.github.com/jojo-v-dongen/69494ea08d36b881a6241a7cd64dbc09"
debug_on = True

command_list = ["hug", "cuddle", "gay", "insult", "pog", "send",
                "clear", "movie",
                "watch", "pirate",
                "code", "help", "wordgame"]

@bot.event
async def on_ready():
    #print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your mum undressing"))



gamerules = """
    >>> **__RULES FOR THE MENTALLY CHALLANGED__**
1.  Simple rules, you can only type messages with {} amount of words.
        *If you type fewer or more than {} words, you will get scolded for being an absolute retard.*
2.  AT LEAST 2 other people must have sent a message after your last message to be able to type again.
        *This is to prevent absolute idiots from ruining the entire idea of collaboration.*
3.  Use punctuation so sentences won't go until the end of time.
        *If you can't follow this you should learn basic English instead of spending time on Discord.*
4.  Actually try to continue the story and make it possible for the next person to continue it.
        *I will personally beat up the people who just type {} random words.*
5.  DO NOT tag anyone, idc if you make fun of them in the story by saying their name tho.
        *If you tag someone it will break the bot and instead of @... it'll give a long number.*
    """.format(amountofwords, amountofwords, amountofwords)


@bot.event
async def on_message(message):
    global ingame, amountofwords, gamechannel

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    banned_words = ["uwu", "**uwu**", "_uwu_", "__uwu__", "`uwu`", "u w u", "u   w   u", "owo", "vwv", "pvp"]
    if any(x in message.content.lower() for x in banned_words):
        if str(message.author.id).lower() in ["pickle", "<@761640603930722357>", "zoe", "761640603930722357"]:
            member = message.author
            await member.edit(nick="ZoZo")
        time_timeout = humanfriendly.parse_timespan("30")
        await message.author.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time_timeout), reason="Being a bitch")
        await message.channel.send(f">>> {message.author} got timed out for {time_timeout} seconds.\r**REASON: Being a bitch**\n*and bitches get insulted*")
        insults = ["{} is a gay sprinkle on a gay rainbow.",
                   "If I gave a penny for {} thoughts, I'd get change.",
                   "Hey {}. There is no joke, kill yourself.",
                   "I heard {}'s mum fell over, I hope the damage to the city can be fixed.",
                   "I am going to build a time-machine, grab a dinasour egg and put it in {}'s living room so one day it will kill them.",
                   "Not even the most loyal dog could love {}.",
                   "I ran out of jokes, but I can get more just looking at {}'s life.",
                   "*{} is gay*",
                   "Hey {}, Does your ass ever get jealous of the shit that comes out of your mouth?",
                   "I would agree with {} but then we would both be wrong.",
                   "Stop being mean! {} is not useless. They can be used as a bad example.",
                   "There's a tree creating the oxygen {} is wasting. They should go find it in the woods and apologize",
                   "I'd try to insult {}, but I can't top what nature has already done to them.",
                   "{} is the human equivalent of a participation award",
                   "Slavers would pay to get rid of {}",
                   "If {} went for a swim in the sea, you'd be polluting.\nThen again that would be washing and they sure don't smell like they wash.",
                   "Not even cannibals would want to eat {}."]
        await message.channel.send(random.choice(insults).format(message.author.mention))
        await message.channel.send("The best thing is that they can't even say anything about it <:kek:919548503741575168> ")

    if ingame:
        if "<#" + str(message.channel.id) + ">" == str(gamechannel):
            word_list = message.content.split()
            if len(word_list) != amountofwords:
                await message.delete()
                await message.channel.send("Can you not count you fucking dumbass?", delete_after=3)


            elif message.author.id == people[-1] or message.author.id == people[-2]:
                await message.delete()
                await message.channel.send("Did you not read the fucking rules you cunt?", delete_after=3)
            else:
                people.append(message.author.id)





@bot.command()
@commands.has_role("Administrator")
async def wordgame(ctx, arg, channel='', words=3):
    """
    DISCONTINUED
    """
    global ingame, amountofwords, gamechannel, people
    amountofwords = words
    #print(channel)
    arg = arg.lower()
    if arg == "start":
        if channel == 0:
            await ctx.send("**You didn't specify the #channel dumbass!**")
        else:
            ingame = True
            gamechannel = channel
            await ctx.send("**Let the game begin!**\n||I am sure you won't do as terrible this time :)   ||")
            tempchannel = channel[2:]
            tempchannel = tempchannel[:-1]
            #print(tempchannel)
            channeltosend = bot.get_channel(int(tempchannel))
            await channeltosend.send(gamerules)


    elif arg == "stop":
        await ctx.send("**Wordgame stopped**\ncause you pussied out.")
        ingame = False
        channel = ctx.message.channel.id
        # for c in gamechannel:
        #     #print(c)
        #     if c.isdigit():
        #         channel = channel + c
        #print(channel)
        channel = bot.get_channel(int(channel))
        messages = await channel.history(limit=None, oldest_first=True).flatten()
        ##print(messages)
        people = [0, 0]

        count = 0
        with open("Story.txt", 'w', encoding="utf-8") as f:
            for i in messages:
                count += 1
                f.write(i.content.replace("\n", " ")+" ")
                if count == 10:
                    f.write("\n")
                    count = 0
            f.close()

        with open("Story.txt", 'r') as f:
            await ctx.send("Here is your **GARBAGE** story:", file=discord.File(f, "Story.txt"))
            f.close()
    else:
        await ctx.send("That command doesn't exist you fucking moron!")


@bot.command()
async def hug(ctx):

    """
    What do you think this shit does? It gives a hug!
    """

    await ctx.send(" <:people_hugging:964274854532644945> ")

@bot.command()
async def watch(ctx, *TheMovieName):

    """
    Gives you a link where to watch the movie for free.
    """
    TheMovieName = ' '.join(TheMovieName)
    MovieName = str(TheMovieName).replace(" ", "-")

    #print(MovieName)
    link = f"https://allmoviesforyou.net/{MovieName}"
    responses = requests.get(link)
    check = []


    for response in responses.history:
        check.append(response.url)
        #print(response.url)

    if check:
        embedVar = discord.Embed(title=f"""**Watch "{TheMovieName}" for free at:**""",
                                 description=f"*[AllMoviesForYou]({link})*\n*[Flixtor](https://flixtor.gg/search/{MovieName})*",
                                 color=0x00ff00)
        embedVar.set_image(url="https://i0.wp.com/allmoviesforyou.net/wp-content/uploads/2021/04/cropped-cropped-allmoviesforyou-logo-header-HD.png?w=800&ssl=1")
        await ctx.channel.send(embed=embedVar)


    else:
        link = "https://allmoviesforyou.net/"
        embedVar = discord.Embed(title=f"**SORRY! We could not find this movie on AllMoviesForYou.**",
                                     description=f"Check other search websites:\n*[AllMoviesForYou](https://allmoviesforyou.net)*\n*[Flixtor](https://flixtor.gg)*\n*[123Movies](https://wwv.la123movies.com/search/)*\n*[Vumoo](https://vumoo.to/)*",
                                 color=0x00ff00)
        await ctx.channel.send(embed=embedVar)

@bot.command()
async def pirate(ctx, *TheGameName):

    """
    Gives you a link where to download the game for free.
    """
    TheGameName = ' '.join(TheGameName)
    GameName = str(TheGameName).replace(" ", "-")
    igg_gamename = str(TheGameName).replace(" ", "+")


    #print(GameName)
    link = f"https://agfy.co/{GameName}"
    responses = requests.get(link)
    check = []


    for response in responses.history:
        check.append(response.url)
        link = responses.url

    if check:
        embedVar = discord.Embed(title=f"""**Download "{TheGameName}" for free at:**""",
                                 description=f"*[AllGamesForYou]({link})*\n\n**Or try the search results of these websites!**\n*[igg-games](<https://igg-games.com/?s={igg_gamename}>)*\n*[SteamUnlocked](<https://steamunlocked.net/?s={igg_gamename}>)*",
                                 color=0x00ff00)
        embedVar.set_thumbnail(url="https://agfy.co/wp-content/uploads/2022/02/newalgfylogo-1.png")
        await ctx.channel.send(embed=embedVar)


    else:
        link = "https://allmoviesforyou.net/"
        embedVar = discord.Embed(title=f"**SORRY! We could not find this movie at AllGamesForYou.**",
                                     description=f"Check the search results:\n*[AllGamesForYou](<https://agfy.co/?s={igg_gamename}>)*\n*[igg-games](<https://igg-games.com/?s={igg_gamename}>)*\n*[SteamUnlocked](<https://steamunlocked.net/?s={igg_gamename}>)*",
                                 color=0x00ff00)
        embedVar.set_image(url=link)
        await ctx.channel.send(embed=embedVar)

def parse_embed_json(json_file, command):
    embeds_json = loads(json_file)[command]['embeds']

    for embed_json in embeds_json:
        embed = discord.Embed().from_dict(embed_json)
        yield embed



@bot.command()
async def help(ctx, command="help"):
    if command[0] == "$":
        command = command[1:]

    print(command)
    command = command.lower()
    if command not in command_list:
        command = "command_not_found"
        with open("EmbedsCommands.json", "r", encoding="utf-8") as file:
            temp_ban_embeds = parse_embed_json(file.read(), command)

        for embed in temp_ban_embeds:
            await ctx.send(embed=embed)
    else:
        command = command + "_command"
        with open("EmbedsCommands.json", "r", encoding="utf-8") as file:
            temp_ban_embeds = parse_embed_json(file.read(), command)

        for embed in temp_ban_embeds:
            await ctx.send(embed=embed)

@bot.command()
@commands.has_role("Administrator")
async def movie(ctx, *args):
    """
    Announces next movie! (GABE ONLY)
    input 1: movie name (pulp fiction):
    input 2: time in GMT(6):
    MUST SPLIT BY COMMA (,)
    EXAMPLE OF USAGE: $movie pulp fiction,6
    (will sent announcement of the movie "pulp fiction" at "6" pm)
    WARNING: WILL @EVERYONE!
    """
    #print(args)
    lol = ' '.join(args)
    #print(lol)
    ok = lol.split(',')
    #print(ok)

    message = f"""
    {ctx.message.guild}
𝗪𝗲 𝗮𝗿𝗲 𝗴𝗼𝗶𝗻𝗴 𝘁𝗼 𝘄𝗮𝘁𝗰𝗵 *{ok[0]}* 𝗶𝗻 𝗧𝗵𝗲 𝗟𝗼𝘂𝗻𝗴𝗲 𝘃𝗰.
𝗙𝗶𝗹𝗺 𝘀𝘁𝗮𝗿𝘁𝘀 𝗮𝘁 {ok[1]} 𝗣𝗺 𝗚𝗠𝗧 𝘁𝗼𝗻𝗶𝗴𝗵𝘁.
𝗬𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝘁𝗼 𝘂𝘀𝗲 𝗺𝗶𝗰 𝗼𝗿 𝗰𝗮𝗺𝗲𝗿𝗮.
<:peepohappy:887657009917362246> 𝗠𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗰𝗼𝗺𝗳𝘆 𝗮𝗻𝗱 𝗰𝗼𝘇𝘆 <:peepohappy:887657009917362246>                           https://discord.gg/AftSEwd4Ys
    """
    channel = bot.get_channel(887630579389059087)
    await channel.send(message)



@bot.command()
async def send(ctx, *args):
    """
    Sends a message and removes your own for privacy.
    :param args:
    :return:
    """
    await ctx.message.delete()
    time.sleep(0.1)
    await ctx.channel.send(' '.join(args))

@bot.command()
@commands.has_role("Administrator")
async def clear(ctx,amount=1):
    """
    Removes/purges messages. Default = 1
    :param ctx:
    :param amount:
    :return:
    """
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f"Succesfully removed {amount} messages", delete_after=2.0)

@bot.command()
async def code(ctx):
    """
    Gives you a link to the code of this bot!
    """
    await ctx.send(f"""*{link_to_code}*""")


# @bot.command()
# async def rules(ctx):
#     global amountofwords
#     await ctx.send(gamerules)


@bot.command()
async def cuddle(ctx, name=None):

    """
    Also gives you a hug, but better!
    :param name:
    """

    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": "hug",
        "api_key": giphy_api_key,
        "limit": "30"
    })

    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    gaylist = []
    # #print(data)
    for i in data['data']:
        link = i['images']['original']['url']
        gaylist.append(link)

    link = random.choice(gaylist)
    sender = str(ctx.author.mention)

    if name is None:
        embedVar = discord.Embed(title=f"**Sending a nice warm hug! :people_hugging:**", description=f"I hope your day is a little better now.", color=0x00ff00)
        embedVar.set_image(url=link)
        await ctx.channel.send(embed=embedVar)

    else:
        hug_quotes = ["A hug will make your day better! :grin:",
                      "A hug per day will keep anxiety away! <:peepohappy:887657009917362246>",
                      "A hug per day will keep all problems away! <:peepohappy:887657009917362246>",
                      "Hugs are the morphine for mental pain. :relieved:",
                      "This hug will better make your day amazing! :rage: :knife:"
                      ]

        try:
            name2 = await commands.MemberConverter().convert(ctx, name)
            name3 = name2.display_name
            sender_2 = await commands.MemberConverter().convert(ctx, sender)
            sender_3 = sender_2.display_name
            embedVar = discord.Embed(title=f"**{sender_3} would like to hug {name3}**", description=f"{random.choice(hug_quotes)}", color=0x00ff00)
            embedVar.set_image(url=link)
            await ctx.channel.send(embed=embedVar)

        except Exception as e:
            sender_2 = await commands.MemberConverter().convert(ctx, sender)
            sender_3 = sender_2.display_name
            embedVar = discord.Embed(title=f"**{sender_3} would like to hug {name}**", description=f"{random.choice(hug_quotes)}", color=0x00ff00)
            embedVar.set_image(url=link)
            await ctx.channel.send(embed=embedVar)

@bot.command()
async def pog(ctx):
    """
    Pickle Obviously Gay
    """
    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": "gay",
        "api_key": giphy_api_key,
        "limit": "30"
    })

    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    gaylist = []
    # #print(data)
    for i in data['data']:
        link = i['images']['original']['url']
        gaylist.append(link)

    link = random.choice(gaylist)
    user = bot.get_user(761640603930722357)
    embedVar = discord.Embed(title="**PICKLE IS STILL GAY! :rainbow_flag:**", description=f"In case you were wondering, {user.mention} is in fact still gay.", color=0x00ff00)
    #embedVar.add_field(name="Gif of Pickle and all her gayness", value=link, inline=False)
    embedVar.set_image(url=link)
    await ctx.channel.send(embed=embedVar)

@bot.command()
async def gif(ctx, *args):
    """
    Shows a gif
    """
    url = "http://api.giphy.com/v1/gifs/search"
    args = ' '.join(args)
    params = parse.urlencode({
        "q": args,
        "api_key": giphy_api_key,
        "limit": "30"
    })

    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    giflist = []
    # #print(data)
    for i in data['data']:
        link = i['images']['original']['url']
        giflist.append(link)

    link = random.choice(giflist)
    user = bot.get_user(761640603930722357)
    embedVar = discord.Embed(title=f"{args}", color=0x00ff00)
    #embedVar.add_field(name="Gif of Pickle and all her gayness", value=link, inline=False)
    embedVar.set_image(url=link)
    await ctx.channel.send(embed=embedVar)


@bot.command()
async def gay(ctx, name):

    """
    You can now call someone gay with *some spice*
    :param name:
    :return:
    """


    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": "gay",
        "api_key": giphy_api_key,
        "limit": "30"
    })

    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    gaylist = []
    # #print(data)
    for i in data['data']:
        link = i['images']['original']['url']
        gaylist.append(link)

    link = random.choice(gaylist)

    try:
        name2 = await commands.MemberConverter().convert(ctx, name)
        name3 = name2.display_name
        embedVar = discord.Embed(title=f"**{name3} IS GAY AS FUCK! :rainbow_flag:**", description=f"Have you seen {name}? This is gif is of them!", color=0x00ff00)
        #embedVar.add_field(name="Gif of Pickle and all her gayness", value=link, inline=False)
        embedVar.set_image(url=link)
        await ctx.channel.send(embed=embedVar)
    except Exception as e:
        embedVar = discord.Embed(title=f"**{name} IS GAY AS FUCK! :rainbow_flag:**", description=f"Have you seen {name}? This is gif is of them!", color=0x00ff00)
        #embedVar.add_field(name="Gif of Pickle and all her gayness", value=link, inline=False)
        embedVar.set_image(url=link)
        await ctx.channel.send(embed=embedVar)


@bot.command()
async def insult(ctx, name):

    """
    Insults the goddamn person obviously.
    :param name:
    :return:
    """

    insults = ["{} is a gay sprinkle on a gay rainbow.",
               "If I gave a penny for {} thoughts, I'd get change.",
               "Hey {}. There is no joke, kill yourself.",
               "I heard {}'s mum fell over, I hope the damage to the city can be fixed.",
               "I am going to build a time-machine, grab a dinasour egg and put it in {}'s living room so one day it will kill you.",
               "Not even the most loyal dog could love {}.",
               "I ran out of jokes, but I can get more just looking at {}'s life.",
               "*{} is gay*",
               "Hey {}, Does your ass ever get jealous of the shit that comes out of your mouth?",
               "I would agree with {} but then we would both be wrong.",
               "Stop being mean! {} is not useless. They can be used as a bad example.",
               "There's a tree creating the oxygen {} is wasting. They should go find it in the woods and apologize",
               "I'd try to insult {}, but I can't top what nature has already done to you.",
               "{} is the human equivalent of a participation award",
               "Slavers would pay to get rid of {}",
               "If {} went for a swim in the sea, you'd be polluting.\nThen again that would be washing and they sure don't smell like they wash.",
               "Not even cannibals would want to eat {}."]
    random_insult = random.choice(insults)
    #print(name)
    if random_insult == "*{} is gay*":
        if str(name).lower() in ["pickle", "<@761640603930722357>", "zoe"]:
            random_insult = "*{} is (actually) **GAY*** :rainbow_flag: "

    if random_insult == "{} is a gay sprinkle on a gay rainbow.":
        if str(name).lower() in ["pickle", "<@761640603930722357>", "zoe"]:
            random_insult = "{} is a **gay** :rainbow_flag: sprinkle on a **gay** :rainbow_flag: rainbow."

    await ctx.send(random_insult.format(name))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        insults = ["Are you mad fam? You that dumb yeh? That command doesn't exist, prick!",
                   "That command doesn't exist you dumb twat!",
                   "Your mom wished that you didn't exist, just like this command you fucking idiot!",
                   "Try again wanker! Command doesn't exist!",
                   "Did you make a typo or are you just retarded? That command doesn't exist.",
                   "The command you just typed is non-existent, just like your friends."]
        await ctx.send(random.choice(insults))
    else:
        message = "\n>>> **FOR FUCK SAKE!!!**\nAn error occured: ||`{}`||".format(str(error))
        await ctx.send(message)



@movie.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('''You are not allowed to use this command, you fucking idiot!''')



bot.run('My Special Token :)') #SaadBot
