import discord
from discord.ext import commands, tasks
import asyncio
import json
import time
from datetime import datetime

class ChatRevive(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.revive_loop.start()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def set_revive_channel(self, ctx, channel: discord.TextChannel):
        with open("revive_channel.json", "r") as readfile:
            data = json.load(readfile)
        data["channel"] = channel.id
        with open("revive_channel.json", "w") as writefile:
            json.dump(data, writefile)
        await ctx.send(f"Revive channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def revive_amount(self, ctx, amount: int):
        with open("revive_channel.json", "r") as readfile:
            data = json.load(readfile)
        data["amount"] = amount
        with open("revive_channel.json", "w") as writefile:
            json.dump(data, writefile)
        await ctx.send(f"Revive amount set to {amount}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def revive_set(self, ctx, amount: int, channel: discord.TextChannel):
        with open("revive_channel.json", "r") as readfile:
            data = json.load(readfile)
        data["amount"] = amount
        data["channel"] = channel.id
        with open("revive_channel.json", "w") as writefile:
            json.dump(data, writefile)
        await ctx.send(f"Revive amount set to {amount} and channel set to {channel.mention}")

    #start a loop that checks ever 2h if there has been the revive_amount of messages in the revive_channel
    #if there has been, send a message in the revive_channel saying that the chat has been revived
    @tasks.loop(hours=2)
    async def revive_loop(self):
        print("revive loop started")
        with open("revive_channel.json", "r") as readfile:
            data = json.load(readfile)
        channel = await self.client.fetch_channel(data["channel"])
        amount = data["amount"]
        if channel is None:
            pass
        else:
            #see if the revive_amount of messages were send longer than 2h ago
            async for message in channel.history(limit=amount):
                #check so see if the oldest message is older than 2h
                uctmessage = message.created_at.replace(tzinfo=None)
                if (datetime.utcnow() - uctmessage).total_seconds() > 7200:
                    #if it is, send a message in the channel saying that the chat has been revived
                    await channel.send("Its been a bit quiet in here, so um <@&1135308788614823946>")
                print("revive loop ended")
                print((datetime.utcnow() - uctmessage).total_seconds())
        
    @revive_loop.before_loop
    async def before_revive_loop(self):
        await self.client.wait_until_ready()



    
    
            

def setup(client):
    client.add_cog(ChatRevive(client))