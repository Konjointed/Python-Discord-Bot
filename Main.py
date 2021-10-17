import discord
import os
from discord import activity
import motor.motor_asyncio
import random
import sys
import logging
from discord.ext import commands
from utils.mongo import Document

sys.dont_write_bytecode = True #apparently this is how you prevent __pycache__ folders being created?

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.guilds = True

async def GetPrefix(client,msg):
    if not msg.guild:
        return commands.when_mentioned_or("!")(client,msg)

    try:
        data = await client.config.find(msg.guild.id) #find the data of the server in the mongo database by the id of the server

        if not data or "prefix" not in data: #if data is not found (so no data at all) or no prefix is in the data return default stuff
             return commands.when_mentioned_or("!")(client,msg)
        return commands.when_mentioned_or(data["prefix"])(client,msg)
    except:
        return commands.when_mentioned_or("!")(client,msg) 

client = commands.Bot(
    command_prefix = GetPrefix,
    case_insenitive = True,
    status = discord.Status.idle, 
    activity = discord.Activity(type=discord.ActivityType.watching, name="!help"),
    intents = intents,
)

client.muted_users = {}

#Load all the cogs in the cog folder
for FileName in os.listdir("./cogs"):
    if FileName.endswith(".py"):
        client.load_extension(f"cogs.{FileName[:-3]}")

#global check (temporaily having this here for learning)
#runs whenever a command does
@client.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@client.command()
async def presence(ctx,*,text):
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=text))

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Bot is in {str(len(client.guilds))} server(s)")

    #setup mongodb
    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO"])
    client.db = client.mongo["dbName"]
    client.mutes = Document(client.db,"mutes")
    client.config = Document(client.db,"config")
    client.reminders = Document(client.db,"reminders")
    print("Database Initalized")

    current_mutes = await client.mutes.get_all()
    for mute in current_mutes:
        client.muted_users[mute["_id"]] = mute

    #Remove any data to the database for servers the bot was removed from when it was offline
    for document in await client.config.get_all():
        if not client.get_guild(document["_id"]):
            await client.config.delete_by_id(document["_id"])

    #Add any data to the database for servers the bot joined while it was offline
    for guild in client.guilds:
        if not await client.config.find(guild.id):
            await client.config.upsert({"_id": guild.id})

client.run(os.environ["TOKEN"])