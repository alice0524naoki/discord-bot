import random
from pathlib import Path

import discord
from discord.ext import commands

from config import OMIKUJI_NOTIFY


class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_dir = Path(__file__).parent / "omikuji_images"

    @discord.app_commands.command(
        name="omikuji",
        description="オミくじを引きます"
    )
    async def omikuji(self, interaction: discord.Interaction):

        fortunes = [
            ("大吉", "daikichi.jpeg"),
            ("中吉", "chukichi.jpeg"),
            ("吉", "kichi.jpeg"),
            ("小吉", "shokichi.jpeg"),
            ("末吉", "suekichi.jpeg"),
            ("凶", "kyou.jpeg"),
            ("！！！", "extra.jpeg"),
        ]

        weights = [13, 19, 20, 18, 14, 8, 80000]

        fortune, filename = random.choices(
            fortunes,
            weights=weights,
            k=1
        )[0]

        file = discord.File(self.image_dir / filename)

        await interaction.response.send_message(
            f"{interaction.user.mention} の今日の運勢は… **{fortune}** です！",
            file=file
        )

        # 「！！！」を引いた場合のみ通知
        if (
            fortune == "！！！"
            and interaction.guild is not None
            and interaction.guild.id == OMIKUJI_NOTIFY["guild_id"]
            and any(
                role.id == OMIKUJI_NOTIFY["role_id"]
                for role in interaction.user.roles
            )
        ):
            channel = interaction.guild.get_channel(
                OMIKUJI_NOTIFY["channel_id"]
            )

            if channel is not None:
                await channel.send(
                    f"🎉 {interaction.user.mention} さんが **！！！** を引きました！"
                )


async def setup(bot):
    await bot.add_cog(Omikuji(bot))
