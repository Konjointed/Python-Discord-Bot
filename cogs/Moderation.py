from discord.ext import commands
from typing import Optional
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands import Cog, Greedy
from discord import Embed, Member, message

class Moderation(commands.Cog):

    def __init__(self,client):
        self.client = client

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

def setup(client):
    client.add_cog(Moderation(client))