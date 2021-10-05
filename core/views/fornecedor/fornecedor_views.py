import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from api.models.fornecedor import Fornecedor
from api.models.produto import Produto
from core.models.empresas_models import Alerta
from core.models.parametros_models import Parametro
from core.views.analise.analise_views import mapas_serie


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

        result = result.drop_duplicates(subset=['cod_fornecedor', 'cod_filial'], keep='first')

        p_fornec =  result.to_dict('records')

        context = {
            'fornecedores': p_fornec
        }

        return render(request, 'aplicacao/paginas/fornecedor/excesso_fornec.html', context)
    else:
        return render(request, 'aplicacao/paginas/fornecedor/excesso_fornec.html')


@login_required
def ver_excesso_fornecedor(request, cod_fornecedor):
    empresa = request.user.usuario.empresa_id
    fornec = Fornecedor.objects.get(empresa_id=empresa, cod_fornecedor__exact=cod_fornecedor)
    produtos_fornec = Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque='EXCESSO',
        cod_fornecedor__exact=cod_fornecedor
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
def ver_ruptura_fornecedor(request, cod_fornecedor):
    empresa = request.user.usuario.empresa_id
    fornec = Fornecedor.objects.get(empresa_id=empresa, cod_fornecedor__exact=cod_fornecedor)
    estado = ['RUPTURA', 'PARCIAL']
    produtos_fornec = Alerta.objects.filter(
        empresa__id__exact=empresa,
        estado_estoque__in=estado,
        cod_fornecedor__exact=cod_fornecedor
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

            print(produto_id)
            print(cod_filial)

            produto = Produto.objects.get(id=produto_id)
            cod_produto = produto.cod_produto
            print(cod_produto)

            parametros = Parametro.objects.get(empresa_id=id_empresa)
            periodo = parametros.periodo


            mapa = mapas_serie(id_empresa, cod_produto, cod_filial, periodo)
            data = [mapa]

            return JsonResponse({'data': data})

        except Exception as error:
            print(error)

    return JsonResponse({})