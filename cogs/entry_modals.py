import discord
from datetime import datetime

class AddEntryModal(discord.ui.Modal, title="参加者追加（最大5名）"):
    name1 = discord.ui.TextInput(label="名前1", required=True)
    name2 = discord.ui.TextInput(label="名前2（任意）", required=False)
    name3 = discord.ui.TextInput(label="名前3（任意）", required=False)
    name4 = discord.ui.TextInput(label="名前4（任意）", required=False)
    name5 = discord.ui.TextInput(label="名前5（任意）", required=False)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        data = self.bot.event_data

        names = [
            self.name1.value,
            self.name2.value,
            self.name3.value,
            self.name4.value,
            self.name5.value,
        ]

        # 空欄を除外
        names = [n for n in names if n]

        messages = []

        for name in names:
            total = len(data["entries"]) + len(data["pending"]) + 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if total <= data["limit"]:
                entry = {
                    "number": total,
                    "name": name,
                    "user": interaction.user.name,
                    "timestamp": now,
                }
                data["entries"].append(entry)
                messages.append(f"{entry['number']} {entry['name']} を登録しました。")
            else:
                pending = {
                    "name": name,
                    "user": interaction.user.name,
                    "timestamp": now,
                }
                data["pending"].append(pending)
                messages.append(f"仮登録 {pending['name']} を登録しました。")

        # ★ 修正ポイント：ephemeral=False（全員に見える）
        await interaction.response.send_message("\n".join(messages))


class ChangeEntryModal(discord.ui.Modal, title="参加者変更"):
    name = discord.ui.TextInput(label="変更前の名前", required=True)
    new_name = discord.ui.TextInput(label="変更後の名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        old = self.name.value
        new = self.new_name.value

        for e in data["entries"]:
            if e["name"] == old:
                e["name"] = new
                await interaction.response.send_message(f"{old} を {new} に変更しました。")
                return

        await interaction.response.send_message("該当する名前が見つかりませんでした。")


class DeleteEntryModal(discord.ui.Modal, title="参加者削除"):
    name = discord.ui.TextInput(label="削除する名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        name = self.name.value

        for e in data["entries"]:
            if e["name"] == name:
                data["entries"].remove(e)
                await interaction.response.send_message(f"{name} を削除しました。")
                return

        await interaction.response.send_message("該当する名前が見つかりませんでした。")


async def setup(bot):
    pass  # Modal だけなので add_cog は不要
