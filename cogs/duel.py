import discord
from discord.ext import commands
import asyncio


class pyduel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="duel",
        description="Start a duel with another user. (duration_unit can be minutes or days)",
    )
    async def duel(self, ctx, topic: str, duration: int, duration_unit: str):
        x = discord.Embed(
            title=f"Duel topic {topic}",
            description=f"You have {duration} {duration_unit} to make something fitting the theme {topic}. When you have finished, post the final work in the thread created by the bot. After the time is up, the bot will automatically put them in judging.",
        )
        response = await ctx.respond(embed=x)
        message = await response.original_message()
        thread = await message.create_thread(name=f"Duel: {topic}")

        # Calculate sleep duration
        sleep_duration = (
            duration * 60 if duration_unit.lower() == "minutes" else duration * 60 * 24
        )
        await asyncio.sleep(sleep_duration)

        # Process thread messages and collect submissions
        submissions = []
        async for msg in thread.history(limit=None):
            if msg.attachments:
                submission = {"url": msg.attachments[0].url, "author": msg.author}
                submissions.append(submission)

        # Send poll message
        tosend = 1101590208698384454
        channelsend = await self.client.fetch_channel(tosend)

        poll_embed = discord.Embed(
            title=f"Duel Poll for {topic}",
            description="React to vote for your favorite submission.",
        )
        # Add reactions for each submission
        reaction_emojis = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

        for i, submission in enumerate(submissions):
            if i >= len(reaction_emojis):
                break
            await poll_message.add_reaction(reaction_emojis[i])
            await channelsend.send(
                f"{reaction_emojis[i]}: {submission['url']} (Made by: {submission['author'].mention})"
            )
        poll_message = await channelsend.send(embed=poll_embed)
        # ping judge role 958172090509443083
        await channelsend.send("<@&958172090509443083>")

        # poll auto closes in 2 days
        poll_duration = 172800
        await asyncio.sleep(poll_duration)

        # Count reactions and determine the winner
        poll_message = await channelsend.fetch_message(poll_message.id)
        votes = {reaction.emoji: reaction.count for reaction in poll_message.reactions}

        winner_emoji = max(votes, key=votes.get)
        winner_index = reaction_emojis.index(winner_emoji)
        winner_submission = submissions[winner_index]

        # Announce the winner
        winner_embed = discord.Embed(
            title="Duel Winner Announcement",
            description=f"The winner of the duel is {winner_submission['author'].mention}",
        )
        winner_embed.set_image(url=winner_submission["url"])
        await channelsend.send(embed=winner_embed)


def setup(client):
    client.add_cog(pyduel(client))
