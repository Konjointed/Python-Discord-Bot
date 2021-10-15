import discord
import asyncio
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from discord.ext import commands, tasks
from typing import Optional
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands import Cog, Greedy
from discord import Embed, Member, message
from copy import deepcopy

class Moderation(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.mute_task = self.check_current_mutes.start()

    def cog_unload(self):
        self.mute_task.cancel()

    #this is so when the bot comes back online it can unmute anyone that needs to be muted (I think?)
    #thing to remember: use asyncio.Task instead (according to some discord user)
    @tasks.loop(minutes=5)
    async def check_current_mutes(self):
        CurrentTime = datetime.now()
        mutes = deepcopy(self.client.muted_users) #not sure what the point of this is, but it's literally just an exact copy
        for key,value in mutes.items():
            if value["muteDuration"] is None: #this is a perm mute so just conitnue
                continue

            UnmuteTime = value["mutedAt"] + relativedelta(seconds=value["muteDuration"])

            if CurrentTime >= UnmuteTime:
                guild = self.client.get_guild(value["guildId"])
                member = guild.get_member(value["_id"])
                await self.unmute_members(guild,[member])

    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.client.wait_until_ready()

    #greedy is esentially multiple arguments of that type it will keep converting until it can't
    #also greedy is an optional arg
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    @commands.command(
        name = "kick",
        help = "kick a member from the server",
    )
    async def Kick(self,ctx,targets: Greedy[Member],*,reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("Missing a required argument")
        else:
            for target in targets:
                await target.kick(reason = reason)

    @commands.bot_has_permissions(ban_members = True)
    @commands.has_permissions(ban_members = True)
    @commands.command(
        name = "ban",
        help = "ban a member from the server",
    )
    async def Ban(self,ctx,targets: Greedy[Member],*,reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("Missing a required argument")
        else:
            for target in targets:
                await target.kick(reason = reason)

    async def mute_members(self,ctx,message,targets,hours,reason):
        unmutes = []
        mute_role = discord.utils.get(message.guild.roles,name="mute")

        #Make a mute role
        if not mute_role:
            try:
                mute_role = await message.guild.create_role(name="mute")

                for channel in message.guild.channels:
                    await channel.set_permissions(mute_role,speak=False,send_messages=False)
            except:
                return

        for target in targets:
            if not mute_role in target.roles:
                if message.guild.me.top_role.position > target.top_role.position:
                    #mute information
                    data = {
                        "_id": target.id,
                        "mutedAt": datetime.now(),
                        "muteDuration": hours or None,
                        "mutedBy": ctx.author.id,
                        "guildId": ctx.guild.id,                  
                    }
                    await self.client.mutes.upsert(data) #put it on the database
                    self.client.muted_users[target.id] = data #not exactly sure why this is needed
                    await target.edit(roles=[mute_role]) #give them the mute role

                    if hours:
                        unmutes.append(target)

        return unmutes

    async def unmute_members(self,guild,targets,*,reason="Mute time expired"):
        mute_role = discord.utils.get(guild.roles,name="mute")

        for target in targets:
            if mute_role in target.roles:
                await target.remove_roles(mute_role)

            await self.client.mutes.delete(target.id)
            try:
                self.client.muted_users.pop(target.id)
            except KeyError:
                return

    @commands.bot_has_permissions(administrator = True)
    @commands.has_permissions(administrator = True)
    @commands.command()
    async def Mute(self,ctx,targets:Greedy[Member],hours:Optional[int],*,reason:Optional[str]):

        if len(targets):
            unmutes = await self.mute_members(ctx,ctx.message,targets,hours,reason)

            if len(unmutes):
                await asyncio.sleep(hours)
                await self.unmute_members(ctx.guild,targets)

    @commands.bot_has_permissions(administrator = True)
    @commands.has_permissions(administrator = True)
    @commands.command()
    async def Unmute(self,ctx,targets:Greedy[Member],hours:Optional[int],*,reason:Optional[str]):
        if len(targets):
            await self.unmute_members(ctx.guild,targets,reason=reason)

    @commands.bot_has_permissions(administrator = True)
    @commands.has_permissions(administrator = True)
    @commands.command(
        name = "changeprefix",
        help = "change the prefix of the bot",
        aliases = ["newprefix","cp","changep","cprefix","np"] #np = newprefix cp = changeprefix
    )
    async def ChangePrefix(self,ctx,*,prefix="!"):
        await self.client.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(f"The prefix has been changed to {prefix}")

    @commands.bot_has_permissions(administrator = True)
    @commands.has_permissions(administrator = True)
    @commands.command(
        name = "resetprefix",
        help = "reset the current prefix back to the default one",
        aliases = ["rp","rprefix","removeprefix"] 
    )
    async def ResetPrefix(self,ctx):
        await self.client.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("Prefix has been reset to default")

    @commands.bot_has_permissions(administrator = True)
    @commands.has_permissions(administrator = True)
    @commands.command(
        name = "setuplogs",
        help = "Setup a log channel",
        aliases = ["sp","makelogschannel","setuplogchannel","mp"] 
    )
    async def LogChannel(self,ctx):
        GuildId = ctx.message.guild.id
        Data = await self.client.config.find(GuildId)

        if "LogChannelId" not in Data:
            await self.client.config.upsert({"_id": GuildId, "LogChannelId": 0})

        try:
            if await self.client.fetch_channel(Data["LogChannelId"]):
                await ctx.send("You already have a log channel setup")
                return
        except:
            LogChannel = await ctx.message.guild.create_text_channel("logs")
            await self.client.config.upsert({"_id": GuildId, "LogChannelId": LogChannel.id})
            await ctx.send("Successfully made logs channel")

def setup(client):
    client.add_cog(Moderation(client))