import discord
from discord.ext import commands
import random

from config import AIJIN_POWER_SETTINGS


# 設定されたサーバーにだけコマンドを登録
AIJIN_GUILDS = [
    discord.Object(id=guild_id)
    for guild_id in AIJIN_POWER_SETTINGS
]


class AijinSelect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.guilds(*AIJIN_GUILDS)
    @discord.app_commands.command(
        name="aijin_select",
        description="今日の愛人を選びます"
    )
    async def aijin_select(
        self,
        interaction: discord.Interaction
    ):
        # サーバー内でのみ実行可能
        if interaction.guild is None:
            await interaction.response.send_message(
                "このコマンドはサーバー内でのみ使用できます。",
                ephemeral=True
            )
            return

        # サーバーごとの設定を取得
        settings = AIJIN_POWER_SETTINGS.get(
            interaction.guild.id
        )

        if settings is None:
            await interaction.response.send_message(
                "このサーバーでは使用できません。",
                ephemeral=True
            )
            return

        # 実行者が必要なロールを持っているか確認
        role_id = settings["role_id"]

        if not any(
            role.id == role_id
            for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                f"このコマンドは<@&{role_id}>内の人専用です！",
                ephemeral=True
            )
            return

        # サーバー内のメンバーから選択
        members = [
            member
            for member in interaction.guild.members
            if not member.bot
        ]

        # 選択対象がいない場合
        if not members:
            await interaction.response.send_message(
                "選択できるメンバーがいません！",
                ephemeral=True
            )
            return

        # ランダムに1人選択
        selected_member = random.choice(members)

        # 結果を表示
        await interaction.response.send_message(
            f"今日の{interaction.user.mention}の愛人は"
            f"{selected_member.mention}です(*･∀･*)ｴｯﾁｰ!!"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AijinSelect(bot))
