import discord
from discord.ext import commands
from utils.pdf_generator import generate_pdf
import os

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

        # 1. 即時応答
        await interaction.response.send_message("PDF を生成しています…")

        # 2. ピン解除
        try:
            msg = await interaction.channel.fetch_message(data["message_id"])
            await msg.unpin()
        except:
            pass

        # 3. PDF生成
        filename = f"{data['title']}_{data['date']}.pdf"
        generate_pdf(data, filename)

        # ★ ここで PDF が存在するか確認（重要）
        if not os.path.exists(filename):
            await interaction.followup.send(
                f"PDF の生成に失敗しました。ファイルが見つかりません: {filename}"
            )
            return

        # 4. followup で PDF を送信
        await interaction.followup.send(
            "受付を終了しました。PDFを出力します。",
            file=discord.File(filename)
        )

        # 5. データ初期化
        self.bot.event_data = None


async def setup(bot):
    await bot.add_cog(FormEnd(bot))
