import discord
from discord import app_commands
from discord.ext import commands
import random
import os


TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"こんにちは、{ctx.author.name}！")

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot(command_prefix="!", intents=discord.Intents.default())

@bot.tree.command(name="omikuji", description="今日の運勢を占います")
async def omikuji(interaction: discord.Interaction):
    results = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
    choice = random.choice(results)
    await interaction.response.send_message(
        f"{interaction.user.mention} の今日の運勢は… **{choice}** です！"
    )


bot.run(TOKEN)
