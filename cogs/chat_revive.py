import discord
from discord.ext import commands, tasks
import asyncio
import json
import random
import time
from datetime import datetime

chatprompts = [
    "I am a kind of coat that can only be put on when wet. What am I? \n ||A coat of paint||",
    "What is the best thing to do if a bull charges you? \n ||Pay him||",
    "Why did the vampire take art class? \n ||He wanted to learn how to draw blood||",
    "What do you call a gorilla that plays with clay? \n ||A Hairy Potter!||",
    "They put pictures on me \n then take pictures of me \n to share with the world \n \n But the pictures disappear \n as my end draws near \n and anxious heartbeats stilled \n \n I am sought after very wide \n especially after every night \n when things are put in motion \n \n And after a little while \n I will be able to defile \n your ability to sleep with devotion \n \n What am I? \n ||Cappuccino||",
    "What do you call a mom who can’t draw? \n ||Tracy||",
    "why couldn’t the man afford expensive art? \n || He had no Monet.||",
    "What do you call a painting of a cat? \n ||A paw-trait||",
    "What do you call a painting of a dog? \n ||A paw-trait||",
    "Why was the artist hauled to court? \n ||To face the mosaic.||",
    "Why did Van Gogh become a painter? \n ||Because he didn’t have an ear for music.||",
    "What is it called when someone mislabels a color? \n || A false ac-hue-sation.|| ",
    "When an artist meets his rival, what does he say? \n ||I am challenging you for a doodle.||"


        
]

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
            messages = await channel.history(limit=amount).flatten()
            oldest = messages[-1]
            uctmessage = oldest.created_at.replace(tzinfo=None)
            if (datetime.utcnow() - uctmessage).total_seconds() > 7200:
                #if it is, send a message in the channel saying that the chat has been revived
                ridder = random.choice(chatprompts)
                await channel.send(f"Its been a bit quiet in here, so um this is awkward... \n \n {ridder}")
            print("revive loop ended")
            print((datetime.utcnow() - uctmessage).total_seconds())
        
                
                


    @revive_loop.before_loop
    async def before_revive_loop(self):
        await self.client.wait_until_ready()



    
    
            

def setup(client):
    client.add_cog(ChatRevive(client))