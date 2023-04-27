
from email import message
import discord
import datetime
import requests
from discord.ext import commands
from discord.commands import slash_command
from dotenv import load_dotenv
import os
import json
import info
import chat_exporter
import io
import aiosqlite

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
        if ctx.author.id == int(481377376475938826):
            for i in ctx.guild.members:
                await ctx.send("Adding all users to the database")
                try:
                    await ctx.send(f"{i} has been added to database as {i.id}")
                    data.append({"ID" : i.id, "Warning amount" : 0})
                    with open("warning.json", "w") as writefile:
                        json.dump(data, writefile)
                except Exception as e:
                    print(e)
                    await ctx.send(e)
            await ctx.send("Database set up")
        else: 
            await ctx.send("Only Lord Mic can do this to stop you breaking stuff")

            
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


    @commands.command()
    async def export(self, ctx: commands.Context, limit = 2000, tz_info: str = "UTC", military_time: bool = True):
            if ctx.author.id == int(481377376475938826):
                await ctx.send("All systems go")
                await ctx.send("Exporting chat...")
                transcript = await chat_exporter.export(
                    ctx.channel,
                    limit=limit,
                    tz_info=tz_info,
                    military_time=military_time
                )
                if transcript is None:
                    return
                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{ctx.channel.name}.html",
                )
                #send with out embed
                #if file is too big, discord will not send it
                
                await ctx.send(file=transcript_file, content="Here is the transcript")
            else:
                await ctx.send("You shall not pass")

            
#serverlist
    @commands.command()
    async def serverlist(self,ctx):
        if ctx.author.id == int(481377376475938826):
            for guild in self.client.guilds:
                await ctx.send(f"{guild.name} (id: {guild.id})")
                await ctx.send("Member amount: " + str(guild.member_count))
                #invite link to server system channel
                try:
                    genlink = await guild.system_channel.create_invite(max_age=0, max_uses=0)
                    await ctx.send(genlink)
                except Exception as e:
                    pass

        else:
            await ctx.send("You shall not pass")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def made_backup(self, ctx):
        await ctx.send("Making the backup...")
        async with aiosqlite.connect("backup.db") as db:
            # Create backup table for channels
            await db.execute("CREATE TABLE IF NOT EXISTS channel_backup (category TEXT, channel TEXT, channel_id TEXT, channel_type TEXT)")
            await db.commit()

            # Backup channels
            for category in ctx.guild.categories:
                for channel in category.channels:
                    try:
                        # Backup channel information
                        await db.execute("INSERT INTO channel_backup VALUES (?,?,?,?)", (str(category.name), str(channel.name), str(channel.id), str(channel.type)))
                        await db.commit()

                    except Exception as e:
                        await ctx.send(f"Error backing up {channel.name}: {e}")

            await ctx.send("Backup of channels complete.")

        # Open a new connection to the database for backing up roles
        async with aiosqlite.connect("backup.db") as db:
            # Create backup table for roles
            await db.execute("CREATE TABLE IF NOT EXISTS role_backup (role_id TEXT, role_name TEXT, color INTEGER, permissions INTEGER, position INTEGER)")
            await db.commit()

            # Backup roles
            for role in ctx.guild.roles:
                try:
                    # Backup role information
                    await db.execute("INSERT INTO role_backup VALUES (?,?,?,?,?)", (str(role.id), str(role.name), role.color.value, role.permissions.value, role.position))
                    await db.commit()

                except Exception as e:
                    await ctx.send(f"Error backing up {role.name}: {e}")

        await ctx.send("Backup of roles complete.")
        await ctx.send("Backup complete.")



                
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def restore(self, ctx):
        await ctx.send("Restoring from backup...")
        async with aiosqlite.connect("backup.db") as db:
            # Restore channels
            await db.execute("SELECT category, channel, channel_id, channel_type FROM channel_backup")
            channel_rows = await db.fetchall()
            for channel_row in channel_rows:
                category_name = channel_row[0]
                channel_name = channel_row[1]
                channel_id = int(channel_row[2])
                channel_type = channel_row[3]
                try:
                    category = discord.utils.get(ctx.guild.categories, name=category_name)
                    if not category:
                        category = await ctx.guild.create_category(category_name)
                    if channel_type == "text":
                        await category.create_text_channel(channel_name)
                    elif channel_type == "voice":
                        await category.create_voice_channel(channel_name)
                except Exception as e:
                    await ctx.send(f"Error restoring {channel_name}: {e}")
            
            # Restore roles
            await db.execute("SELECT role_id, role_name, color, permissions, position FROM role_backup")
            role_rows = await db.fetchall()
            for role_row in role_rows:
                role_id = int(role_row[0])
                role_name = role_row[1]
                color = int(role_row[2])
                permissions = discord.Permissions(int(role_row[3]))
                position = int(role_row[4])
                try:
                    role = discord.utils.get(ctx.guild.roles, id=role_id)
                    if not role:
                        role = await ctx.guild.create_role(id=role_id, name=role_name, color=discord.Color(color), permissions=permissions)
                    else:
                        await role.edit(name=role_name, color=discord.Color(color), permissions=permissions)
                    await role.edit(position=position)
                except Exception as e:
                    await ctx.send(f"Error restoring {role_name}: {e}")
            
            # Restore channel permissions
            await db.execute("SELECT channel_id, role_id, read_messages, send_messages, manage_messages, manage_channels FROM channel_permissions_backup")
            channel_perm_rows = await db.fetchall()
            for channel_perm_row in channel_perm_rows:
                channel_id = int(channel_perm_row[0])
                role_id = int(channel_perm_row[1])
                read_messages = bool(channel_perm_row[2])
                send_messages = bool(channel_perm_row[3])
                manage_messages = bool(channel_perm_row[4])
                manage_channels = bool(channel_perm_row[5])
                try:
                    channel = discord.utils.get(ctx.guild.channels, id=channel_id)
                    role = discord.utils.get(ctx.guild.roles, id=role_id)
                    if channel and role:
                        overwrite = discord.PermissionOverwrite()
                        overwrite.read_messages = read_messages
                        overwrite.send_messages = send_messages
                        overwrite.manage_messages = manage_messages
                        overwrite.manage_channels = manage_channels
                        await channel.set_permissions(role, overwrite=overwrite)
                except Exception as e:
                    await ctx.send(f"Error restoring permissions for {channel.name}: {e}")
                    
        await ctx.send("Restore complete.")
    
        await ctx.send("All hail lord tea for saving out asses")
        await ctx.send("Consider donating to him: www.buymeacoffee.com/Michaelrbparker")




    
def setup(client):
    client.add_cog(Mod(client))