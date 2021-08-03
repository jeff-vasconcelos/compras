import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
from core.models.empresas_models import Empresa
from core.models.parametros_models import GraficoCurva, DadosEstoque, GraficoRuptura


def processa_grafico_um(produtos):
    global status
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


    total_normal = sum(lista_normal)
    total_excesso = sum(lista_excesso)
    total_parcial = sum(lista_parcial)
    total_ruptura = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()


    curva_a = {
        'curva': 'A',
        'total_normal':total_normal,
        'total_excesso':total_excesso,
        'total_parcial':total_parcial,
        'total_ruptura':total_ruptura
    }

    # CURVA B
    for b in curva:
        if b['curva'] == 'B':
            lista_normal.append(b['valor_normal'])
            lista_excesso.append(b['valor_excesso'])
            lista_parcial.append(b['valor_parcial'])
            lista_ruptura.append(b['valor_ruptura'])

        total_normal = sum(lista_normal)
        total_excesso = sum(lista_excesso)
        total_parcial = sum(lista_parcial)
        total_ruptura = sum(lista_ruptura)

        lista_normal.clear()
        lista_excesso.clear()
        lista_parcial.clear()
        lista_ruptura.clear()

    curva_b = {
        'curva': 'B',
        'total_normal': total_normal,
        'total_excesso': total_excesso,
        'total_parcial': total_parcial,
        'total_ruptura': total_ruptura
    }

    # CURVA C
    for c in curva:
        if c['curva'] == 'C':
            lista_normal.append(c['valor_normal'])
            lista_excesso.append(c['valor_excesso'])
            lista_parcial.append(c['valor_parcial'])
            lista_ruptura.append(c['valor_ruptura'])

    total_normal = sum(lista_normal)
    total_excesso = sum(lista_excesso)
    total_parcial = sum(lista_parcial)
    total_ruptura = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_c = {
        'curva': 'C',
        'total_normal': total_normal,
        'total_excesso': total_excesso,
        'total_parcial': total_parcial,
        'total_ruptura': total_ruptura
    }

    # CURVA D
    for d in curva:
        if d['curva'] == 'D':
            lista_normal.append(d['valor_normal'])
            lista_excesso.append(d['valor_excesso'])
            lista_parcial.append(d['valor_parcial'])
            lista_ruptura.append(d['valor_ruptura'])

    total_normal = sum(lista_normal)
    total_excesso = sum(lista_excesso)
    total_parcial = sum(lista_parcial)
    total_ruptura = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_d = {
        'curva': 'D',
        'total_normal': total_normal,
        'total_excesso': total_excesso,
        'total_parcial': total_parcial,
        'total_ruptura': total_ruptura
    }

    # CURVA E
    for e in curva:
        if e['curva'] == 'E':
            lista_normal.append(e['valor_normal'])
            lista_excesso.append(e['valor_excesso'])
            lista_parcial.append(e['valor_parcial'])
            lista_ruptura.append(e['valor_ruptura'])

    total_normal = sum(lista_normal)
    total_excesso = sum(lista_excesso)
    total_parcial = sum(lista_parcial)
    total_ruptura = sum(lista_ruptura)

    lista_normal.clear()
    lista_excesso.clear()
    lista_parcial.clear()
    lista_ruptura.clear()

    curva_e = {
        'curva': 'E',
        'total_normal': total_normal,
        'total_excesso': total_excesso,
        'total_parcial': total_parcial,
        'total_ruptura': total_ruptura
    }

    lista_status = [curva_a, curva_b, curva_c, curva_d, curva_e]

    return lista_status


def db_grafico_um(id_empresa, produtos):

    itens = GraficoCurva.objects.all().filter(empresa__id__exact=id_empresa)
    itens_rupt = GraficoRuptura.objects.all().filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if itens:
        itens.delete()

    if itens_rupt:
        itens_rupt.delete()


    for i in produtos:
        normal = i['total_normal']
        excesso = i['total_excesso']
        parcial = i['total_parcial']
        ruptura = i['total_ruptura']

        total = normal + excesso + parcial

        normal = locale.currency(normal, grouping=True)
        excesso = locale.currency(excesso, grouping=True)
        parcial = locale.currency(parcial, grouping=True)
        total = locale.currency(total, grouping=True)

        b = GraficoCurva.objects.create(
            curva=i['curva'],
            normal=normal,
            parcial=parcial,
            excesso=excesso,
            total=total,
            empresa=empresa
        )

        r = GraficoRuptura.objects.create(
            curva=i['curva'],
            total=ruptura,
            empresa=empresa
        )

        b.save()
        r.save()


