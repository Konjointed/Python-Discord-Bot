import asyncio
import nextcord
from nextcord.ext import commands
from random import choice, randint
from datetime import datetime,timedelta
from nextcord.ext.commands import Greedy
from nextcord import Embed, Member
from typing import Optional

from nextcord.ext.commands.errors import DisabledCommand
class Utilities(commands.Cog):

    def __init__(self,client):
        self.client = client

    #This command is just random did it for testing
    @commands.command(
         name = "remind", 
        help = "set a reminder for yourself",  
    )
    async def Remind(self,ctx,hours,*,reminder):
        data = {
            "_id": ctx.author.id,
            "createdAt": datetime.now(),
            "time": hours or None,
            "guildId": ctx.guild.id,  
            "reminder": reminder,
        }
        await self.client.reminders.upsert(data)
        await asyncio.sleep(int(hours))
        await ctx.send(f"hey I'm here to remind you about your reminder: {reminder}")

    @commands.command(
        name = "reminders", 
        help = "show a list of your reminders",
    )
    async def Reminders(self,ctx,hours,*,reminder):
        Data = await self.client.reminders.find(ctx.author.id)
        for reminder in Data:
            print("reminder")

    @commands.command(
        name = "userinfo", 
        help = "gets info about a user",
        aliases = ["ui","memberinfo","mi"])
    async def userinfo(self,ctx,target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title = "User Information",
                      colour = target.colour,
                      timestamp = datetime.utcnow())

        embed.set_thumbnail(url = target.avatar_url)

        fields = [("ID",target.id,False),
                  ("Name",str(target),True),
                  ("Bot?",target.bot,True),
                  ("Top Role",target.top_role.mention,True),
                  ("Status",str(target.status).title(),True),
                  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                  ("Created At",target.created_at.strftime("%d/%m/%Y %H:%M:%S"),True),
                  ("Joined At",target.joined_at.strftime("%d/%m/%Y %H:%M:%S"),True),
                  ("Boosted", bool(target.premium_since),True)]

        for name,value,inline in fields:
            embed.add_field(name = name, value = value, inline = inline)

        await ctx.send(embed = embed)   

    @commands.command(
        name = "serverinfo", 
        help = "gets info about the server",
        aliases = ["si","guildinfo","gi"])
    async def serverinfo(self,ctx):
        embed = Embed(title = "Server Information",
                      colour = ctx.guild.owner.colour,
                      timestamp = datetime.utcnow())

        embed.set_thumbnail(url = ctx.guild.icon_url)

        fields = [("ID", ctx.guild.id, True),
                 ("Owner", ctx.guild.owner, True),
                 ("Region", ctx.guild.region, True),
                 ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                 ("Members", len(ctx.guild.members), True),
                 ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                 ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                 ("Banned members", len(await ctx.guild.bans()), True),
                 ("Text channels", len(ctx.guild.text_channels), True),
                 ("Voice channels", len(ctx.guild.voice_channels), True),
                 ("Categories", len(ctx.guild.categories), True),
                 ("Roles", len(ctx.guild.roles), True),
                 ("Invites", len(await ctx.guild.invites()), True),
                 ("\u200b", "\u200b", True)]

        for name,value,inline in fields:
            embed.add_field(name = name, value = value, inline = inline)

        await ctx.send(embed = embed)

    

def setup(client):
    client.add_cog(Utilities(client))