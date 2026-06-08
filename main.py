import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.omikuji")
        await self.load_extension("cogs.storage")
        await self.load_extension("cogs.form_start")
        await self.load_extension("cogs.form_end")
        await self.load_extension("cogs.entry_buttons")
        await self.load_extension("cogs.entry_modals")
        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

bot.run(TOKEN)
