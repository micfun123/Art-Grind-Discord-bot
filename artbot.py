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
from pretty_help import DefaultMenu, PrettyHelp
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement

load_dotenv()

Themes = ['When Pigs Fly', 
    'Tutle lord',
    'magic ball answers Signs point to yes.',
    'magicball affirms Yes definitely.',
    'magicball affirms Yes.',
    '8 ball magic said Most likely.',
    'magic ball answers Very doubtful.',
    'magic 8 ball answers Without a doubt.',
    'mystic eight ball said Most likely.',
    "magic ball answers Don't count on it.",
    'Magic ball says 100% No',
    'Magic ball does not know have you tryed google?',
    "Its not looking so good"]


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


@client.command(help = "Gives you the ping of the bot",guild_ids=["898557704858136617"])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ping time')


@client.slash_command(guild_ids=["898557704858136617"])
async def hello(ctx):
    await ctx.respond("Hello!")

@client.slash_command(guild_ids=["898557704858136617"])
async def duelIdea(ctx):
    em = discord.Embed(title="Duel Idea", description="Here is a duel idea for you to try out!", color=0x00ff00)
    em.add_field(name="Theme : ", value=random.choice(Themes))
    await ctx.respond()

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

