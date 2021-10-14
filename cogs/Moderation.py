from discord.ext import commands
from typing import Optional
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands import Cog, Greedy
from discord import Embed, Member

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


def setup(client):
    client.add_cog(Moderation(client))