import discord
from discord.ext import commands
import random

from config import OMIKUJI_NOTIFY


class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            ("！！！", "extra.jpeg")
        ]

        # デフォルト重み
        weights = [13, 19, 20, 18, 14, 8, 8]

        # サーバーごとの重み設定
        if interaction.guild is not None:
            settings = OMIKUJI_NOTIFY.get(interaction.guild.id)

            if settings is not None and "weights" in settings:
                weights = settings["weights"]

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

        # 「！！！」以外は通知しない
        if fortune != "！！！":
            return

        if interaction.guild is None:
            return

        settings = OMIKUJI_NOTIFY.get(interaction.guild.id)
        if settings is None:
            return

        # 指定ロールを持っているか確認
        if not any(
            role.id == settings["role_id"]
            for role in interaction.user.roles
        ):
            return

        channel = interaction.guild.get_channel(
            settings["channel_id"]
        )

        if channel is None:
            return

        await channel.send(
            f"🎉 {interaction.user.mention} さんが **！！！** を引きました！"
        )


async def setup(bot):
    await bot.add_cog(Omikuji(bot))
