import discord
from discord import app_commands
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

# Bot クラスを拡張してスラッシュコマンド同期を自動化
class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()
        print("スラッシュコマンドを同期しました")

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

# スラッシュコマンド（/omikuji）
@bot.tree.command(name="omikuji", description="今日の運勢を占います")
async def omikuji(interaction: discord.Interaction):
    results = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
    choice = random.choice(results)
    await interaction.response.send_message(
        f"{interaction.user.mention} の今日の運勢は… **{choice}** です！"
    )

bot.run(TOKEN)
