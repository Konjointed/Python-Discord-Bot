import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.guilds = True
client = commands.Bot(
    command_prefix = commands.when_mentioned_or("!"),
    case_insenitive = True,
    status = discord.Status.idle,
    intents = intents,
)
client.activity = discord.Game(name=f"Watchinver over {str(len(client.guilds))} server(s)")

#Load all the cogs in the cog folder
for FileName in os.listdir("./cogs"):
    if FileName.endswith(".py"):
        client.load_extension(f"cogs.{FileName[:-3]}")

#global check
#runs whenever a command does
@client.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Bot is in {str(len(client.guilds))} server(s)")

client.run(getenv("TOKEN"))