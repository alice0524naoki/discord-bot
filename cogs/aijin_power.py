import discord
from discord.ext import commands
import random

from config import AIJIN_POWER_SETTINGS


# 設定されたサーバーにだけコマンドを登録
AIJIN_GUILDS = [
    discord.Object(id=guild_id)
    for guild_id in AIJIN_POWER_SETTINGS
]


class AijinPower(commands.Cog):
    def __init__(self, bot: commands.Bot):
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

        # 指定ロールID
        role_id = settings["role_id"]

        # 指定ロールを持つユーザーは抽選しない
        if any(
            role.id == role_id
            for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                f"{interaction.user.mention} は"
                "愛人を作る側です(*･∀･*)ｴｯﾁｰ!!"
            )
            return

        # 愛人パワーを抽選
        # 1～100：90%
        # 1000：8%
        # 10000：2%
        roll = random.random()

        if roll < 0.90:
            power = random.randint(1, 100)
        elif roll < 0.98:
            power = 1000
        else:
            power = 10000

        # 抽選結果を表示
        await interaction.response.send_message(
            f"{interaction.user.mention} の"
            f"愛人パワーは{power}です！"
        )

        # 1000と10000以外は通知しない
        if power not in (1000, 10000):
            return

        # 通知先チャンネルを取得
        channel = interaction.guild.get_channel(
            settings["channel_id"]
        )

        if channel is None:
            print(
                "愛人パワー通知先が見つかりません: "
                f"{settings['channel_id']}"
            )
            return

        # 愛人パワー1000の通知
        if power == 1000:
            message = (
                f"{interaction.user.mention} は"
                "完ぺきな愛人です(((o(*ﾟ▽ﾟ*)o)))"
            )

        # 愛人パワー10000の通知
        else:
            target_role = interaction.guild.get_role(
                role_id
            )

            # 指定ロールを持つメンバーを個別にメンション
            if target_role is not None:
                mentions = " ".join(
                    member.mention
                    for member in target_role.members
                )
            else:
                mentions = ""

            message = (
                f"{mentions} "
                f"{interaction.user.mention} "
                "おみ(*･∀･*)ｴｯﾁｰ!!"
            )

        await channel.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(AijinPower(bot))
