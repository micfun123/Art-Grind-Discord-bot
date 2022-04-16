from urllib.request import proxy_bypass
import discord
import datetime
import requests
from discord.ext import commands 
from discord.commands import slash_command
from dotenv import load_dotenv
import os
import json


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

   
        
def setup(client):
    client.add_cog(Mod(client))