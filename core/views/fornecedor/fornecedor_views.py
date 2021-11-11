import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from api.models.fornecedor import Fornecedor
from api.models.produto import Produto
from core.models.empresas_models import Alerta
from core.models.parametros_models import Parametro
from core.views.analise.analise_views import graficos_serie
from core.views.analise.vendas import vendas
from core.views.utils.datas import data_mes


@login_required
def excesso_fornecedor(request):
    empresa = request.user.usuario.empresa_id
    df = pd.DataFrame(Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque='EXCESSO'
    ).order_by('cod_fornecedor').values())

    if not df.empty:

        df['vl_excesso'] = df['vl_excesso'].astype(float)

        list_val_cus = ['vl_excesso']

        counts = df['cod_fornecedor'].value_counts()
        counts_df = counts.to_frame().reset_index()
        counts_df.columns=['cod_fornecedor', 'contagem']

        por_fornecedor = df.groupby(['cod_fornecedor', 'fornecedor', 'cod_filial'])[list_val_cus].sum().round(2).reset_index()

        result = pd.merge(por_fornecedor, counts_df, how="right", on=['cod_fornecedor'])
        valor_total_excesso = sum(por_fornecedor['vl_excesso'])

        result = result.drop_duplicates(subset=['cod_fornecedor', 'cod_filial'], keep='first')

        p_fornec = result.to_dict('records')

        context = {
            'fornecedores': p_fornec,
            'valor_total_excesso': valor_total_excesso
        }

        return render(request, 'aplicacao/paginas/fornecedor/excesso_fornec.html', context)
    else:
        return render(request, 'aplicacao/paginas/fornecedor/excesso_fornec.html')


@login_required
def ver_excesso_fornecedor(request, cod_fornecedor, filial):
    empresa = request.user.usuario.empresa_id
    fornec = Fornecedor.objects.get(empresa_id=empresa, cod_fornecedor__exact=cod_fornecedor)
    produtos_fornec = Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque='EXCESSO',
        cod_fornecedor__exact=cod_fornecedor,
        cod_filial=filial
    )

    context = {
        'produtos': produtos_fornec,
        'fornecedor': fornec
    }

    return render(request, 'aplicacao/paginas/fornecedor/ver_excesso_fornec.html', context)


@login_required
def ruptura_fornecedor(request):
    empresa = request.user.usuario.empresa_id
    estado = ["RUPTURA", "PARCIAL"]

    df = pd.DataFrame(Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque__in=estado
    ).order_by('cod_fornecedor').values())

    if not df.empty:

        df['valor'] = df['valor'].astype(float)

        sugestao = df['sugestao'].apply(lambda x: 0 if x <= 0 else x)
        valor = df['valor'].apply(lambda x: 0 if x <= 0 else x)

        df['sugestao'] = sugestao
        df['valor'] = valor

        list_val_cus = ['sugestao', 'valor']

        counts = df['cod_fornecedor'].value_counts()
        counts_df = counts.to_frame().reset_index()
        counts_df.columns = ['cod_fornecedor', 'contagem']

        por_fornecedor = df.groupby(['cod_fornecedor', 'fornecedor', 'cod_filial', 'estado_estoque'])[list_val_cus].sum().round(2).reset_index()

        result = pd.merge(por_fornecedor, counts_df, how="right", on=['cod_fornecedor'])

        result = result.drop_duplicates(subset=['cod_fornecedor', 'cod_filial'], keep='first')

        p_fornec =  result.to_dict('records')

        context = {
            'fornecedores': p_fornec
        }

        return render(request, 'aplicacao/paginas/fornecedor/ruptura_fornec.html', context)
    else:
        return render(request, 'aplicacao/paginas/fornecedor/ruptura_fornec.html')


@login_required
def ver_ruptura_fornecedor(request, cod_fornecedor, filial):
    empresa = request.user.usuario.empresa_id
    fornec = Fornecedor.objects.get(empresa_id=empresa, cod_fornecedor__exact=cod_fornecedor)
    estado = ['RUPTURA', 'PARCIAL']
    produtos_fornec = Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque__in=estado,
        cod_fornecedor__exact=cod_fornecedor,
        cod_filial=filial
    )

    context = {
        'produtos': produtos_fornec,
        'fornecedor': fornec
    }

    return render(request, 'aplicacao/paginas/fornecedor/ver_ruptura_fornec.html', context)


def graficos_alert_fornec(request):
    if request.is_ajax():

        try:
            id_empresa = request.user.usuario.empresa_id

            produto_id = int(request.POST.get('produto'))
            cod_filial = request.POST.get('filial')

            produto = Produto.objects.get(id=produto_id)
            cod_produto = produto.cod_produto

            parametros = Parametro.objects.get(empresa_id=id_empresa)
            periodo = parametros.periodo

            #grafico
            graficos = graficos_serie(id_empresa, cod_produto, cod_filial, periodo)

            # VENDAS MES
            vendas_p, info_produto = vendas(cod_produto, id_empresa, periodo, [cod_filial])

            total_venda = vendas_p
            total_venda['data'] = pd.to_datetime(total_venda['data'])
            total_venda['mes'] = total_venda['data'].map(lambda x: 100 * x.year + x.month)
            total_vendas = total_venda.groupby(['mes', 'cod_filial'])['qt_vendas'].sum().reset_index()
            total_vendas['mes'] = total_vendas['mes'].astype(str)
            df_total_vendas = total_vendas.query('cod_filial == @cod_filial')

            lista_total_vendas = []

            for index, row in df_total_vendas.iterrows():
                mes = row['mes'][4:]
                ano = row['mes'][:4]
                qt = row['qt_vendas']

                dicionario = {
                    'mes': data_mes(mes),
                    'ano': ano,
                    'quantidade': qt
                }
                lista_total_vendas.append(dicionario)

            data = [graficos, lista_total_vendas]

            return JsonResponse({'data': data})

        except Exception as error:
            return JsonResponse({'data':error})

    return JsonResponse({})