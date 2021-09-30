import xlwt
from django.http import HttpResponse


def export_xls(request) -> object:

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="insight.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Pedido Insight')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # COLUNAS DA PLANILHA
    columns = ['cod_produto', 'preco', 'quantidade']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    # GET PEDIDO SESSÃO
    pedido = request.session.get('pedido_produto', [])
    lista = []


    # SALVAR ITENS DO PEDIDO
    for value in pedido.values():
        temp = value

        del [temp['ped_cod_filial']]
        del [temp['ped_produto_nome']]
        del [temp['ped_produto_id']]

        lista.append(temp)

    # LINHAS DA PLANILHA
    for row in lista:
        valores = row.values()
        l_valores = list(valores)
        row_num += 1

        for col_num in range(len(l_valores)):
            ws.write(row_num, col_num, l_valores[col_num], font_style)

    wb.save(response)

    del request.session['pedido_produto']
    request.session.save()

    return response