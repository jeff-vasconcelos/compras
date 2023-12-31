from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render
from core.views.alerta.processa_produtos import *
from core.views.alerta.verificador import *
from core.models.empresas_models import *
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from core.models.parametros_models import Email
from core.models.usuarios_models import User
from django.utils import timezone

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# ALERTA EXCESSO
@login_required
def alerta_all_excesso(request, template_name='aplicacao/paginas/alertas/excesso.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = "EXCESSO"
    produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque=estado)
    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


def alerta_excesso_filial(request, filial, template_name='aplicacao/paginas/alertas/excesso.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = "EXCESSO"
    if filial == 0:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque=estado)

    else:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, cod_filial=filial, estado_estoque=estado)

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


def alerta_excesso_curva(request, curva, template_name='aplicacao/paginas/alertas/excesso.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = "EXCESSO"
    if curva == 'todos':
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque=estado)

    else:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, curva=curva, estado_estoque=estado)

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


# ALERTA RUPTURA
@login_required
def alerta_all_ruptura(request, template_name='aplicacao/paginas/alertas/ruptura.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = ["RUPTURA", "PARCIAL"]
    produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque__in=estado)
    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


def alerta_ruptura_filial(request, filial, template_name='aplicacao/paginas/alertas/ruptura.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = ["RUPTURA", "PARCIAL"]
    if filial == 0:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque=estado)

    else:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, cod_filial=filial, estado_estoque=estado)

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


def alerta_ruptura_curva(request, curva, template_name='aplicacao/paginas/alertas/ruptura.html'):
    id_empresa = request.user.usuario.empresa_id
    estado = ["RUPTURA", "PARCIAL"]
    if curva == 'todos':
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, estado_estoque=estado)

    else:
        produtos = Alerta.objects.filter(empresa__id__exact=id_empresa, curva=curva, estado_estoque=estado)

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    contexto = {
        'produtos': produtos,
        'filiais': filiais,
        'p_ativo': p_ativo
    }

    return render(request, template_name, contexto)


def alerta_db(id_empresa, produtos):
    itens = Alerta.objects.all().filter(
        empresa__id__exact=id_empresa
    )
    empresa = Empresa.objects.get(id=id_empresa)
    if itens:
        itens.delete()

    contador_alerta = 0

    for i in produtos:
        if i["qt_excesso"] > 0 or i["condicao_estoque"] != "NORMAL":
            valor = round(i['valor_sugestao'], 0)
            valor_excesso = i['vl_excesso']

            try:
                produto = Produto.objects.get(empresa_id=id_empresa,
                                              cod_produto=i['cod_produto'],
                                              cod_fornecedor=i['cod_fornecedor'])
            except Produto.DoesNotExist:
                produto = None

            if produto:

                b = Alerta.objects.create(
                    cod_filial=i['filial'],
                    cod_produto=i['cod_produto'],
                    desc_produto=i['desc_produto'],
                    saldo=round(i['saldo'], 0),
                    estado_estoque=i['condicao_estoque'],
                    valor=valor,
                    sugestao=round(i['sugestao_unidade'], 0),
                    estoque=round(i['estoque'], 0),
                    qt_excesso=round(i['qt_excesso'], 0),
                    vl_excesso=valor_excesso.replace("'", ""),
                    curva=i['curva'],
                    fornecedor=i['fornecedor'],
                    cod_fornecedor=i['cod_fornecedor'],
                    empresa=empresa,
                    dde=i['dde'],
                    # campo_dois=i['media_ajustada'],
                    media=i['media'],
                    principio_ativo=i['principio_ativo'],
                    data_entrada=i['dt_ult_entrada'],
                    id_produto=produto.id,
                    preco_venda=i['vl_ult_entrada']
                )
                b.save()

                contador_alerta = contador_alerta + 1

    data_hora = datetime.datetime.now(tz=timezone.utc)
    empresa.atualizacao_alerta = data_hora
    empresa.quantidade_alerta = contador_alerta
    empresa.save()


def mm(valor):
    return valor / 0.352777


def send_email_alerta(request, id_empresa):
    pdf = pdf_generate(request)
    hoje = timezone.now().strftime('%d-%m-%Y')

    lista_email = []
    lista_email_cc = []

    emails_cad = Email.objects.filter(empresa__id=id_empresa)
    usuarios = User.objects.filter(usuario__empresa__id=id_empresa)

    for i in usuarios:
        email_user = i.email

        lista_email.append(email_user)

    if emails_cad:
        for a in emails_cad:
            email = a.email
            lista_email_cc.append(email)

    msg = EmailMessage(
        'Alerta de Ruptura',
        '*Este é um e-mail automático, por favor, não responda.',
        to=lista_email,
        cc=lista_email_cc
    )

    msg.attach(f'alerta-insight-{hoje}', pdf, 'application/pdf')
    msg.content_subtype = 'html'
    msg.send()


def pdf_generate(request):
    itens = Alerta.objects.all().filter(
        empresa__id__exact=1
    ).order_by('estado_estoque')

    hoje = timezone.now().strftime('%d/%m/%Y')
    buffer = BytesIO()

    logo = ImageReader('templates/static/aplicacao/img/logo1.png')
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Helvetica', 12)
    p.drawImage(logo, mm(83), mm(270), height=40, width=130)
    p.drawString(mm(70), mm(255), f'ALERTA INSIGHT {hoje}', charSpace=2)

    p.setFont('Times-Roman', 8)
    p.drawString(mm(6), mm(245), "FILIAL")
    p.drawString(mm(20), mm(245), "PRODUTO")
    p.drawString(mm(10), mm(245), "PREV. ESTOQUE")
    p.drawString(mm(128), mm(245), "ESTOQUE")
    p.drawString(mm(150), mm(245), "QT. SUGERIDA")
    p.drawString(mm(175), mm(245), "VALOR PED. SUG.")

    p.line(mm(6), mm(243), mm(205), mm(243))

    contador_y = 240
    for prod in itens:
        if prod.qt_excesso == 0:
            contador_y = contador_y - 5
            p.drawString(mm(8), mm(contador_y), f'{prod.cod_filial}')
            p.drawString(mm(21), mm(contador_y), f'{prod.cod_produto} - {prod.desc_produto}')
            p.drawString(mm(11), mm(contador_y), f'{prod.estado_estoque}')
            p.drawString(mm(129), mm(contador_y), f'{prod.estoque}')
            p.drawString(mm(151), mm(contador_y), f'{prod.sugestao}')
            p.drawString(mm(176), mm(contador_y), f'{prod.valor}')

        else:
            contador_y = contador_y - 5
            p.drawString(mm(8), mm(contador_y), f'{prod.cod_filial}')
            p.drawString(mm(21), mm(contador_y), f'{prod.cod_produto} - {prod.desc_produto}')
            p.drawString(mm(11), mm(contador_y), f'{prod.estado_estoque}')
            p.drawString(mm(129), mm(contador_y), f'{prod.estoque}')
            p.drawString(mm(151), mm(contador_y), f'{prod.qt_excesso}')
            p.drawString(mm(176), mm(contador_y), f'{prod.vl_excesso}')

        if contador_y <= 1:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
