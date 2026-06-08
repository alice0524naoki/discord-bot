import discord
from datetime import datetime

class AddEntryModal(discord.ui.Modal, title="参加者追加"):
    name_input = discord.ui.TextInput(label="名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        name = self.name_input.value
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total = len(data["entries"]) + len(data["pending"]) + 1

        if total <= data["limit"]:
            entry = {
                "number": total,
                "name": name,
                "user": interaction.user.name,
                "timestamp": now,
            }
            data["entries"].append(entry)
            await interaction.response.send_message(f"{entry['number']} {entry['name']} を登録しました。")
        else:
            pending = {
                "name": name,
                "user": interaction.user.name,
                "timestamp": now,
            }
            data["pending"].append(pending)
            await interaction.response.send_message(f"仮登録 {pending['name']} を登録しました。")


class ChangeEntryModal(discord.ui.Modal, title="参加者変更"):
    old_number = discord.ui.TextInput(label="旧ナンバー", required=True)
    old_name = discord.ui.TextInput(label="旧名前", required=True)
    new_name = discord.ui.TextInput(label="新しい名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        old_num = int(self.old_number.value)
        old_name = self.old_name.value
        new_name = self.new_name.value

        for entry in data["entries"]:
            if entry["number"] == old_num and entry["name"] == old_name:
                entry["name"] = new_name
                entry["user"] = interaction.user.name
                entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await interaction.response.send_message(f"{old_num} を {new_name} に変更しました。")
                return

        await interaction.response.send_message("該当者が見つかりません。", ephemeral=True)


class DeleteEntryModal(discord.ui.Modal, title="参加者削除"):
    old_number = discord.ui.TextInput(label="旧ナンバー", required=True)
    old_name = discord.ui.TextInput(label="旧名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        old_num = int(self.old_number.value)
        old_name = self.old_name.value

        new_entries = []
        removed = False

        for entry in data["entries"]:
            if entry["number"] == old_num and entry["name"] == old_name:
                removed = True
                continue
            new_entries.append(entry)

        data["entries"] = new_entries

        if removed:
            await interaction.response.send_message(f"{old_num} {old_name} を削除しました。")
        else:
            await interaction.response.send_message("該当者が見つかりません。", ephemeral=True)
async def setup(bot):
    pass
