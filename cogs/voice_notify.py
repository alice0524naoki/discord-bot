import discord
from discord.ext import commands

# サーバーごとの設定
GUILD_SETTINGS = {
    1074637664503996446: { # Test
        "role_id": 1243898257801871474,
        "channel_id": 1074637664961179650,
        "voice_name": "VC",
    },
    895995463965216798: { # K#Q
        "role_id": 1521537000866582599,
        "channel_id": 895995463965216801,
        "voice_name": "ララジオ",
    },
    1384346771173675108: { # 討伐会
        "role_id": 1384699338806132736,
        "channel_id": 1384346771970326529,
        "voice_name": "一人語り",
    },
}

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
