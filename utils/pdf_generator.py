from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_expense_pdf(expenses, filename):

    pdf = canvas.Canvas(filename, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 750, "Expense Report")

    pdf.setFont("Helvetica", 12)

    y = 710

    pdf.drawString(50, y, "Category")
    pdf.drawString(180, y, "Amount")
    pdf.drawString(280, y, "Payment")
    pdf.drawString(400, y, "Date")

    y -= 25

    for expense in expenses:

        pdf.drawString(50, y, str(expense[0]))
        pdf.drawString(180, y, f"₹ {expense[1]}")
        pdf.drawString(280, y, str(expense[2]))
        pdf.drawString(400, y, str(expense[3]))

        y -= 20

        if y < 50:

            pdf.showPage()

            y = 750

    pdf.save()