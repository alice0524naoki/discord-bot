import discord
from discord.ext import commands
import os
from utils.pdf_generator import generate_pdf
import re

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)

class FormEnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="form_end",
        description="受付を終了しPDFを出力します"
    )
    async def form_end(self, interaction: discord.Interaction):

        data = self.bot.event_data
        if data is None:
            await interaction.response.send_message(
                "受付が開始されていません。",
                ephemeral=True
            )
            return

        # ★ 最初に応答（3秒以内）
        await interaction.response.defer()

        # 表示用とファイル名用を分離
        safe_title = sanitize_filename(data["title"])
        safe_date = sanitize_filename(data["date_file"])  # ← m-d が入っている

        filename = f"{safe_title}_{safe_date}.pdf"

        print(f"[PDF] 生成開始: {filename}")

        try:
            generate_pdf(data, filename)
        except Exception as e:
            print(f"[PDF] 例外発生: {e}")
            await interaction.followup.send(f"PDF生成中にエラーが発生しました: {e}")
            return

        abs_path = os.path.abspath(filename)

        await interaction.followup.send(
            "受付を終了しました。PDFを出力します。",
            file=discord.File(abs_path)
        )

        self.bot.event_data = None


async def setup(bot):
    await bot.add_cog(FormEnd(bot))
