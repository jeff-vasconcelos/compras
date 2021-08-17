from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def mm(valor):
    return valor / 0.352777


def pdf_pedidos_insight(request):
    contexto = request.session.get('pedido_produto', [])
    lista = []

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.drawImage(logo, mm(83), mm(270), height=40, width=130)
    p.drawString(mm(70), mm(255), f'PEDIDO INSIGHT {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(25), mm(245), "PRODUTO")
    p.drawString(mm(120), mm(245), "PREÇO DE COMPRA")
    p.drawString(mm(160), mm(245), "QUANTIDADE")

    p.line(mm(6), mm(243), mm(203), mm(243))

    if not contexto:
        res = "FALSE"
        return JsonResponse({'data': res})

    else:
        for value in contexto.values():
            temp = value
            preco = temp['ped_pr_compra']
            preco_form = locale.currency(preco, grouping=True)
            temp.update({'ped_pr_compra': preco_form})
            lista.append(temp)

        contador_y = 243
        for prod in lista:
            contador_y = contador_y - 5
            p.drawString(mm(8), mm(contador_y), f"{prod['ped_cod_filial']}")
            p.drawString(mm(26), mm(contador_y), f"{prod['ped_produto_cod']} - {prod['ped_produto_nome']}")
            p.drawString(mm(121), mm(contador_y), f"{prod['ped_pr_compra']}")
            p.drawString(mm(161), mm(contador_y), f"{prod['ped_qt_digitada']}")

            if contador_y <= 10:
                p.showPage()
                p.setFont('Times-Roman', 8)
                contador_y = 285

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, filename='PedidoInsight.pdf')
