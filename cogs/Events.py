from nextcord.ext import commands

class Events(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author == self.client.user:
            return

        #reply example
        if "hello" in ctx.content:
            await ctx.reply("Hello!")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        #create data for the server in the database if it doesn't already exisit
        if not await self.client.config.find(guild.id):
            await self.client.config.upsert({"_id": guild.id})

        #Send message in the first channel it's able to post in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Thanks for adding me!")
            break

    @commands.Cog.listener() 
    async def on_guild_remove(self,guild):
        #remove the data for the server in the database
        if await self.client.config.find(guild.id):
            await self.client.config.delete_by_id(guild.id)\

    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}!")
        else:
            print("no system channel!")
            
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send(f"{member} left :(")
        else:
            print("no system channel!")

def setup(client):
    client.add_cog(Events(client))