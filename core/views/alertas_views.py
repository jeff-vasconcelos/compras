from django.core.mail import EmailMessage
from django.utils import timezone
from core.alertas.processa_produtos_alertas import *
from core.alertas.verificador import *
from core.models.empresas_models import *
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from core.models.parametros_models import Email
from core.models.usuarios_models import User
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def alertas():
    global alertas_produtos, infor_produtos_filiais, condicao
    id_empresa = 1 #TODO Automatizar empresa
    lista_alertas = []
    parametros = Parametro.objects.get(empresa_id=id_empresa)

    fornecedores = get_fornecedores(id_empresa)

    for fornecedor in fornecedores:
        leadtime = fornecedor.leadtime
        t_reposicao = fornecedor.ciclo_reposicao
        produtos = get_produtos(id_empresa, fornecedor.id)

        for produto in produtos:
            print(produto.desc_produto)
            verif_produto = verifica_produto(produto.cod_produto, id_empresa, parametros.periodo)

            if verif_produto == True:
                infor_produtos_filiais = processa_produtos_filiais(
                    produto.cod_produto,
                    fornecedor.cod_fornecedor,
                    id_empresa,
                    leadtime,
                    t_reposicao,
                    parametros.periodo
                )

                infor_produtos_filiais['cod_produto'] = produto.cod_produto
                infor_produtos_filiais['desc_produto'] = produto.desc_produto
                infor_produtos_filiais['fornecedor'] = fornecedor.desc_fornecedor
                infor_produtos_filiais['cod_fornecedor'] = fornecedor.cod_fornecedor

                condicao = ['FALSE' if x == 'NORMAL' else 'TRUE' for x in infor_produtos_filiais['condicao_estoque']]
                excesso_estoque = ['FALSE' if x > 0  else 'TRUE' for x in infor_produtos_filiais['sugestao_unidade']]

                if "TRUE" in condicao or "TRUE" in excesso_estoque:
                    alertas_produtos = infor_produtos_filiais.to_dict('records')

                    lista_alertas.append(alertas_produtos)

    return lista_alertas


def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    id_empresa = request.user.usuario.empresa_id
    produtos = Alerta.objects.filter(empresa__id__exact=id_empresa)


    # send_email_alerta(request)

    return render(request, template_name, {'produtos': produtos})


def executar_alerta(id_empresa, produtos):

    itens = Alerta.objects.all().filter(
        empresa__id__exact=id_empresa
    )

    empresa = Empresa.objects.get(id=id_empresa)

    if itens:
        itens.delete()

    for i in produtos:
        produto = i
        for a in produto:

            if a['excesso_estoque'] == "TRUE":
                status = "EXCESSO"
            else:
                status = a['condicao_estoque']
            valor = round(a['valor_sugestao'], 0)
            valor_sug = locale.currency(valor, grouping=True)

            b = Alerta.objects.create(
                cod_filial=a['filial'],
                cod_produto=a['cod_produto'],
                desc_produto=a['desc_produto'],
                saldo=round(a['saldo'], 0),
                estado_estoque=status,
                valor=valor_sug,
                sugestao=round(a['sugestao_unidade'], 0),
                estoque=round(a['estoque'], 0),
                curva=a['curva'],
                fornecedor=a['fornecedor'],
                cod_fornecedor=a['cod_fornecedor'],
                empresa=empresa
                )
            b.save()


def teste(request, template_name='testando_alerta.html'):
    produtos = alertas()
    executar_alerta(1, produtos)
    send_email_alerta(request)
    return render(request, template_name)


def mm(valor):
    return valor / 0.352777


def send_email_alerta(request):
    pdf = pdf_generate(request)
    hoje = timezone.now().strftime('%d-%m-%Y')

    lista_email = []
    #TODO Altomatizar id empresa
    emails_cad = Email.objects.filter(empresa__id=1)
    usuarios = User.objects.filter(usuario__empresa__id=1)

    for i in usuarios:
        email = i.email

        lista_email.append(email)

    if emails_cad:
        for a in emails_cad:
            email = a.email
            lista_email.append(email)


    # lista_email_cc = ['wellesoncolares@gmail.com']

    msg = EmailMessage(
        'Alerta de Ruptura',
        '*Este é um e-mail automático, por favor, não responda.',
        to=lista_email,
        # cc=lista_email_cc
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
    p.drawString(mm(100), mm(245), "PREV. ESTOQUE")
    p.drawString(mm(128), mm(245), "ESTOQUE")
    p.drawString(mm(150), mm(245), "QT. SUGERIDA")
    p.drawString(mm(175), mm(245), "VALOR PED. SUG.")

    p.line(mm(6), mm(243), mm(205), mm(243))

    contador_y = 240
    for prod in itens:
        contador_y = contador_y - 5
        p.drawString(mm(8), mm(contador_y), f'{prod.cod_filial}')
        p.drawString(mm(21), mm(contador_y), f'{prod.cod_produto} - {prod.desc_produto}')
        p.drawString(mm(101), mm(contador_y), f'{prod.estado_estoque}')
        p.drawString(mm(129), mm(contador_y), f'{prod.estoque}')
        p.drawString(mm(151), mm(contador_y), f'{prod.sugestao}')
        p.drawString(mm(176), mm(contador_y), f'{prod.valor}')
        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285


    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf