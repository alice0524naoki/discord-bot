import discord
from discord.ext import commands
import os

from config import OMIKUJI_NOTIFY

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("環境変数 TOKEN が設定されていません")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        # Cogの読み込み
        await self.load_extension("cogs.omikuji")
        await self.load_extension("cogs.voice_notify")
        await self.load_extension("cogs.emoji_converter")
        await self.load_extension("cogs.aijin_power")

        # グローバルコマンドを同期
        await self.tree.sync()

        # 愛人パワーコマンドを対象サーバーに同期
        for guild_id in OMIKUJI_NOTIFY:
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
