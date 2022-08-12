
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

with open("warning.json", "r") as readfile:
    data = json.load(readfile)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="reloads cog, for mic only")
    async def reload(self,ctx,cog):
        self.client.reload_extension(f"cogs.{cog}")
        await ctx.send("reload")
    
    @commands.command()
    async def illegal(self,ctx):
        await ctx.send("Adding all users to the database")
        for i in ctx.guild.members:
            try:
                await ctx.send(f"{i} has been added to database as {i.id}")
                data.append({"ID" : i.id, "Warning amount" : 0})
                with open("warning.json", "w") as writefile:
                    json.dump(data, writefile)
            except Exception as e:
                print(e)
                await ctx.send(e)
        await ctx.send("Database set up")
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id not in data:
            data.append({"ID" : member.id, "Warning amount" : 0})
            with open("warning.json", "w") as writefile:
                json.dump(data, writefile)

    @commands.command()
    async def warn(self,ctx,member: discord.Member, *, reason):
        if member.id in data:
            data[data.index({"ID" : member.id})]["Warning amount"] += 1
            with open("warning.json", "w") as writefile:
                json.dump(data, writefile)
            await ctx.send(f"{member} has been warned for {reason}")
        else:
            await ctx.send("User not in database")

    @commands.command()
    async def warnlist(self,ctx):
        await ctx.send(data)

    @commands.command()
    async def warnring(self,ctx,member: discord.Member):
        if member.id in data:
           for i in range(data[data.index({"ID" : member.id})]["Warning amount"]):
               await ctx.send(f"{member} has been warned")  
    
    @commands.command()
    async def warnreset(self,ctx,member: discord.Member):
        if member.id in data:
            data[data.index({"ID" : member.id})]["Warning amount"] = 0
            with open("warning.json", "w") as writefile:
                json.dump(data, writefile)
            await ctx.send(f"{member} has been reset")
        else:
            await ctx.send("User not in database")



            


        
def setup(client):
    client.add_cog(Mod(client))