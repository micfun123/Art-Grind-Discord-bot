from pydoc import describe
from string import whitespace
from unicodedata import name
from xml.dom.expatbuilder import theDOMImplementation
import discord
import random
import os
from os import listdir
from os.path import isfile, join
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont , ImageEnhance
from io import BytesIO
from datetime import datetime,time
import textwrap
import urllib
import asyncio

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

client = commands.Bot(command_prefix= "^", intents=intents, presences = True, members = True, guilds=True, case_insensitive=True,allowed_mentions = discord.AllowedMentions(everyone=True))


@client.event
async def on_ready():
    # Setting `Playing ` status
    print("we have powered on, I an alive.")
    await client.change_presence(activity=discord.Game(f"I do art stuff in {len(client.guilds)} servers."))
    weekly_challenge.start()


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
    if today == 7:  # Monday == 7
        channel = client.get_channel(964936769277677578)
        allmes = []
        async for message in channel.history(limit=200):
            allmes.append(message)
        randoms = random.choice(allmes)
        chennel2 = client.get_channel(915305657803108362)
        em = discord.Embed(title=f"weekly challenge",color=0x00ff00)
        em.description = "Its your favorite time of the week again!\n"
        em.add_field(name="Challenge :", value=randoms.content)
        msg = await channel.fetch_message(randoms.id)
        print(msg.content)
        await chennel2.send(embed=em)
        await chennel2.send(f'<@&856677753125208081>')
        await msg.delete()

@client.command()
async def test(ctx):

    channel = client.get_channel(964936769277677578)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    randoms = random.choice(allmes)
    chennel2 = 964936769277677578
    em = discord.Embed(title=f"weekly challenge",color=0x00ff00)
    em.description = "Its your favorite time of the week again!\n"
    em.add_field(name="Challenge :", value=randoms.content)
    msg = await channel.fetch_message(randoms.id)
    await ctx.send(embed=em)
    await ctx.send(f'<@&856677753125208081>')

@client.slash_command()
async def code(ctx):
    em = discord.Embed(title="You want my code", description="I dont give my code to any one you know", color=0x00ff00)
    em.add_field(name="Link :", value="https://github.com/micfun123/Art-Grind-Discord-bot")
    await ctx.respond(embed=em)
    
@client.slash_command(guild_ids=[856677753108693002],description="Suggest a theme for the weekly challenge")
async def suggest_theme(ctx,theme):
    em = discord.Embed(title="Suggestion", description=f"{theme}", color=0x00ff00)
    await ctx.respond("sent")
    channelsend = client.get_channel(967784275216846968)
    await channelsend.send(embed=em)


@client.slash_command()
async def duelidea(ctx):
    channel = client.get_channel(975383857115332729)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)
    em = discord.Embed(title="Duel Idea", description="Here is a duel idea for you to try out!", color=0x00ff00)
    em.add_field(name="Theme : ", value=random.choice(allmes))
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
    
    channel = client.get_channel(975383857115332729)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    for i in allmes:
        await ctx.send(i.content)
    
    




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

