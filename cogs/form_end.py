import discord
from discord.ext import commands
import os
from utils.pdf_generator import generate_pdf


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

        # ★ 最初に応答（3秒以内に必須）
        await interaction.response.defer()

        # ピン解除（ピン留めを使わないなら削除してもOK）
        try:
            msg = await interaction.channel.fetch_message(data["message_id"])
            await msg.unpin()
        except:
            pass

        # PDF生成
        filename = f"{data['title']}_{data['date']}.pdf"
        generate_pdf(data, filename)

        abs_path = os.path.abspath(filename)

        # followup で PDF を送信
        await interaction.followup.send(
            "受付を終了しました。PDFを出力します。",
            file=discord.File(abs_path)
        )

        # データ初期化
        self.bot.event_data = None


async def setup(bot):
    await bot.add_cog(FormEnd(bot))
