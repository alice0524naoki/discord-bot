import discord
from discord.ext import commands
from .entry_modals import AddEntryModal, ChangeEntryModal, DeleteEntryModal

class EntryButtonsView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="追加", style=discord.ButtonStyle.green)
    async def add_button(self, interaction, button):
        await interaction.response.send_modal(AddEntryModal(self.bot))

    @discord.ui.button(label="変更", style=discord.ButtonStyle.blurple)
    async def change_button(self, interaction, button):
        await interaction.response.send_modal(ChangeEntryModal(self.bot))

    @discord.ui.button(label="削除", style=discord.ButtonStyle.red)
    async def delete_button(self, interaction, button):
        await interaction.response.send_modal(DeleteEntryModal(self.bot))


async def setup(bot):
    pass
