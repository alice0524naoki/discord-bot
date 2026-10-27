import discord
from discord.ext import commands
import os

from config import AIJIN_POWER_SETTINGS

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("環境変数 TOKEN が設定されていません")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        # 既存のCog
        await self.load_extension("cogs.omikuji")
        await self.load_extension("cogs.voice_notify")
        await self.load_extension("cogs.emoji_converter")
        await self.load_extension("cogs.aijin_power")
        await self.load_extension("cogs.aijin_select")

        # 既存のグローバルコマンドを同期
        await self.tree.sync()

        # 対象サーバーだけに同期
        for guild_id in AIJIN_POWER_SETTINGS:
            guild = discord.Object(id=guild_id)
            await self.tree.sync(guild=guild)

        print("スラッシュコマンドを同期しました")


bot = MyBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")


bot.run(TOKEN)
