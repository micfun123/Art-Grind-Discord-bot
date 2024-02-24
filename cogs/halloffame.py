from email import message
from itertools import chain
import discord
from discord.ext import commands
import asyncio
import time
import json

from numpy import amax

with open("posts.json", "r") as readfile:
    data = json.load(readfile)


class halloffame(commands.Cog):
    def __init__(self, client):
        self.client = client

    # if any messages has 10 reactions of ♥️ echo message
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
                            await self.client.get_channel(tosend).send(
                                f"|| {content.attachments[0]} ||"
                            )
                            madeby = content.author.name
                            await self.client.get_channel(tosend).send(
                                f"Made by: {madeby} **warning this image is has gore**"
                            )
                            data.append(message)
                            with open("posts.json", "w") as wfile:
                                json.dump(data, wfile)
                            # message the image author
                            await content.author.send(
                                "Your image has been added to the hall of fame, it is the crème de la crème of art. Its the art we heart"
                            )
                        else:
                            await self.client.get_channel(tosend).send(
                                f"{content.attachments[0]}"
                            )
                            madeby = content.author.name
                            await self.client.get_channel(tosend).send(
                                f"Made by: {madeby}"
                            )
                            data.append(message)
                            with open("posts.json", "w") as wfile:
                                json.dump(data, wfile)

                            await content.author.send(
                                "Your image has been added to the hall of fame, it is the crème de la crème of art. Its the art we heart"
                            )

                    break

    @commands.command()
    @commands.is_owner()
    async def check_heart_all(self, ctx):
        await ctx.send("Checking all messages for 10 ♥️")
        tosend = 1086347720463220786
        for channel in ctx.guild.text_channels:
            try:
                print(f"trying channel {channel.name}")
                for message in await channel.history(limit=50000).flatten():
                    for reaction in message.reactions:
                        if reaction.emoji == "❤️":
                            if reaction.count >= 10:
                                if message.id in data:
                                    pass
                                else:
                                    if channel.id == 1086410514348904529:
                                        await self.client.get_channel(tosend).send(
                                            f"|| {message.attachments[0]} ||"
                                        )
                                        madeby = message.author.name
                                        await self.client.get_channel(tosend).send(
                                            f"Made by: {madeby} **warning this image is has gore**"
                                        )
                                        data.append(message.id)
                                        with open("posts.json", "w") as wfile:
                                            json.dump(data, wfile)

                                        # message the image author
                                        await message.author.send(
                                            "Your image has been added to the hall of fame, it is the crème de la crème of art. Its the art we heart"
                                        )
                                    else:
                                        await self.client.get_channel(tosend).send(
                                            f"{message.attachments[0]}"
                                        )
                                        madeby = message.author.name
                                        await self.client.get_channel(tosend).send(
                                            f"Made by: {madeby}"
                                        )
                                        data.append(message.id)
                                        with open("posts.json", "w") as wfile:
                                            json.dump(data, wfile)
                                        await message.author.send(
                                            "Your image has been added to the hall of fame, it is the crème de la crème of art. Its the art we heart"
                                        )
                                    break
            except:
                pass
        await ctx.send("Done")

    @commands.command()
    @commands.is_owner()
    async def adder(self, ctx):
        target_channel_id = 1086330350592086187  # Channel ID to check
        target_emoji = "❤️"  # Heart emoji

        target_channel = await ctx.guild.fetch_channel(target_channel_id)
        if target_channel:
            await ctx.send(f"Checking messages in {target_channel.name}")
            async for message in target_channel.history(limit=30000):
                for reaction in message.reactions:
                    if str(reaction.emoji) == target_emoji and reaction.count == 9:
                        try:
                            await message.add_reaction(target_emoji)
                            print(f"Added {target_emoji} to message ID: {message.id}")
                        except discord.HTTPException:
                            print("Failed to add reaction. Insufficient permissions.")
                        break  # Once a message is found with 9 ❤️, move to the next message
                time.sleep(2)
        else:
            await ctx.send("Target channel not found.")


def setup(client):
    client.add_cog(halloffame(client))
