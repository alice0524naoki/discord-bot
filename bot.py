import discord
from discord.ext import commands

TOKEN = "MTE4MDMzNTYzMTQxNTY1NjU2OA.GWqUcr.24ZylIuiRDWbpgAwYwOcy4vv7eXB3wTy8BSF_E"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"こんにちは、{ctx.author.name}！")

bot.run(TOKEN)
