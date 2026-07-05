import json
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

    async def load_data(self):
        """JSONとアプリ絵文字を読み込む（起動時1回のみ）"""

        if self.loaded:
            return

        # emoji_map.json
        json_path = Path(__file__).parent.parent / "data" / "emoji_map.json"

        with open(json_path, "r", encoding="utf-8") as f:
            self.char_map = json.load(f)

        # アプリ絵文字取得
        emojis = await self.bot.fetch_application_emojis()

        self.emoji_cache = {
            emoji.name: str(emoji)
            for emoji in emojis
        }

        self.loaded = True

        print(
            f"[EmojiConverter] "
            f"{len(self.char_map)}文字 "
            f"/ {len(self.emoji_cache)}個の絵文字を読み込みました"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_data()

    @app_commands.command(
        name="emoji",
        description="絵文字変換"
    )
    @app_commands.describe(
        text="変換したい文字(ひらがな,カタカナ)"
    )
    async def emoji(
        self,
        interaction: discord.Interaction,
        text: str
    ):

        result = []

        for ch in text:

            # 日本語 → 絵文字名
            emoji_name = self.char_map.get(ch)

            if emoji_name:

                # 絵文字名 → 実際の絵文字
                emoji = self.emoji_cache.get(emoji_name)

                if emoji:
                    result.append(emoji)
                    continue

            # 見つからない文字はそのまま
            result.append(ch)

        await interaction.response.send_message(
            "".join(result)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiConverter(bot))
