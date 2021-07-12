from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
import os
import io
from reportlab.lib.utils import ImageReader



def milimetro(valor):
    return valor/0.352777

def pdf_alerta_gerar(request):
    print("funcionou aqui")
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawImage(logo, milimetro(10), milimetro(220))
    p.drawString(milimetro(100), milimetro(100), "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')