def dados_estoque_home(produtos):

    sku = 0
    cont_normal = 0
    cont_excesso = 0
    cont_parcial = 0
    cont_ruptura = 0

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
    for a in list_a:
        sku = sku + 1

        if a['condicao_estoque'] == "NORMAL":
            cont_normal = cont_normal + 1

        elif a['condicao_estoque'] == "EXCESSO":
            cont_excesso = cont_excesso + 1

        elif a['condicao_estoque'] == "PARCIAL":
            cont_parcial = cont_parcial + 1

        elif a['condicao_estoque'] == "RUPTURA":
            cont_ruptura = cont_ruptura + 1

    curva_a = {
        'curva': 'A',
        'skus': sku,
        'normal': cont_normal,
        'excesso': cont_excesso,
        'parcial': cont_parcial,
        'ruptura': cont_ruptura
    }

    #CURVA B
    for b in list_b:
        sku = sku + 1

        if b['condicao_estoque'] == "NORMAL":
            cont_normal = cont_normal + 1

        elif b['condicao_estoque'] == "EXCESSO":
            cont_excesso = cont_excesso + 1

        elif b['condicao_estoque'] == "PARCIAL":
            cont_parcial = cont_parcial + 1

        elif b['condicao_estoque'] == "RUPTURA":
            cont_ruptura = cont_ruptura + 1

    curva_b = {
        'curva': 'B',
        'skus': sku,
        'normal': cont_normal,
        'excesso': cont_excesso,
        'parcial': cont_parcial,
        'ruptura': cont_ruptura
    }

    #CURVA C
    for c in list_c:
        sku = sku + 1

        if c['condicao_estoque'] == "NORMAL":
            cont_normal = cont_normal + 1

        elif c['condicao_estoque'] == "EXCESSO":
            cont_excesso = cont_excesso + 1

        elif c['condicao_estoque'] == "PARCIAL":
            cont_parcial = cont_parcial + 1

        elif c['condicao_estoque'] == "RUPTURA":
            cont_ruptura = cont_ruptura + 1

    curva_c = {
        'curva': 'C',
        'skus': sku,
        'normal': cont_normal,
        'excesso': cont_excesso,
        'parcial': cont_parcial,
        'ruptura': cont_ruptura
    }

    for d in list_d:
        sku = sku + 1

        if d['condicao_estoque'] == "NORMAL":
            cont_normal = cont_normal + 1

        elif d['condicao_estoque'] == "EXCESSO":
            cont_excesso = cont_excesso + 1

        elif d['condicao_estoque'] == "PARCIAL":
            cont_parcial = cont_parcial + 1

        elif d['condicao_estoque'] == "RUPTURA":
            cont_ruptura = cont_ruptura + 1

    curva_d = {
        'curva': 'D',
        'skus': sku,
        'normal': cont_normal,
        'excesso': cont_excesso,
        'parcial': cont_parcial,
        'ruptura': cont_ruptura
    }

    for e in list_e:
        sku = sku + 1

        if e['condicao_estoque'] == "NORMAL":
            cont_normal = cont_normal + 1

        elif e['condicao_estoque'] == "EXCESSO":
            cont_excesso = cont_excesso + 1

        elif e['condicao_estoque'] == "PARCIAL":
            cont_parcial = cont_parcial + 1

        elif e['condicao_estoque'] == "RUPTURA":
            cont_ruptura = cont_ruptura + 1

    curva_e = {
        'curva': 'E',
        'skus': sku,
        'normal': cont_normal,
        'excesso': cont_excesso,
        'parcial': cont_parcial,
        'ruptura': cont_ruptura
    }


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