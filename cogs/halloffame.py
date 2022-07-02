from email import message
from itertools import chain
import discord
from discord.ext import commands
import asyncio

from numpy import amax

class halloffame(commands.Cog):
    def __init__(self, client):
        self.client = client

    

            
    #if any messages has 10 reactions of ♥️ echo message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = payload.message_id
        channel = payload.channel_id
        guild = payload.guild_id
        tosend = 991740480398311544
        content = await self.client.get_channel(channel).fetch_message(message)
        for reaction in content.reactions:
            if reaction.emoji == "♥️":
                if reaction.count == 10:
                    await self.client.get_channel(tosend).send(f"{content.attachments[0]}")
                    madeby = content.author.name
                    await self.client.get_channel(tosend).send(f"Made by: {madeby}")
                    break

                    
            
            

def setup(client):
    client.add_cog(halloffame(client))