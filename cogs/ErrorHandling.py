import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def OnCommandError(self,ctx,error):
        #Check if the command already has an error handler (I think?)
        # if hasattr(ctx.command,"on_error"):
        #     return

        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You are missing the required permissions to run this command")

def setup(client):
    client.add_cog(ErrorHandler(client))