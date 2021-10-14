from discord.ext import commands

class TestCog(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.counter = 0

    @commands.Cog.listener() #this is a decorator for events/listeners
    async def on_message(self,ctx):
        if ctx.author == self.client.user:
            return

        print("a message was sent")

    @commands.has_role("Admin")
    @commands.command() #for making a command
    async def add(self,ctx):
        self.counter += 1
        await ctx.send(f"Counter is now {self.counter}")

def setup(client): #required
    client.add_cog(TestCog(client))