
import discord
from discord.ext import commands
import random

from config import OMIKUJI_NOTIFY


class AijinPower(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="aijin_power",
        description="愛人パワーを測定します"
    )
    async def aijin_power(
        self,
        interaction: discord.Interaction
    ):
        # DMでは使用不可
        if interaction.guild is None:
            await interaction.response.send_message(
                "このコマンドはサーバー内でのみ使用できます。",
                ephemeral=True
            )
            return

        # 設定済みサーバーのみ使用可能
        settings = OMIKUJI_NOTIFY.get(
            interaction.guild.id
        )

        if settings is None:
            await interaction.response.send_message(
                "このサーバーでは使用できません。",
                ephemeral=True
            )
            return

        # 既存のrole_idを使用
        target_role_id = settings["role_id"]

        # 特定ロールを持つユーザーは専用メッセージのみ
        if any(
            role.id == target_role_id
            for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                "あなたは愛人を作る側です(*･∀･*)ｴｯﾁｰ!!"
            )
            return

        # 愛人パワー抽選
        roll = random.random()

        if roll < 0.90:
            power = random.randint(1, 100)
        elif roll < 0.98:
            power = 1000
        else:
            power = 10000

        # 結果を表示
        await interaction.response.send_message(
            f"{interaction.user.display_name}の"
            f"愛人パワーは{power}です！"
        )


async def setup(bot):
    await bot.add_cog(AijinPower(bot))
