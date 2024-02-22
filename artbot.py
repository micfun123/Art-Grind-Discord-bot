import discord
import random
import os
from os import listdir
from os.path import isfile, join
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont , ImageEnhance,ImageColor
from io import BytesIO
from datetime import datetime,time
import textwrap
import urllib
import asyncio
import json
import io
from time import sleep
import sqlite3

load_dotenv()

 



from discord.ext import commands, tasks

def generate_i_made(url):
    hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req) 
    f = BytesIO(response.read())
    
    im1 = Image.open("images/IMG_4397.png")
    im1 = im1.convert("RGBA")
    im2 = Image.open(f)
    im2 = im2.convert("RGBA")
    im2 = im2.resize((400, 360))
    

    img = im1.copy()
    img = img.convert("RGBA")
    #img.alpha_composite(im2 (1300, 450))
    img.paste(im2.rotate(30 , resample=Image.BILINEAR, expand = 1, fillcolor = (255,255,255,0)), (1300, 450))
    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.guilds=True

client = commands.Bot(command_prefix= "+", intents=intents, presences = True, members = True, guilds=True, case_insensitive=True,allowed_mentions = discord.AllowedMentions(everyone=True))

def warningrole(ctx):
    #fetch server from id
    server = client.get_guild(856677753108693002)
    role = discord.utils.get(server.guild.roles, name="taskfailedwarning")
    return role


@client.event
async def on_ready():
    # Setting `Playing ` status
    print("we have powered on, I an alive.")
    await client.change_presence(activity=discord.Game(f"with some paint and a brush"))
    weekly_challenge.start()
    infochannel = await client.fetch_channel(1086330333185708123)
    await infochannel.send("I am back online. Seems like I was down for a while. Sorry for the inconvenience")
    await infochannel.send(f'Feel free to donate to me at <https://www.buymeacoffee.com/Michaelrbparker>')



@client.command(help = "Gives you the ping of the bot")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ping time')

def i_wrote(text):
    im = Image.open("images/IMG_4398.png")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Roboto-Black.ttf", 30)

    margin = 900
    offset = 350
    for line in textwrap.wrap(text, width=10):
            draw.text((margin, offset), line, font=font, fill=(0, 0, 0))
            offset += font.getsize(line)[1]

    d = BytesIO()
    d.seek(0)
    im.save(d, "PNG")
    d.seek(0)
    return d

@client.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")


@client.command(help = "Gives you the ping of the bot")
async def status(ctx,*, status):
    if ctx.author.id == int(481377376475938826):
        await client.change_presence(activity=discord.Game(f"{status}"))
    else: 
        await ctx.send("Only Lord Mic can do this")


@client.command()
async def pingtest(ctx):
    await asyncio.sleep(int(5))
    await ctx.send(f'<@&856677753125208081>')

@tasks.loop(time=time(12,00))
async def weekly_challenge():
    '''runs every day at 1PM UTC'''
    # check if the day is monday
    today = datetime.utcnow().isoweekday()
    if today == 5:  # Monday == 7
        message_channel = await client.fetch_channel(1086336641817378968)
        channeltosend = await client.fetch_channel(1086336788446056609)
        messages = await message_channel.history(limit=None).flatten()
        message = random.choice(messages)
        em = discord.Embed(title="Weekly Challenge", description=f"{message.content}", color=0x00ff00)
        await channeltosend.send(embed=em)
        await channeltosend.send(f'<@&856677753125208081>')
        await message.delete()


@client.command()
async def spam(ctx):
    user = await client.fetch_user("947008468294967357")
    channel = client.get_channel(999395345870094457)
    for i in range(0,50):
        await user.send(f"{user}")
        await user.send("Spamming")
        await channel.send(f"<@!947008468294967357>")
        print("test")
        sleep(1)

        

