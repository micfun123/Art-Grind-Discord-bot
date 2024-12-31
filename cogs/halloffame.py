import discord
from discord.ext import commands
import asyncio
import time
import json

# Load existing posts data
with open("posts.json", "r") as readfile:
    posts_data = json.load(readfile)

# Load or initialize user frequency data
try:
    with open("user_frequencies.json", "r") as readfile:
        user_frequencies = json.load(readfile)
        if not isinstance(user_frequencies, dict):
            user_frequencies = {}
except FileNotFoundError:
    user_frequencies = {}


class HallOfFame(commands.Cog):
    def __init__(self, client):
        self.client = client

    # If any message has 10 reactions of ❤️, echo the message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        channel_id = payload.channel_id
        tosend = 1086347720463220786

        content = await self.client.get_channel(channel_id).fetch_message(message_id)
        for reaction in content.reactions:
            if reaction.emoji == "❤️":
                if reaction.count == 10:
                    if message_id in posts_data:
                        return
                    else:
                        madeby = content.author.name
                        madebyid = content.author.id
                        if channel_id == 1086410514348904529:
                            await self.client.get_channel(tosend).send(
                                f"|| {content.attachments[0]} ||"
                            )
                            await self.client.get_channel(tosend).send(
                                f"Made by: {madeby} **warning this image has gore**"
                            )
                        else:
                            await self.client.get_channel(tosend).send(
                                f"{content.attachments[0]}"
                            )
                            await self.client.get_channel(tosend).send(
                                f"Made by: {madeby}"
                            )

                        posts_data.append(message_id)
                        with open("posts.json", "w") as wfile:
                            json.dump(posts_data, wfile)

                        # Update user frequency data
                        if madeby in user_frequencies:
                            user_frequencies[madebyid] += 1
                        else:
                            user_frequencies[madebyid] = 1

                        with open("user_frequencies.json", "w") as wfile:
                            json.dump(user_frequencies, wfile)

                        # Message the image author
                        await content.author.send(
                            "Your image has been added to the hall of fame, it is the crème de la crème of art. It's the art we heart"
                        )
                    break

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def check_heart_all(self, ctx):
        await ctx.send("Checking all messages for 10 ❤️")
        tosend = 1086347720463220786

        for channel in ctx.guild.text_channels:
            try:
                print(f"trying channel {channel.name}")
                async for message in channel.history(limit=50555):
                    for reaction in message.reactions:
                        if reaction.emoji == "❤️" and reaction.count >= 10:
                            if message.id in posts_data:
                                continue
                            else:
                                madeby = message.author.name
                                madebyid = message.author.id
                                if channel.id == 1086410514348904529:
                                    await self.client.get_channel(tosend).send(
                                        f"|| {message.attachments[0]} ||"
                                    )
                                    await self.client.get_channel(tosend).send(
                                        f"Made by: {madeby} **warning this image has gore**"
                                    )
                                else:
                                    await self.client.get_channel(tosend).send(
                                        f"{message.attachments[0]}"
                                    )
                                    await self.client.get_channel(tosend).send(
                                        f"Made by: {madeby}"
                                    )

                                posts_data.append(message.id)
                                with open("posts.json", "w") as wfile:
                                    json.dump(posts_data, wfile)

                                # Update user frequency data
                                if madeby in user_frequencies:
                                    user_frequencies[madebyid] += 1
                                else:
                                    user_frequencies[madebyid] = 1

                                with open("user_frequencies.json", "w") as wfile:
                                    json.dump(user_frequencies, wfile)

                                await message.author.send(
                                    "Your image has been added to the hall of fame, it is the crème de la crème of art. It's the art we heart"
                                )
                                break
            except Exception as e:
                print(f"Error processing channel {channel.name}: {e}")
        await ctx.send("Done")

    @commands.command()
    @commands.is_owner()
    async def adder(self, ctx):
        target_channel_id = 1086330350592086187  # Channel ID to check
        target_emoji = "❤️"  # Heart emoji
        target_count = 9

        guild = ctx.guild
        for channel in guild.text_channels:
            if channel.id == target_channel_id:
                async for message in channel.history(limit=50000):
                    for reaction in message.reactions:
                        if (
                            reaction.emoji == target_emoji
                            and reaction.count == target_count
                        ):
                            await message.add_reaction("❤️")
                            time.sleep(2)
                            break
                        
        print("Done")


    @commands.command()
    @commands.is_owner()
    async def force_add(self, ctx, message_id: int):
        tosend = 1086347720463220786

        content = await self.client.get_channel(1086330350592086187).fetch_message(message_id)
        madeby = content.author.name
        madebyid = content.author.id
        if content.id in posts_data:
            return
        else:
            if content.channel.id == 1086410514348904529:
                await self.client.get_channel(tosend).send(
                    f"|| {content.attachments[0]} ||"
                )
                await self.client.get_channel(tosend).send(
                    f"Made by: {madeby} **warning this image has gore**"
                )
            else:
                await self.client.get_channel(tosend).send(
                    f"{content.attachments[0]}"
                )
                await self.client.get_channel(tosend).send(
                    f"Made by: {madeby}"
                )

            posts_data.append(content.id)
            with open("posts.json", "w") as wfile:
                json.dump(posts_data, wfile)

            # Update user frequency data
            if madeby in user_frequencies:
                user_frequencies[madebyid] += 1
            else:
                user_frequencies[madebyid] = 1

            with open("user_frequencies.json", "w") as wfile:
                json.dump(user_frequencies, wfile)

            await content.author.send(
                "Your image has been added to the hall of fame, it is the crème de la crème of art. It's the art we heart"
            )

def setup(client):
    client.add_cog(HallOfFame(client))
