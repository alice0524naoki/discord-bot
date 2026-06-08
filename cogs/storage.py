from discord.ext import commands

class Storage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.event_data = None

async def setup(bot):
    await bot.add_cog(Storage(bot))
