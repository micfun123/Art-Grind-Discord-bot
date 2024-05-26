import discord
from discord.ext import commands
import json
import asyncio

intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable the message content intent
intents.guilds = True  # Enable guilds intent to fetch guild information
intents.guild_messages = True  # Enable guild messages intent to fetch messages in the guild

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def get_user_ids(ctx):
    print("starting")
    guild = bot.get_guild(856677753108693002)
    if not guild:
        await ctx.send('Guild not found.')
        return

    try:
        with open('posts.json', 'r') as f:
            message_ids = json.load(f)
    except Exception as e:
        await ctx.send(f'Error reading input file: {e}')
        return

    user_id_frequency = {}
    count = 0
    channel = guild.get_channel(1086330350592086187)
    for message_id in message_ids:
        print(f"count {count} out of {len(message_ids)}")
        count = count + 1
        message_found = False
        try:
            message = await channel.fetch_message(message_id)
            user_id = message.author.id
            user_id_frequency[user_id] = user_id_frequency.get(user_id, 0) + 1
            print("Found")
        except Exception as e:
            print(e)
        message_found = True
           

    try:
        with open("userscommon.json", 'w') as f:
            json.dump(user_id_frequency, f, indent=4)
        await ctx.send(f'User ID frequencies saved to {"userscommon.json"}')
    except Exception as e:
        await ctx.send(f'Error writing output file: {e}')

# Replace 'your_token_here' with your bot's token
bot.run('')