@client.command()
async def test(ctx):
    message_channel = await client.fetch_channel(1086336641817378968)
    channeltosend = await client.fetch_channel(1086336788446056609)
    messages = await message_channel.history(limit=None).flatten()
    message = random.choice(messages)
    em = discord.Embed(title="Weekly Challenge", description=f"{message.content}", color=0x00ff00)
    await channeltosend.send(embed=em)
    await message.delete()


@client.slash_command()
async def code(ctx):
    em = discord.Embed(title="You want my code", description="I dont give my code to any one you know", color=0x00ff00)
    em.add_field(name="Link :", value="https://github.com/micfun123/Art-Grind-Discord-bot")
    await ctx.respond(embed=em)
    
@client.slash_command(guild_ids=[856677753108693002],description="Suggest a theme for the weekly challenge")
async def suggest_theme(ctx,theme):
    em = discord.Embed(title="Suggestion", description=f"{theme}\n Suggested by: {ctx.author.name}", color=0x00ff00)
    await ctx.respond("sent")
    channelsend = client.get_channel(1086727673499373599)
    await channelsend.send(embed=em)


@client.slash_command()
async def duelidea(ctx):
    channel = client.get_channel(1086336562452779111)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)
    em = discord.Embed(title="Duel Idea", description="Here is a duel idea for you to try out!", color=0x00ff00)
    em.add_field(name="Theme : ", value=random.choice(allmes).content)
    await ctx.respond(embed=em)

@client.slash_command()
async def look_what_i_wrote(ctx,*,text):
    t = i_wrote(text)
    await ctx.respond(file=discord.File(t, "meme.png"))


@client.slash_command(guild_ids=[856677753108693002],description="test,test")
async def look_what_i_drew(ctx,*,url):
    t = generate_i_made(url)
    await ctx.respond(file=discord.File(t, "meme.png"))
    
#suggest commands
@client.command(help="Suggest a command")
async def suggest(ctx,*,suggestion):
    channel = client.get_channel(967784275216846968)
    em = discord.Embed(title="Suggestion", description=f"{suggestion}", color=0x00ff00)
    em.set_footer(text=f"Suggested by {ctx.author}")
    await channel.send(embed=em)


#make server invite link
@client.slash_command(description="Make an invite link for the server")
async def invite(ctx):
    await ctx.respond(f"{ctx.author.mention} here is your invite link: {await client.invite(ctx.guild)}")

@client.command(help="Dump")
async def dump(ctx):
    
    channel = client.get_channel(1086336562452779111)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    t= 0
    for i in allmes:
        t = t + 1
        await ctx.send(i.content)

    await ctx.send(f"{t}")
    
    
@client.command(help="Dump")
async def dumpremoveduplicate(ctx):
    
    channel = client.get_channel(1086336562452779111)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    t= 0
    for i in allmes:
        t = t + 1
        await ctx.send(i.content)

    await ctx.send(f"{t}")

    
#add 1 point to score board 
@client.command(help="Add 1 point to the score board")
@commands.has_permissions(administrator=True)
async def addpoint(ctx,*,user):
    with open('score.json', 'r') as f:
        data = json.load(f)
    if user in data:
        data[user] += 1
    else:
        data[user] = 1
    with open('score.json', 'w') as f:
        json.dump(data, f)
    await ctx.send(f"{user} has {data[user]} points")

#removes 1 point to score board
@client.command(help="Remove 1 point to the score board")
@commands.has_permissions(administrator=True)
async def removepoint(ctx,*,user):
    with open('score.json', 'r') as f:
        data = json.load(f)
    if user in data:
        data[user] -= 1
    else:
        data[user] = 0
    with open('score.json', 'w') as f:
        json.dump(data, f)
    await ctx.send(f"{user} has {data[user]} points")   

