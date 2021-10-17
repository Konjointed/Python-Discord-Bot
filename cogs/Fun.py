import asyncio
import os
from asyncio.windows_events import NULL
import discord
import random
import json
import praw
import aiohttp
from discord import Embed
from discord.ext import commands
from random import choice, randint

reddit = praw.Reddit(client_id = "Hep_3WWz096efg",
                     client_secret = "8mbT11XiB6geg-nACN012JsmY1RXlg",
                     user_agent = "pythonpraw",
                     check_for_async=False)

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(
        name = "8ball",
        help = "ask a question!",
        aliases = ["ask"]
    )
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

    @commands.command(
        name = "dice",
        help = "roll a di with any number of sides!",
        aliases = ["roll","di"]
    )
    async def RollDice(self,ctx,number = 6): #default is 6
        await ctx.send(f"Rolling a {number} sided di")
        await asyncio.sleep(1)
        await ctx.send(f"you rolled a **{randint(1,int(number))}**!")    

    @commands.command(
        name = "repeat",
        help = "make the bot repeat what you say",
        aliases = ["say"]
    )
    async def Repeat(self,ctx,msg):
        await ctx.send(msg)    

    @commands.command()
    async def giphy(self,ctx,*,search=None):
        embed = discord.Embed(colour=discord.Colour.blue())
        session = aiohttp.ClientSession()

        if not search:
            response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={os.environ["GIPHY"]}')
            print(response)
            data = json.loads(await response.text())
            print(data)
            embed.set_image(url=data)
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace('','+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={os.environ["GIPHY"]}&limit=10')
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()
        await ctx.send(embed=embed)

    @commands.command(
        help = "Sends a random spicy hot meme from r/memes"
        )
    async def meme(self,ctx):

        #Create a submmistion to r/test
        # reddit.subreddit("test").submit("Test submission",url="https://reddit.com")

        # Comment on a known submission
        # submission = reddit.submission(url="https://www.reddit.com/comments/5e1az9")
        # submission.reply("Super rad!")

        # Reply to the first comment of a weekly top thread of a moderated community
        # submission = next(reddit.subreddit("mod").top("week"))
        # submission.comments[0].reply("An automated reply")

        # Output score for the first 256 items on the frontpage
        # for submission in reddit.front.hot(limit=256):
        #     print(submission.score)

        # Obtain the moderator listing for r/redditdev
        # for moderator in reddit.subreddit("redditdev").moderator():
        #     print(moderator)

        submissions = reddit.subreddit("memes").hot()
        post_to_pick = randint(1,100)
        for i in range(0,post_to_pick):
            submission = next(x for x in submissions if not x.stickied)

        embed = Embed(title = submission.title,
                      colour = ctx.message.guild.owner.colour)
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"Meme from r/memes")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))