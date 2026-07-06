import json
import re
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands


class EmojiConverter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # 文字 → 絵文字名
        self.char_map = {}

        # 絵文字名 → <:name:id>
        self.emoji_cache = {}

        self.loaded = False

        # Discord構文
        self.discord_pattern = re.compile(
            r"(<a?:[A-Za-z0-9_]+:\d+>"      # カスタム絵文字
            r"|<@[!&]?\d+>"                 # ユーザー・ロール
            r"|<#\d+>"                      # チャンネル
            r"|<t:\d+(?::[tTdDfFR])?>"      # タイムスタンプ
            r"|https?://\S+)"               # URL
        )

    async def load_data(self):

        if self.loaded:
            return

        data_dir = Path(__file__).parent.parent / "data"

        # *_map.json をすべて読み込む
        for path in sorted(data_dir.glob("*_map.json")):

            with open(path, "r", encoding="utf-8") as f:
                self.char_map.update(json.load(f))

        # アプリ絵文字取得（起動時1回）
        emojis = await self.bot.fetch_application_emojis()

        self.emoji_cache = {
            emoji.name: str(emoji)
            for emoji in emojis
        }

        self.loaded = True

        print(f"[EmojiConverter] {len(self.char_map)}文字を読み込み")
        print(f"[EmojiConverter] {len(self.emoji_cache)}個の絵文字をキャッシュ")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_data()

    def convert_segment(self, text: str) -> str:
        """Discord構文以外を変換"""

        result = []

        for ch in text:

            emoji_name = self.char_map.get(ch)

            if emoji_name:
                emoji = self.emoji_cache.get(emoji_name)

                if emoji:
                    result.append(emoji)
                else:
                    result.append(ch)
            else:
                result.append(ch)

        return "".join(result)

    def convert_text(self, text: str) -> str:
        """Discord構文を壊さず変換"""

        parts = self.discord_pattern.split(text)

        result = []

        for part in parts:

            if not part:
                continue

            # Discord構文ならそのまま
            if self.discord_pattern.fullmatch(part):
                result.append(part)

            # 通常文字だけ変換
            else:
                result.append(self.convert_segment(part))

        return "".join(result)

    @app_commands.command(
        name="emoji",
        description="文字列をアプリ絵文字へ変換します"
    )
    @app_commands.describe(
        text="変換したい文字列"
    )
    async def emoji(
        self,
        interaction: discord.Interaction,
        text: str
    ):

        await interaction.response.send_message(
            self.convert_text(text)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiConverter(bot))
