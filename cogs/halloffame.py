from email import message
from itertools import chain
import discord
from discord.ext import commands
import asyncio
import json

from numpy import amax

with open ("posts.json", "r") as readfile:
   data = json.load(readfile)

class halloffame(commands.Cog):
    def __init__(self, client):
        self.client = client

    

            
    #if any messages has 10 reactions of ♥️ echo message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = payload.message_id
        channel = payload.channel_id
        guild = payload.guild_id
        tosend = 1086347720463220786
        content = await self.client.get_channel(channel).fetch_message(message)
        for reaction in content.reactions:
            if reaction.emoji == "❤️":
                if reaction.count == 10:
                    if message in data:
                        pass
                    else:
                        if channel == 1086410514348904529:
                            await self.client.get_channel(tosend).send(f"|| {content.attachments[0]} ||")
                            madeby = content.author.name
                            await self.client.get_channel(tosend).send(f"Made by: {madeby} **warning this image is has gore**")
                            data.append(message)
                            with open ("posts.json", "w") as wfile:
                                json.dump(data, wfile)
                        else:
                            await self.client.get_channel(tosend).send(f"{content.attachments[0]}")
                            madeby = content.author.name
                            await self.client.get_channel(tosend).send(f"Made by: {madeby}")
                            data.append(message)
                            with open ("posts.json", "w") as wfile:
                                json.dump(data, wfile)
                    
                    break

    @commands.command()
    @commands.is_owner()
    async def check_heart_all(self, ctx):
        tosend = 1086347720463220786
        for channel in ctx.guild.text_channels:
            for message in channel.history(limit=300):
                for reaction in message.reactions:
                    if reaction.emoji == "❤️":
                        if reaction.count == 10:
                            if message.id in data:
                                pass
                            else:
                                if channel.id == 1086347720463220786:
                                    await self.client.get_channel(tosend).send(f"|| {message.attachments[0]} ||")
                                    madeby = message.author.name
                                    await self.client.get_channel(tosend).send(f"Made by: {madeby} **warning this image is has gore**")
                                    data.append(message.id)
                                    with open ("posts.json", "w") as wfile:
                                        json.dump(data, wfile)
                                else:
                                    await self.client.get_channel(tosend).send(f"{message.attachments[0]}")
                                    madeby = message.author.name
                                    await self.client.get_channel(tosend).send(f"Made by: {madeby}")
                                    data.append(message.id)
                                    with open ("posts.json", "w") as wfile:
                                        json.dump(data, wfile)
                                break


                    
            
            

def setup(client):
    client.add_cog(halloffame(client))