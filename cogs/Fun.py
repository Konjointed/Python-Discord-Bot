import asyncio
from discord.ext import commands
from random import choice, randint

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def EightBall(self,ctx,*,question):
        responses = ["It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {choice(responses)}")

    @commands.guild_only()
    @commands.command()
    async def RollDice(self,ctx,number = 6): #default is 6
        await ctx.send(f"Rolling a {number} sided di")
        await asyncio.sleep(1)
        await ctx.send(f"you rolled a **{randint(1,int(number))}**!")    

    @commands.guild_only()
    @commands.command()
    async def Say(self,ctx,msg):
        await ctx.send(msg)    

def setup(client):
    client.add_cog(Fun(client))