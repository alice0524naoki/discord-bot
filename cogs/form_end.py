import discord
from discord.ext import commands
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

        # ★ 1. まず即時応答（Discord のタイムアウト回避）
        await interaction.response.send_message(
            "PDF を生成しています…しばらくお待ちください。"
        )

        # ★ 2. ピン解除（時間がかかる可能性があるので後でOK）
        try:
            msg = await interaction.channel.fetch_message(data["message_id"])
            await msg.unpin()
        except:
            pass

        # ★ 3. PDF 生成（Railway だとここが重い）
        filename = f"{data['title']}_{data['date']}.pdf"
        generate_pdf(data, filename)

        # ★ 4. followup で PDF を送信（これが本番の応答）
        await interaction.followup.send(
            "受付を終了しました。PDFを出力します。",
            file=discord.File(filename)
        )

        # ★ 5. データ初期化
        self.bot.event_data = None


async def setup(bot):
    await bot.add_cog(FormEnd(bot))
