import locale

from core.alertas.curva_abc_alertas import abc
from core.alertas.verificador import get_fornecedores
from core.models.empresas_models import Empresa
from core.models.parametros_models import GraficoCurva, DadosEstoque, GraficoFaturamento, Parametro

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def processa_grafico_um(produtos):
    global status, total_normal_b, total_excesso_b, total_parcial_b, total_ruptura_b

    lista_normal = []
    lista_excesso = []
    lista_parcial = []
    lista_ruptura = []

    curva = []

    for i in produtos:
        if i['condicao_estoque'] == "NORMAL":
            i['valor_normal'] = i['estoque'] * i['custo']

            i['valor_excesso'] = 0
            i['valor_parcial'] = 0
            i['valor_ruptura'] = 0

            curva.append(i)

        elif i['condicao_estoque'] == "EXCESSO":
            i['valor_excesso'] = i['qt_excesso'] * i['custo']
            i['valor_normal'] = 0
            i['valor_parcial'] = 0
            i['valor_ruptura'] = 0

            curva.append(i)

        elif i['condicao_estoque'] == "PARCIAL":
            i['valor_parcial'] = i['estoque'] * i['custo']

            i['valor_excesso'] = 0
            i['valor_normal'] = 0
            i['valor_ruptura'] = 0

            curva.append(i)

        elif i['condicao_estoque'] == "RUPTURA":
            i['valor_ruptura'] = i['estoque'] * i['custo']

            i['valor_excesso'] = 0
            i['valor_normal'] = 0
            i['valor_parcial'] = 0

            curva.append(i)

    #CURVA A
    for a in curva:
        if a['curva'] == 'A':
            lista_normal.append(a['valor_normal'])
            lista_excesso.append(a['valor_excesso'])
            lista_parcial.append(a['valor_parcial'])
            lista_ruptura.append(a['valor_ruptura'])


    total_normal_a = sum(lista_normal)
    total_excesso_a = sum(lista_excesso)
    total_parcial_a = sum(lista_parcial)
    total_ruptura_a = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()


    curva_a = {
        'curva': 'A',
        'total_normal':total_normal_a,
        'total_excesso':total_excesso_a,
        'total_parcial':total_parcial_a,
        'total_ruptura':total_ruptura_a
    }

    # CURVA B
    for b in curva:
        if b['curva'] == 'B':
            lista_normal.append(b['valor_normal'])
            lista_excesso.append(b['valor_excesso'])
            lista_parcial.append(b['valor_parcial'])
            lista_ruptura.append(b['valor_ruptura'])

    total_normal_b = sum(lista_normal)
    total_excesso_b = sum(lista_excesso)
    total_parcial_b = sum(lista_parcial)
    total_ruptura_b = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_b = {
        'curva': 'B',
        'total_normal': total_normal_b,
        'total_excesso': total_excesso_b,
        'total_parcial': total_parcial_b,
        'total_ruptura': total_ruptura_b
    }

    # CURVA C
    for c in curva:
        if c['curva'] == 'C':
            lista_normal.append(c['valor_normal'])
            lista_excesso.append(c['valor_excesso'])
            lista_parcial.append(c['valor_parcial'])
            lista_ruptura.append(c['valor_ruptura'])

    total_normal_c = sum(lista_normal)
    total_excesso_c = sum(lista_excesso)
    total_parcial_c = sum(lista_parcial)
    total_ruptura_c = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_c = {
        'curva': 'C',
        'total_normal': total_normal_c,
        'total_excesso': total_excesso_c,
        'total_parcial': total_parcial_c,
        'total_ruptura': total_ruptura_c
    }

    # CURVA D
    for d in curva:
        if d['curva'] == 'D':
            lista_normal.append(d['valor_normal'])
            lista_excesso.append(d['valor_excesso'])
            lista_parcial.append(d['valor_parcial'])
            lista_ruptura.append(d['valor_ruptura'])

    total_normal_d = sum(lista_normal)
    total_excesso_d = sum(lista_excesso)
    total_parcial_d = sum(lista_parcial)
    total_ruptura_d = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_d = {
        'curva': 'D',
        'total_normal': total_normal_d,
        'total_excesso': total_excesso_d,
        'total_parcial': total_parcial_d,
        'total_ruptura': total_ruptura_d
    }

    # CURVA E
    for e in curva:
        if e['curva'] == 'E':
            lista_normal.append(e['valor_normal'])
            lista_excesso.append(e['valor_excesso'])
            lista_parcial.append(e['valor_parcial'])
            lista_ruptura.append(e['valor_ruptura'])

    total_normal_e = sum(lista_normal)
    total_excesso_e = sum(lista_excesso)
    total_parcial_e = sum(lista_parcial)
    total_ruptura_e = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_e = {
        'curva': 'E',
        'total_normal': total_normal_e,
        'total_excesso': total_excesso_e,
        'total_parcial': total_parcial_e,
        'total_ruptura': total_ruptura_e
    }

    lista_status = [curva_a, curva_b, curva_c, curva_d, curva_e]

    return lista_status