#top 10 score board
@client.command()
async def leaderboardscore(ctx):
    with open('score.json', 'r') as f:
        data = json.load(f)
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        em = discord.Embed(title="All Scores", description="Top 10 score board", color=0x00ff00)
        for i in sorted_data[:10]:
            id = i[0]
            id = id.replace("<@", "")
            id = id.replace(">", "")
            print(id)
            try: 
                user = await ctx.guild.fetch_member(id)
                name = user.name
                em.add_field(name=f"{name}", value=i[1])

            except:
                em.add_field(name=f"{i[0]}", value=i[1])


        await ctx.send(embed=em)

@client.command(name="showstyleprompts",help = "Shows all style prompts")
async def ShowStylePrompts_command(self, ctx):
    em = discord.Embed(title="Style Prompts", description=f"All current Styles DM tea for more to be added", color=0x20BEFF)
    lines = open('databases/StylePrompt.txt').read().splitlines()
    for i in range(len(lines)):
        em.add_field(name=f"{i+1}", value=f"{lines[i]}")
       
    await ctx.send(embed=em)
@client.slash_command(name="showstyleprompts")
async def showstyleprompts_slash(self, ctx):
    em = discord.Embed(title="Style Prompts", description=f"All current Styles DM tea for more to be added", color=0x20BEFF)
    lines = open('databases/StylePrompt.txt').read().splitlines()
    for i in range(len(lines)):
        em.add_field(name=f"{i+1}", value=f"{lines[i]}")
       
    await ctx.respond(embed=em)

@client.slash_command()
async def randomcolour(ctx):
    HEX_random = discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    em = discord.Embed(title="Random Colour", description=f"{ctx.author.mention} here is your random colour: {HEX_random}", color=HEX_random)
    
    await ctx.respond(embed=em)

#full score board
@client.command()
async def fullscore(ctx):
    with open('score.json', 'r') as f:
        data = json.load(f)
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        em = discord.Embed(title="Full leader board", description="If you want to see the top ten then do ```+leaderboardscore```", color=0x00ff00)
        for i in sorted_data:
            id = i[0]
            id = id.replace("<@", "")
            id = id.replace(">", "")
            print(id)
            try: 
                user = await ctx.guild.fetch_member(id)
                name = user.name
                em.add_field(name=f"{name}", value=i[1] ,inline=False)

            except:
                em.add_field(name=f"{i[0]}", value=i[1] ,inline=False)
    await ctx.send(embed=em)


#birthday mode. When its a birthday use
@client.command(help="Birthday mode")
async def birthday(ctx,*,user):
    ctx.message.delete()
    channel = ctx.channel
    em = discord.Embed(title="Happy Birthday! 🎉🍰🎂🥳", description=f"Dear <{user}> \n Hope you have a Great Birthday \n from the Art Grind Staff ", color=0x00ff00)
    await channel.send(embed=em)

   #style prompt command
@client.command(name="styleprompt",help = "Prompts you a Style to draw")
async def StylePrompt_command(ctx):
        lines = open('StylePrompt.txt').read().splitlines()
        myline =random.choice(lines)
        em = discord.Embed(title="Style Prompt. Have fun making", description=f"{myline}", color=0x20BEFF)
        await ctx.send(embed=em)

@client.slash_command(name="styleprompt")
async def styleprompt_slash(ctx):
        lines = open('StylePrompt.txt').read().splitlines()
        myline =random.choice(lines)
        em = discord.Embed(title="Style Prompt. Have fun making", description=f"{myline}", color=0x20BEFF)
        await ctx.respond(embed=em)
   

@client.command(name="dump_proton",help = "Shows all style prompts")
async def dump_proton_commands(ctx):
    lines = open('duel.txt').read().splitlines()
    for i in lines:
        await ctx.send(i)


TOKEN = os.getenv("DISCORD_TOKEN")

def start_bot(client):
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace('.py', '') for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)  # Startup all cogs
            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
        client.run(TOKEN) # Token do not change it here. Change it in the .env if you do not have a .env make a file and put DISCORD_TOKEN=Token 

    except Exception as e:
        print(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")



start_bot(client)

