import discord
from discord import app_commands
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.tree.command(name="omikuji", description="オミくじを引きます")
async def omikuji(interaction: discord.Interaction):

    fortunes = [
        ("大吉", "daikichi.jpeg"),
        ("中吉", "chukichi.jpeg"),
        ("吉", "kichi.jpeg"),
        ("小吉", "shokichi.jpeg"),
        ("末吉", "suekichi.jpeg"),
        ("凶", "kyou.jpeg"),
        ("！！！", "extra.jpeg")
    ]

    fortune, filename = random.choice(fortunes)

    # フォルダ分けに対応したパス
    img_path = f"omikuji_images/{filename}"

    file = discord.File(img_path)
    await interaction.response.send_message(
        f"{interaction.user.mention} の今日の運勢は… **{fortune}** です！",
        file=file
    )

bot.run(TOKEN)