def db_grafico_um(id_empresa, produtos):

    itens = GraficoCurva.objects.all().filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if itens:
        itens.delete()

    for i in produtos:
        normal = i['total_normal']
        excesso = i['total_excesso']
        parcial = i['total_parcial']
        ruptura = i['total_ruptura']

        total = normal + excesso + parcial

        b = GraficoCurva.objects.create(
            curva=i['curva'],
            normal= round(normal, 2),
            parcial= round(parcial, 2),
            excesso= round(excesso, 2),
            total= round(total, 2),
            empresa=empresa
        )

        b.save()


def db_grafico_dois(id_empresa):

    global total_a, total_b, total_c, total_d, total_e
    lista_fornecedor = get_fornecedores(id_empresa)
    empresa = Empresa.objects.get(id=id_empresa)
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    itens_faturamento = GraficoFaturamento.objects.all().filter(empresa__id__exact=id_empresa)

    curva = abc(lista_fornecedor, id_empresa, parametros.periodo)

    la, lb, lc, ld, le = [], [], [], [], []

    for index, row in curva.iterrows():

        if row['curva'] == 'A':
            la.append(float(row['vl_total_vendido']))

        if row['curva'] == 'B':
            lb.append(float(row['vl_total_vendido']))

        if row['curva'] == 'C':
            lc.append(float(row['vl_total_vendido']))

        if row['curva'] == 'D':
            ld.append(float(row['vl_total_vendido']))

        if row['curva'] == 'E':
            le.append(float(row['vl_total_vendido']))

    # curva A
    if len(la) != 0:
        total_a = sum(la)
    else:
        total_a = 0

    curva_a = {
        'curva': "A",
        'total': total_a
    }

    # curva B
    if len(lb) != 0:
        total_b = sum(lb)
    else:
        total_b = 0

    curva_b = {
        'curva': "B",
        'total': total_b
    }

    # curva C
    if len(lc) != 0:
        total_c = sum(lc)
    else:
        total_c = 0
    curva_c = {
        'curva': "C",
        'total': total_c
    }


    # curva D
    if len(ld) != 0:
        total_d = sum(ld)
    else:
        total_d = 0
    curva_d = {
        'curva': "D",
        'total': total_d
    }


    #curva E
    if len(le) != 0:
        total_e = sum(le)
    else:
        total_e = 0
    curva_e = {
        'curva': "E",
        'total': total_e
    }

    curvas = [curva_a, curva_b, curva_c, curva_d, curva_e]

    if itens_faturamento:
        itens_faturamento.delete()

    for c in curvas:

        r = GraficoFaturamento.objects.create(
            curva=c['curva'],
            total=c['total'],
            empresa=empresa
        )
        r.save()


