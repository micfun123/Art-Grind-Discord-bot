
from imp import reload
from urllib.request import proxy_bypass
import discord
import datetime
import requests
from discord.ext import commands 
from discord.commands import slash_command
from dotenv import load_dotenv
import os
import json
import info

botman = info.mic

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="reloads cog, for mic only")
    @commands.check(botman)
    async def reload(self,ctx,cog):
        self.client.reload_extension(f"cogs.{cog}")
        await ctx.send("reload")
    
        
def setup(client):
    client.add_cog(Mod(client))