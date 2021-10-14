import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()

client = commands.Bot(command_prefix = "!")

#Load all the cogs in the cog folder
for FileName in os.listdir("./cogs"):
    if FileName.endswith(".py"):
        client.load_extension(f"cogs.{FileName[:-3]}")

#global check
@client.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Bot is in {str(len(client.guilds))} server(s)")
    
    await client.change_presence(activity=discord.Game(name="Hello!"))

client.run(getenv("TOKEN"))