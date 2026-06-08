from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 日本語フォントの登録（fonts/IPAexGothic.ttf を配置してください）
pdfmetrics.registerFont(TTFont("IPAexGothic", "fonts/IPAexGothic.ttf"))

def generate_pdf(data, filename):
    print(f"[PDF] 生成開始: {filename}")
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # タイトル部分
        c.setFont("IPAexGothic", 16)
        c.drawString(
            50,
            height - 50,
            f"{data['title']} ({data['date_display']}) 受付結果"
        )

        # --- 本登録ページ ---
        y = height - 80
        c.setFont("IPAexGothic", 12)
        c.drawString(50, y, "【本登録：名前昇順】")
        y -= 20

        # ニックネーム優先でソート
        entries = sorted(
            data["entries"],
            key=lambda x: x.get("nickname") or x["name"]
        )

        c.setFont("IPAexGothic", 10)
        no = 1
        for e in entries:
            display_name = e.get("nickname") or e["name"]
            c.drawString(50, y, f"{no}")
            c.drawString(90, y, f"{e['number']}")
            c.drawString(150, y, display_name)
            c.drawString(250, y, e["user"])
            c.drawString(350, y, e["timestamp"])
            y -= 15
            no += 1

        # --- 仮登録ページ（pending がある場合のみ） ---
        if data["pending"]:
            c.showPage()
            y = height - 50
            c.setFont("IPAexGothic", 12)
            c.drawString(50, y, "【仮登録：入力順】")
            y -= 20

            c.setFont("IPAexGothic", 10)
            no = 1
            for p in data["pending"]:
                display_name = p.get("nickname") or p["name"]
                c.drawString(50, y, f"{no}")
                c.drawString(150, y, display_name)
                c.drawString(250, y, p["user"])
                c.drawString(350, y, p["timestamp"])
                y -= 15
                no += 1

        # 保存
        c.save()

        # 生成確認
        if os.path.exists(filename):
            print(f"[PDF] 生成成功: {filename}")
        else:
            print(f"[PDF] 生成失敗: ファイルが存在しません {filename}")

    except Exception as e:
        print(f"[PDF] 例外発生: {e}")
