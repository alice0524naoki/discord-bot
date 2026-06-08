from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"{data['title']} ({data['date']}) 受付結果")

    y = height - 80
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "【本登録：名前昇順】")
    y -= 20

    entries = sorted(data["entries"], key=lambda x: x["name"])
    c.setFont("Helvetica", 10)

    no = 1
    for e in entries:
        c.drawString(50, y, f"{no}")
        c.drawString(90, y, f"{e['number']}")
        c.drawString(150, y, e["name"])
        c.drawString(250, y, e["user"])
        c.drawString(350, y, e["timestamp"])
        y -= 15
        no += 1

    c.showPage()
    y = height - 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "【仮登録：入力順】")
    y -= 20

    c.setFont("Helvetica", 10)
    no = 1
    for p in data["pending"]:
        c.drawString(50, y, f"{no}")
        c.drawString(150, y, p["name"])
        c.drawString(250, y, p["user"])
        c.drawString(350, y, p["timestamp"])
        y -= 15
        no += 1

    c.save()
