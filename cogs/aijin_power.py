import discord
from discord.ext import commands
import random

from config import AIJIN_POWER_SETTINGS


# 設定に登録されているサーバーだけにコマンドを登録
AIJIN_GUILDS = [
    discord.Object(id=guild_id)
    for guild_id in AIJIN_POWER_SETTINGS
]


class AijinPower(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.guilds(*AIJIN_GUILDS)
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

        # 登録されたサーバーか確認
        settings = AIJIN_POWER_SETTINGS.get(
            interaction.guild.id
        )

        if settings is None:
            await interaction.response.send_message(
                "このサーバーでは使用できません。",
                ephemeral=True
            )
            return
            
        
        # 特定ロールを持つユーザーは専用メッセージのみ
        target_role_id = settings["role_id"]

        if any(
            role.id == target_role_id
            for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                f"{interaction.user.mention} は愛人を作る側です(*･∀･*)ｴｯﾁｰ!!"
            )
            return

        # 抽選
        roll = random.random()

        if roll < 0.90:
            power = random.randint(1, 100)
        elif roll < 0.98:
            power = 1000
        else:
            power = 10000

        # 結果を表示
        await interaction.response.send_message(
            f"{interaction.user.mention} の愛人パワーは{power}です！"
        )


async def setup(bot):
    await bot.add_cog(AijinPower(bot))
