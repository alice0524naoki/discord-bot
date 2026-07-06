import json
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands


class EmojiConverter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # 全ての文字マップ
        self.char_map = {}

        # アプリ絵文字キャッシュ
        self.emoji_cache = {}

        self.loaded = False

    async def load_data(self):
        """JSON・アプリ絵文字を読み込む"""

        if self.loaded:
            return

        data_dir = Path(__file__).parent.parent / "data"

        json_files = (
            "hiragana_map.json",
            "katakana_map.json",
            "alphabet_map.json",
            "number_map.json",
            "symbol_map.json"
        )

        # JSONを結合
        for filename in json_files:
            path = data_dir / filename

            if not path.exists():
                print(f"[EmojiConverter] {filename} が見つかりません")
                continue

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

    @app_commands.command(
        name="emoji",
        description="文字をアプリ絵文字へ変換します"
    )
    @app_commands.describe(
        text="変換する文字列"
    )
    async def emoji(
        self,
        interaction: discord.Interaction,
        text: str
    ):

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

        await interaction.response.send_message(
            "".join(result)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiConverter(bot))
