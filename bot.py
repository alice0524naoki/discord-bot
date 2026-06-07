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

    # 運勢と画像ファイル名
    fortunes = [
        ("大吉", "daikichi.jpeg"),
        ("中吉", "chukichi.jpeg"),
        ("吉", "kichi.jpeg"),
        ("小吉", "shokichi.jpeg"),
        ("末吉", "suekichi.jpeg"),
        ("凶", "kyou.jpeg"),
        ("！！！", "extra.jpeg")
    ]

    # 各運勢の確率（合計100でなくてもOK）
    weights = [
        15,  # 大吉
        20,  # 中吉
        25,  # 吉
        25,  # 小吉
        20,  # 末吉
        10,  # 凶
        5    # ！！！
    ]

    # 重み付きランダム
    fortune, filename = random.choices(fortunes, weights=weights, k=1)[0]

    # フォルダ分け対応
    img_path = f"omikuji_images/{filename}"
    file = discord.File(img_path)

    await interaction.response.send_message(
        f"{interaction.user.mention} の今日の運勢は… **{fortune}** です！",
        file=file
    )

bot.run(TOKEN)
