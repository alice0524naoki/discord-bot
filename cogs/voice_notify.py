import discord
from discord.ext import commands

from config import GUILD_SETTINGS


class VoiceNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # 入室していない場合は無視
        if after.channel is None:
            return

        # 同じチャンネル内の移動は無視
        if before.channel == after.channel:
            return

        guild_id = member.guild.id

        # 設定がないサーバーは無視
        settings = GUILD_SETTINGS.get(guild_id)
        if settings is None:
            return

        role_id = settings["role_id"]
        channel_id = settings["channel_id"]
        voice_name = settings["voice_name"]

        # 指定ロールを持っていない場合は無視
        if not any(role.id == role_id for role in member.roles):
            return

        # 最初の1人だけ通知
        if len(after.channel.members) != 1:
            return

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        await channel.send(
            f"🔊 {member.mention} さんが **{voice_name}** をはじめたみたいです|ω・)ﾁﾗｯ"
        )


async def setup(bot):
    await bot.add_cog(VoiceNotify(bot))
