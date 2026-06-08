import discord
from datetime import datetime

# -----------------------------
# 参加者追加（1名）
# -----------------------------
class AddEntryModal(discord.ui.Modal, title="参加者追加"):
    name = discord.ui.TextInput(label="名前", required=True)
    nickname = discord.ui.TextInput(label="ニックネーム（任意）", required=False)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        data = self.bot.event_data

        name = self.name.value
        nickname = self.nickname.value or None

        total = len(data["entries"]) + len(data["pending"]) + 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry_data = {
            "name": name,
            "nickname": nickname,
            "user": interaction.user.display_name,  # ← Discord の表示名を保存
            "timestamp": now,
        }

        if total <= data["limit"]:
            entry_data["number"] = total
            data["entries"].append(entry_data)
            msg = f"{total} {name} を登録しました。"
        else:
            data["pending"].append(entry_data)
            msg = f"仮登録 {name} を登録しました。"

        await interaction.response.send_message(msg)


# -----------------------------
# 参加者変更
# -----------------------------
class ChangeEntryModal(discord.ui.Modal, title="参加者変更"):
    old_name = discord.ui.TextInput(label="変更前の名前", required=True)
    new_name = discord.ui.TextInput(label="変更後の名前", required=True)
    new_nickname = discord.ui.TextInput(label="新しいニックネーム（任意）", required=False)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        old = self.old_name.value
        new = self.new_name.value
        new_nick = self.new_nickname.value or None

        # 本登録
        for e in data["entries"]:
            if e["name"] == old:
                e["name"] = new
                e["nickname"] = new_nick
                await interaction.response.send_message(f"{old} を {new} に変更しました。")
                return

        # 仮登録
        for p in data["pending"]:
            if p["name"] == old:
                p["name"] = new
                p["nickname"] = new_nick
                await interaction.response.send_message(f"{old}（仮登録）を {new} に変更しました。")
                return

        await interaction.response.send_message("該当する名前が見つかりませんでした。")


# -----------------------------
# 参加者削除
# -----------------------------
class DeleteEntryModal(discord.ui.Modal, title="参加者削除"):
    name = discord.ui.TextInput(label="削除する名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data
        name = self.name.value

        # 本登録
        for e in data["entries"]:
            if e["name"] == name:
                data["entries"].remove(e)
                await interaction.response.send_message(f"{name} を削除しました。")
                return

        # 仮登録
        for p in data["pending"]:
            if p["name"] == name:
                data["pending"].remove(p)
                await interaction.response.send_message(f"{name}（仮登録）を削除しました。")
                return

        await interaction.response.send_message("該当する名前が見つかりませんでした。")


async def setup(bot):
    pass
