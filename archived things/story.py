import asyncio
from distutils.log import debug
from email import message
import discord
from discord.ext import commands
import json


class story(commands.Cog):
    def __init__(self, client, message_id=None, message_content=None):
        self.client = client
        self.message_id = message_id
        self.message_content = message_content

        try:
            with open("storydata.json", "r") as f:
                data = json.load(f)
                for i in data:
                    if i["message_id"]:
                        self.message_id = i["message_id"]
                    if i["message_content"]:
                        self.message_content = i["message_content"]
            print("Found storydata.json")
        except:
            print("No story data found")
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore ourselves
        if message.author.bot:
            return
        # Ignore all messages except in the story channel
        if message.channel.id != 936327671367995473:
            return

        if self.message_id == None:
            self.message_id = message.id
            self.message_content = message.content

            data = [{"message_id": message.id, "message_content": message.content}]
            with open("storydata.json", "w") as f:
                json.dump(data, f)

            role = message.channel.guild.default_role
            if role not in message.channel.overwrites:
                overwrites = {role: discord.PermissionOverwrite(send_messages=False)}
                await message.channel.edit(overwrites=overwrites)
            elif (
                message.channel.overwrites[role].send_messages == True
                or message.channel.overwrites[role].send_messages == None
            ):
                overwrites = message.channel.overwrites[role]
                overwrites.send_messages = False
                await message.channel.set_permissions(role, overwrite=overwrites)
            else:
                overwrites = message.channel.overwrites[role]
                overwrites.send_messages = True

            await message.channel.set_permissions(role, overwrite=overwrites)

            await message.add_reaction("\U0001F44D")
            await message.add_reaction("\U0001F44E")

        else:
            await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = payload.message_id
        channel = payload.channel_id
        content = await self.client.get_channel(channel).fetch_message(message)

        if channel != 936327671367995473:
            return

        upvotes = 0
        downvotes = 0

        if message == self.message_id:
            for reaction in content.reactions:
                if reaction.emoji == "\U0001F44D":
                    upvotes = reaction.count
                if reaction.emoji == "\U0001F44E":
                    downvotes = reaction.count

            if (
                upvotes + downvotes >= 5
            ):  # and ((downvotes / upvotes) < 0.4 or (upvotes / downvotes) < 0.4)):
                if upvotes - downvotes >= 2:
                    await content.channel.send(f"{self.message_content}")
                    self.message_id = None
                    self.message_content = None

                    role = content.channel.guild.default_role

                    if role not in content.channel.overwrites:
                        overwrites = {
                            role: discord.PermissionOverwrite(send_messages=True)
                        }
                        await content.channel.edit(overwrites=overwrites)
                    else:
                        overwrites = content.channel.overwrites[role]
                        overwrites.send_messages = True
                        await content.channel.set_permissions(
                            role, overwrite=overwrites
                        )

                    await content.delete()

                if downvotes - upvotes >= 2:
                    self.message_id = None
                    self.message_content = None

                    role = content.channel.guild.default_role
                    if role not in content.channel.overwrites:
                        overwrites = {
                            role: discord.PermissionOverwrite(send_messages=True)
                        }
                        await content.channel.edit(overwrites=overwrites)
                    else:
                        overwrites = content.channel.overwrites[role]
                        overwrites.send_messages = True
                        await content.channel.set_permissions(
                            role, overwrite=overwrites
                        )

                    await content.delete()


def setup(client):
    client.add_cog(story(client))
    print("story.py loaded")
