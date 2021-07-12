from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
import os
import io
from reportlab.lib.utils import ImageReader



def milimetro(valor):
    return valor/0.352777

def pdf_alerta_gerar(request):


    buffer = io.BytesIO()


    logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')

    p = canvas.Canvas(buffer, pagesize=A4)
    p.drawImage(logo, milimetro(10), milimetro(220))
    p.drawString(milimetro(100), milimetro(100), "Hello world.")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.seek(0)
    # buffer.close()



    return pdf
    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')