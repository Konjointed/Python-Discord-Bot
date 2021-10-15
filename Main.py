import discord
import os
import motor.motor_asyncio
from discord.ext import commands
from utils.mongo import Document


intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.guilds = True

async def GetPrefix(client,msg):
    if not msg.guild:
        return commands.when_mentioned_or("!")(client,msg)

    try:
        data = await client.config.find(msg.guild.id)

        if not data or "prefix" not in data:
             return commands.when_mentioned_or("!")(client,msg)
        return commands.when_mentioned_or(data["prefix"])(client,msg)
    except:
        return commands.when_mentioned_or("!")(client,msg) 

client = commands.Bot(
    command_prefix = GetPrefix,
    case_insenitive = True,
    status = discord.Status.idle, 
    intents = intents,
)
client.activity = discord.Game(name=f"Watching over {str(len(client.guilds))} server(s)")

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

    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO"])
    client.db = client.mongo["dbName"]
    client.config = Document(client.db,"config")
    print("Database Initalized")
    for document in await client.config.get_all():
        print(document)

client.run(os.environ["TOKEN"])