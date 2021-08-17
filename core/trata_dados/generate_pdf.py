from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
from core.models.pedidos_models import *
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def mm(valor):
    return valor / 0.352777


def pdf_pedidos_insight(request, pk):
    pedido = PedidoInsight.objects.get(id=pk)
    itens = PedidoInsightItens.objects.filter(pedido=pedido.pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="PedidoInsight.pdf"'
    #response['Content-Disposition'] = 'attachment: filename="PedidoInsight.pdf"'

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.setTitle('Insight')
    p.drawImage(logo, mm(83), mm(270), height=40, width=130)
    p.drawString(mm(70), mm(255), f'PEDIDO INSIGHT {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(25), mm(245), "PRODUTO")
    p.drawString(mm(120), mm(245), "PREÇO DE COMPRA")
    p.drawString(mm(160), mm(245), "QUANTIDADE")

    p.line(mm(6), mm(243), mm(203), mm(243))

    contador_y = 243

    for prod in itens:
        contador_y = contador_y - 5
        p.drawString(mm(8), mm(contador_y), f"{prod.cod_filial}")
        p.drawString(mm(26), mm(contador_y), f"{prod.cod_produto} - {prod.desc_produto}")
        p.drawString(mm(121), mm(contador_y), f"{prod.preco}")
        p.drawString(mm(161), mm(contador_y), f"{prod.quantidade}")

        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    # buffer.seek(0)
    # return FileResponse(buffer, filename='PedidoInsight.pdf')
    return response