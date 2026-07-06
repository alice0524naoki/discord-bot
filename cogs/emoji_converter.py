import json
import re
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands


class EmojiConverter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # 「文字 → 絵文字名」
        self.char_map = {}

        # 「絵文字名 → <:name:id>」
        self.emoji_cache = {}

        self.loaded = False

        # Discord構文を保護する正規表現
        self.discord_pattern = re.compile(
            r"<a?:[A-Za-z0-9_]+:\d+>"      # カスタム絵文字
            r"|<@[!&]?\d+>"                # ユーザー・ロールメンション
            r"|<#\d+>"                     # チャンネルメンション
            r"|<t:\d+(?::[tTdDfFR])?>"     # タイムスタンプ
            r"|https?://\S+"               # URL
        )

    async def load_data(self):
        """JSON・アプリ絵文字を読み込む"""

        if self.loaded:
            return

        data_dir = Path(__file__).parent.parent / "data"

        # dataフォルダ内の *_map.json を自動読み込み
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

    def convert_text(self, text: str) -> str:
        """文字列をアプリ絵文字へ変換"""

        protected = {}

        def save(match):
            key = f"__DISCORD_{len(protected)}__"
            protected[key] = match.group(0)
            return key

        # Discord構文を一時退避
        text = self.discord_pattern.sub(save, text)

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

        result = "".join(result)

        # Discord構文を復元
        for key, value in protected.items():
            result = result.replace(key, value)

        return result

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
