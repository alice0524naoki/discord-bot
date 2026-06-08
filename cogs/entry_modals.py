import discord
from datetime import datetime

# -----------------------------
# 参加者追加（最大5名）
# -----------------------------
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
        names = [n for n in names if n]

        messages = []

        for name in names:
            total = len(data["entries"]) + len(data["pending"]) + 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            entry_data = {
                "name": name,
                "user": interaction.user.display_name,
                "timestamp": now,
            }

            if total <= data["limit"]:
                entry_data["number"] = total
                data["entries"].append(entry_data)
                messages.append(f"{total} {name} を登録しました。")
            else:
                data["pending"].append(entry_data)
                messages.append(f"仮登録 {name} を登録しました。")

        await interaction.response.send_message("\n".join(messages))


# -----------------------------
# 参加者変更（本登録のみ）
# -----------------------------
class ChangeEntryModal(discord.ui.Modal, title="参加者変更"):
    old_number = discord.ui.TextInput(label="変更前の番号", required=True)
    old_name = discord.ui.TextInput(label="変更前の名前", required=True)
    new_name = discord.ui.TextInput(label="変更後の名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data

        # 仮登録は番号が無いので変更不可
        if not self.old_number.value.isdigit():
            await interaction.response.send_message("仮登録は変更できません。")
            return

        old_num = int(self.old_number.value)
        old_name = self.old_name.value
        new_name = self.new_name.value

        for e in data["entries"]:
            if e["number"] == old_num and e["name"] == old_name:
                e["name"] = new_name
                await interaction.response.send_message(
                    f"{old_num} {old_name} を {new_name} に変更しました。"
                )
                return

        await interaction.response.send_message("該当する本登録の参加者が見つかりませんでした。")


# -----------------------------
# 参加者削除（本登録 or 仮登録）
# -----------------------------
class DeleteEntryModal(discord.ui.Modal, title="参加者削除"):
    number = discord.ui.TextInput(label="削除する番号（仮登録の場合は「仮登録」と入力）", required=True)
    name = discord.ui.TextInput(label="削除する名前", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction):
        data = self.bot.event_data

        num_text = self.number.value
        name = self.name.value

        # -------------------------
        # 仮登録の削除
        # -------------------------
        if num_text == "仮登録":
            for p in data["pending"]:
                if p["name"] == name:
                    data["pending"].remove(p)
                    await interaction.response.send_message(
                        f"仮登録 {name} を削除しました。"
                    )
                    return

            await interaction.response.send_message("該当する仮登録が見つかりませんでした。")
            return

        # -------------------------
        # 本登録の削除
        # -------------------------
        if num_text.isdigit():
            num = int(num_text)
            for e in data["entries"]:
                if e["number"] == num and e["name"] == name:
                    data["entries"].remove(e)
                    await interaction.response.send_message(
                        f"{num} {name} を削除しました。"
                    )
                    return

            await interaction.response.send_message("該当する本登録の参加者が見つかりませんでした。")
            return

        # -------------------------
        # それ以外の入力
        # -------------------------
        await interaction.response.send_message("番号には数字か「仮登録」を入力してください。")


async def setup(bot):
    pass
