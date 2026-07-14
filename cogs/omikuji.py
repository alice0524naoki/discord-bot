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

        settings = None

        if interaction.guild is not None:
            settings = OMIKUJI_NOTIFY.get(interaction.guild.id)

        # 設定ファイルに登録されているサーバーのみ超大当たりを追加
        if settings is not None:
            fortunes = [
                ("大吉", "daikichi.jpeg"),
                ("中吉", "chukichi.jpeg"),
                ("吉", "kichi.jpeg"),
                ("小吉", "shokichi.jpeg"),
                ("末吉", "suekichi.jpeg"),
                ("凶", "kyou.jpeg"),
                ("！！！", "extra.jpeg"),
                ("超大当たり", "super.jpeg")
            ]

            weights = settings.get(
                "weights",
                [13, 19, 20, 18, 14, 8, 8, 0]
            )

            # 通知対象ロールは専用重み
            if any(
                role.id == settings["role_id"]
                for role in interaction.user.roles
            ):
                weights = settings.get(
                    "role_weights",
                    weights
                )

        # 設定ファイルに無いサーバーは従来どおり
        else:
            fortunes = [
                ("大吉", "daikichi.jpeg"),
                ("中吉", "chukichi.jpeg"),
                ("吉", "kichi.jpeg"),
                ("小吉", "shokichi.jpeg"),
                ("末吉", "suekichi.jpeg"),
                ("凶", "kyou.jpeg"),
                ("！！！", "extra.jpeg")
            ]

            weights = [13, 19, 20, 18, 14, 8, 0]

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

        # DMでは通知しない
        if interaction.guild is None:
            return

        settings = OMIKUJI_NOTIFY.get(interaction.guild.id)
        if settings is None:
            return

        channel = interaction.guild.get_channel(
            settings["channel_id"]
        )

        if channel is None:
            return

        # ==========================
        # 超大当たり
        # （役職関係なく通知）
        # ==========================
        if fortune == "超大当たり":
            await channel.send(
                f"🎊🎊 ｽｰﾊﾟｰｵﾐ(*･∀･*)ｴｯﾁｰ!! 🎊🎊"
            )
            return

        # ==========================
        # シークレット（！！！）
        # （従来どおり通知対象ロールのみ）
        # ==========================
        if fortune != "！！！":
            return

        if not any(
            role.id == settings["role_id"]
            for role in interaction.user.roles
        ):
            return

        await channel.send(
            "🎉 ｵﾐ(*･∀･*)ｴｯﾁｰ!!"
        )


async def setup(bot):
    await bot.add_cog(Omikuji(bot))
