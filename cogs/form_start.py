import discord
from discord.ext import commands
from .entry_buttons import EntryButtonsView

class StartFormModal(discord.ui.Modal, title="受付フォーム設定"):
    title_input = discord.ui.TextInput(label="タイトル", required=True)
    date_input = discord.ui.TextInput(label="開催日", required=True)
    limit_input = discord.ui.TextInput(label="定員数", required=True)
    allow_over_input = discord.ui.TextInput(label="上限超過可否（はい/いいえ）", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        title = self.title_input.value
        date = self.date_input.value
        limit = int(self.limit_input.value)
        allow_over = self.allow_over_input.value.lower() in ["はい", "yes", "true"]

        self.bot.event_data = {
            "title": title,
            "date": date,
            "limit": limit,
            "allow_over": allow_over,
            "entries": [],
            "pending": [],
            "message_id": None,
            "channel_id": interaction.channel.id,
        }

        view = EntryButtonsView(self.bot)
        msg = await interaction.channel.send(
            f"**{title}** の受付を開始しました\n"
            f"開催日: {date}　定員: {limit}",
            view=view
        )

        self.bot.event_data["message_id"] = msg.id

        # ★ これが正解：何も表示せずに正常終了
        await interaction.response.defer(ephemeral=True)


class FormStart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="form_start", description="受付フォームを開始します")
    async def form_start(self, interaction: discord.Interaction):

        if self.bot.event_data is not None:
            await interaction.response.send_message(
                "すでに受付が開始されています。\n終了するには /form_end を実行してください。",
                ephemeral=True
            )
            return

        modal = StartFormModal(self.bot)
        await interaction.response.send_modal(modal)


async def setup(bot):
    await bot.add_cog(FormStart(bot))
