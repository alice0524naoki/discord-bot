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
        description="今日の愛人は?(っ ॑꒳ ॑c)ﾜｸﾜｸ"
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

        # 実行に必要なロールID
        role_id = settings["role_id"]

        # 実行者が指定ロールを持っているか確認
        if not any(
            role.id == role_id
            for role in interaction.user.roles
        ):
            # 指定ロールを持つメンバー本人を取得
            target_role = interaction.guild.get_role(role_id)

            role_member = (
                next(iter(target_role.members), None)
                if target_role is not None
                else None
            )

            # メンバー本人をメンションして案内
            if role_member is not None:
                message = (
                    f"このコマンドは{role_member.mention}専用です！"
                )
            else:
                message = "このコマンドは指定メンバー専用です！"

            await interaction.response.send_message(message)
            return

        # サーバー内のBot以外のメンバーから選択
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