def dados_estoque_home(produtos):

    list_a = []
    list_b = []
    list_c = []
    list_d = []
    list_e = []

    for x in produtos:
        if x['curva'] == "A":
            list_a.append(x)

        elif x['curva'] == "B":
            list_b.append(x)

        elif x['curva'] == "C":
            list_c.append(x)

        elif x['curva'] == "D":
            list_d.append(x)

        elif x['curva'] == "E":
            list_e.append(x)

    #CURVA A
    sku_a = 0
    cont_normal_a = 0
    cont_excesso_a = 0
    cont_parcial_a = 0
    cont_ruptura_a = 0

    for a in list_a:
        sku_a += 1

        if a['condicao_estoque'] == "NORMAL":
            cont_normal_a += 1

        elif a['condicao_estoque'] == "EXCESSO":
            cont_excesso_a += 1

        elif a['condicao_estoque'] == "PARCIAL":
            cont_parcial_a += 1

        elif a['condicao_estoque'] == "RUPTURA":
            cont_ruptura_a += 1

    curva_a = {
        'curva': 'A',
        'skus': sku_a,
        'normal': cont_normal_a,
        'excesso': cont_excesso_a,
        'parcial': cont_parcial_a,
        'ruptura': cont_ruptura_a
    }

    #CURVA B
    sku_b = 0
    cont_normal_b = 0
    cont_excesso_b = 0
    cont_parcial_b = 0
    cont_ruptura_b = 0

    for b in list_b:
        sku_b += 1

        if b['condicao_estoque'] == "NORMAL":
            cont_normal_b += 1

        elif b['condicao_estoque'] == "EXCESSO":
            cont_excesso_b += 1

        elif b['condicao_estoque'] == "PARCIAL":
            cont_parcial_b += 1

        elif b['condicao_estoque'] == "RUPTURA":
            cont_ruptura_b += 1

    curva_b = {
        'curva': 'B',
        'skus': sku_b,
        'normal': cont_normal_b,
        'excesso': cont_excesso_b,
        'parcial': cont_parcial_b,
        'ruptura': cont_ruptura_b
    }

    #CURVA C
    sku_c = 0
    cont_normal_c = 0
    cont_excesso_c = 0
    cont_parcial_c = 0
    cont_ruptura_c = 0

    for c in list_c:
        sku_c += 1

        if c['condicao_estoque'] == "NORMAL":
            cont_normal_c += 1

        elif c['condicao_estoque'] == "EXCESSO":
            cont_excesso_c += 1

        elif c['condicao_estoque'] == "PARCIAL":
            cont_parcial_c += 1

        elif c['condicao_estoque'] == "RUPTURA":
            cont_ruptura_c += 1

    curva_c = {
        'curva': 'C',
        'skus': sku_c,
        'normal': cont_normal_c,
        'excesso': cont_excesso_c,
        'parcial': cont_parcial_c,
        'ruptura': cont_ruptura_c
    }

    #CURVA D
    sku_d = 0
    cont_normal_d = 0
    cont_excesso_d = 0
    cont_parcial_d = 0
    cont_ruptura_d = 0

    for d in list_d:
        sku_d += 1

        if d['condicao_estoque'] == "NORMAL":
            cont_normal_d += 1

        elif d['condicao_estoque'] == "EXCESSO":
            cont_excesso_d += 1

        elif d['condicao_estoque'] == "PARCIAL":
            cont_parcial_d += 1

        elif d['condicao_estoque'] == "RUPTURA":
            cont_ruptura_d += 1

    curva_d = {
        'curva': 'D',
        'skus': sku_d,
        'normal': cont_normal_d,
        'excesso': cont_excesso_d,
        'parcial': cont_parcial_d,
        'ruptura': cont_ruptura_d
    }

    #CURVA E
    sku_e = 0
    cont_normal_e = 0
    cont_excesso_e = 0
    cont_parcial_e = 0
    cont_ruptura_e = 0

    for e in list_e:
        sku_e = sku_e + 1

        if e['condicao_estoque'] == "NORMAL":
            cont_normal_e += 1

        elif e['condicao_estoque'] == "EXCESSO":
            cont_excesso_e += 1

        elif e['condicao_estoque'] == "PARCIAL":
            cont_parcial_e += 1

        elif e['condicao_estoque'] == "RUPTURA":
            cont_ruptura_e += 1

    curva_e = {
        'curva': 'E',
        'skus': sku_e,
        'normal': cont_normal_e,
        'excesso': cont_excesso_e,
        'parcial': cont_parcial_e,
        'ruptura': cont_ruptura_e
    }

    list_a.clear()
    list_b.clear()
    list_c.clear()
    list_d.clear()
    list_e.clear()


    lista_dados_estoque = [curva_a, curva_b, curva_c, curva_d, curva_e]

    return lista_dados_estoque


def db_dados_estoque(id_empresa, produtos):

    itens = DadosEstoque.objects.all().filter(
        empresa__id__exact=id_empresa
    )
    empresa = Empresa.objects.get(id=id_empresa)
    if itens:
        itens.delete()


    for i in produtos:

        b = DadosEstoque.objects.create(
            curva=i['curva'],
            skus=i['skus'],
            normal=i['normal'],
            parcial=i['parcial'],
            excesso=i['excesso'],
            ruptura=i['ruptura'],
            empresa=empresa
        )
        b.save()