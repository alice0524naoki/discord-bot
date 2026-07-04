import discord
from discord.ext import commands
import random

from config import OMIKUJI_NOTIFY


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

        weights = [13, 19, 20, 18, 14, 8, 8000]

        fortune, filename = random.choices(
            fortunes,
            weights=weights,
            k=1
        )[0]

        img_path = f"omikuji_images/{filename}"
        file = discord.File(img_path)

        await interaction.response.send_message(
            f"{interaction.user.mention} の今日の運勢は… **{fortune}** です！",
            file=file
        )

        # 「！！！」を引いたときのみ通知
        if fortune != "！！！":
            return

        # 指定サーバー以外では通知しない
        if interaction.guild is None:
            return

        if interaction.guild.id != OMIKUJI_NOTIFY["guild_id"]:
            return

        # 指定役職を持っているか確認
        if not any(role.id == OMIKUJI_NOTIFY["role_id"] for role in interaction.user.roles):
            return

        channel = interaction.guild.get_channel(OMIKUJI_NOTIFY["channel_id"])
        if channel is None:
            return

        await channel.send(
            f"🎉 {interaction.user.mention} さんが **！！！** を引きました！"
        )


async def setup(bot):
    await bot.add_cog(Omikuji(bot))
