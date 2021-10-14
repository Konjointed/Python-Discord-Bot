import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

class ErrorHandler(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        #Check if the command already has an error handler (I think?)
        if hasattr(ctx.command,"on_error"):
            return

        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after"
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        elif isinstance(error,CommandNotFound):
            return
        else:
            message = "Oh no! Something went wrong while running the command!"

        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)

def setup(client):
    client.add_cog(ErrorHandler(client))