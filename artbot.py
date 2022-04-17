import discord
import random
import aiohttp
import os
from os import listdir
from os.path import isfile, join
import json
import os
from dotenv import load_dotenv
from easy_pil import Editor, Canvas, Font, load_image, Text
import datetime


load_dotenv()

Themes = ['When Pigs Fly', 
    'Tutle lord',
    'A loxodon warlock who determinedly pushes through their fear of blood, spurred to adventure to escape their previous life.',
    'You can Run but you can not Hide',
    'Hide and seek but on the moon',
    'A cake in a hat on a box in a hat',
    'For Tea and country. did i say country i meant cake',
    'Guard whales',
    'A slice of the stars',
    'Screeming Clouds',
    'climb',
    'United star force',
    'The sun is shining',
    'The moon is shining',
    'Tree wars',
    'swords vs pens',
    'Frog in a Hat',
    'Assassin cat',
    'suited and booted']


from discord.ext import commands, tasks


intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.guilds=True

client = commands.Bot(command_prefix= "^", intents=intents, presences = True, members = True, guilds=True, case_insensitive=True)

@client.event
async def on_ready():
    # Setting `Playing ` status
    print("we have powered on, I an alive.")
    await client.change_presence(activity=discord.Game(f"I do art stuff in {len(client.guilds)} servers."))

testguild = 898557704858136617

@client.command(help = "Gives you the ping of the bot")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ping time')


@client.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")


@tasks.loop(time=datetime.time(12,00))
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
        chennel2 = 964936769277677578
        em = discord.Embed(title=f"weekly challenge",color=0x00ff00)
        em.description = "<@&856677753125208081>\n Its your favorite time of the week again!\n"
        em.add_field(name="Challenge :", value=randoms.content)
        msg = await channel.fetch_message(randoms.id)
        await msg.delete()
        await chennel2.send(embed=em)


@client.command()
async def testNOREMOVE(ctx):

    channel = client.get_channel(964936769277677578)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    randoms = randoms = random.choice(allmes)
    chennel2 = 964936769277677578
    em = discord.Embed(title=f"weekly challenge",color=0x00ff00)
    em.description = "<@&856677753125208081>\n Its your favorite time of the week again!\n"
    em.add_field(name="Challenge :", value=randoms.content)
    msg = await channel.fetch_message(randoms.id)
    await ctx.send(embed=em)

@client.command()
async def test(ctx):

    channel = client.get_channel(964936769277677578)

    allmes = []
    async for message in channel.history(limit=200):
        allmes.append(message)

    randoms = random.choice(allmes)
    chennel2 = 964936769277677578
    em = discord.Embed(title=f"weekly challenge",color=0x00ff00)
    em.description = "<@&856677753125208081>\n Its your favorite time of the week again!\n"
    em.add_field(name="Challenge :", value=randoms.content)
    msg = await channel.fetch_message(randoms.id)
    await msg.delete()
    await ctx.send(embed=em)

    

@client.slash_command()
async def duelidea(ctx):
    em = discord.Embed(title="Duel Idea", description="Here is a duel idea for you to try out!", color=0x00ff00)
    em.add_field(name="Theme : ", value=random.choice(Themes))
    await ctx.respond(embed=em)


    

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

