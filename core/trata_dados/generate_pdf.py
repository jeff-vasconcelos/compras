from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
from core.models.pedidos_models import *
from core.models.empresas_models import *
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
    p.drawImage(logo, mm(80), mm(270), height=40, width=130)
    p.drawString(mm(70), mm(260), f'PEDIDO INSIGHT {hoje}', charSpace=2)

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


def pdf_excesso(request):
    id_empresa = request.user.usuario.empresa_id
    estado = "EXCESSO"

    itens = Alerta.objects.filter(empresa__id=id_empresa, estado_estoque=estado)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Relatório-Excesso.pdf"'
    # response['Content-Disposition'] = 'attachment: filename="PedidoInsight.pdf"'

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.setTitle('Insight')
    p.drawImage(logo, mm(80), mm(270), height=40, width=130)
    p.drawString(mm(55), mm(260), f'RELATÓRIO DE EXCESSO {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(20), mm(245), "PRODUTO")
    p.drawString(mm(100), mm(245), "ESTOQUE")
    p.drawString(mm(120), mm(245), "QUANTIDADE")
    p.drawString(mm(145), mm(245), "VALOR R$")
    p.drawString(mm(166), mm(245), "DDE")
    p.drawString(mm(180), mm(245), "FORNECEDOR")

    p.line(mm(6), mm(243), mm(203), mm(243))

    contador_y = 243

    for prod in itens:
        contador_y = contador_y - 5
        p.drawString(mm(8), mm(contador_y), f"{prod.cod_filial}")
        p.drawString(mm(21), mm(contador_y), f"{prod.cod_produto} - {prod.desc_produto}")
        p.drawString(mm(101), mm(contador_y), f"{prod.estoque}")
        p.drawString(mm(121), mm(contador_y), f"{prod.qt_excesso}")
        p.drawString(mm(146), mm(contador_y), f"{prod.vl_excesso}")
        p.drawString(mm(167), mm(contador_y), f"{prod.campo_um}")
        p.drawString(mm(181), mm(contador_y), f"{prod.cod_fornecedor}")

        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def pdf_parcial(request):
    id_empresa = request.user.usuario.empresa_id
    estado = "PARCIAL"

    itens = Alerta.objects.filter(empresa__id=id_empresa, estado_estoque=estado)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Relatório-Excesso.pdf"'
    # response['Content-Disposition'] = 'attachment: filename="PedidoInsight.pdf"'

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.setTitle('Insight')
    p.drawImage(logo, mm(80), mm(270), height=40, width=130)
    p.drawString(mm(42), mm(260), f'RELATÓRIO DE RUPTURA PARCIAL {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(20), mm(245), "PRODUTO")
    p.drawString(mm(100), mm(245), "ESTOQUE")
    p.drawString(mm(120), mm(245), "SUGESTÃO")
    p.drawString(mm(145), mm(245), "VALOR R$")
    p.drawString(mm(166), mm(245), "DDE")
    p.drawString(mm(180), mm(245), "FORNECEDOR")

    p.line(mm(6), mm(243), mm(203), mm(243))

    contador_y = 243

    for prod in itens:
        contador_y = contador_y - 5
        p.drawString(mm(8), mm(contador_y), f"{prod.cod_filial}")
        p.drawString(mm(21), mm(contador_y), f"{prod.cod_produto} - {prod.desc_produto}")
        p.drawString(mm(101), mm(contador_y), f"{prod.estoque}")
        p.drawString(mm(121), mm(contador_y), f"{prod.sugestao}")
        p.drawString(mm(146), mm(contador_y), f"{prod.valor}")
        p.drawString(mm(167), mm(contador_y), f"{prod.campo_um}")
        p.drawString(mm(181), mm(contador_y), f"{prod.cod_fornecedor}")

        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def pdf_ruptura(request):
    id_empresa = request.user.usuario.empresa_id
    estado = "RUPTURA"

    itens = Alerta.objects.filter(empresa__id=id_empresa, estado_estoque=estado)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Relatório-Excesso.pdf"'
    # response['Content-Disposition'] = 'attachment: filename="PedidoInsight.pdf"'

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.setTitle('Insight')
    p.drawImage(logo, mm(80), mm(270), height=40, width=130)
    p.drawString(mm(54), mm(260), f'RELATÓRIO DE RUPTURA {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(20), mm(245), "PRODUTO")
    p.drawString(mm(100), mm(245), "ESTOQUE")
    p.drawString(mm(120), mm(245), "SUGESTÃO")
    p.drawString(mm(145), mm(245), "VALOR R$")
    p.drawString(mm(166), mm(245), "DDE")
    p.drawString(mm(180), mm(245), "FORNECEDOR")

    p.line(mm(6), mm(243), mm(203), mm(243))

    contador_y = 243

    for prod in itens:
        contador_y = contador_y - 5
        p.drawString(mm(8), mm(contador_y), f"{prod.cod_filial}")
        p.drawString(mm(21), mm(contador_y), f"{prod.cod_produto} - {prod.desc_produto}")
        p.drawString(mm(101), mm(contador_y), f"{prod.estoque}")
        p.drawString(mm(121), mm(contador_y), f"{prod.sugestao}")
        p.drawString(mm(146), mm(contador_y), f"{prod.valor}")
        p.drawString(mm(167), mm(contador_y), f"{prod.campo_um}")
        p.drawString(mm(181), mm(contador_y), f"{prod.cod_fornecedor}")

        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response