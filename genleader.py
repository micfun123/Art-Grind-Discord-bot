import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable the message content intent
intents.guilds = True  # Enable guilds intent to fetch guild information
intents.guild_messages = True  # Enable guild messages intent to fetch messages in the guild
intents.members = True  # Enable members intent to fetch member information

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def fetch_usernames(user_ids):
    user_info = {}
    for user_id in user_ids:
        try:
            user = await bot.fetch_user(user_id)
            user_info[user_id] = user.name
        except discord.NotFound:
            user_info[user_id] = "Unknown User"
        except discord.HTTPException as e:
            print(f'An HTTP error occurred: {e}')
            user_info[user_id] = "Unknown User"
    return user_info

@bot.command()
async def generate_leaderboard(ctx):
    print("starting")
    try:
        with open('userscommon.json', 'r') as f:
            user_data = json.load(f)
    except Exception as e:
        await ctx.send(f'Error reading input file: {e}')
        return

    user_ids = user_data.keys()
    user_info = await fetch_usernames(user_ids)

    sorted_user_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title="User Activity Leaderboard", color=discord.Color.blue())

    for i, (user_id, freq) in enumerate(sorted_user_data):
        username = user_info[user_id]
        print(f"{i+1}. {username} Frequency: {freq}")
        await ctx.send(f"{i+1}. {username} Frequency: {freq}")

# Replace 'your_token_here' with your bot's token
bot.run('')
