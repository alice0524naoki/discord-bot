import discord
from discord.ext import commands
import random

class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="omikuji", description="オミくじを引きます")
    async def omikuji(self, interaction: discord.Interaction):

        fortunes = [
            ("大吉", "daikichi.jpeg"),
            ("中吉", "chukichi.jpeg"),
            ("吉", "kichi.jpeg"),
            ("小吉", "shokichi.jpeg"),
            ("末吉", "suekichi.jpeg"),
            ("凶", "kyou.jpeg"),
            ("！！！", "extra.jpeg")
        ]

        weights = [15, 20, 20, 20, 15, 10, 10]

        fortune, filename = random.choices(fortunes, weights=weights, k=1)[0]

        img_path = f"omikuji_images/{filename}"
        file = discord.File(img_path)

        await interaction.response.send_message(
            f"{interaction.user.mention} の今日の運勢は… **{fortune}** です！",
            file=file
        )

async def setup(bot):
    await bot.add_cog(Omikuji(bot))
