from django.contrib.auth.decorators import login_required
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
from django.utils import timezone
from core.trata_dados.home_abc import *
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def alertas(id_empresa):
    global alertas_produtos, infor_filiais, condicao

    lista_alertas = []
    parametros = Parametro.objects.get(empresa_id=id_empresa)

    fornecedores = get_fornecedores(id_empresa)

    for fornecedor in fornecedores:
        leadtime = fornecedor.leadtime
        t_reposicao = fornecedor.ciclo_reposicao


        produtos = get_produtos(id_empresa, fornecedor.id)

        for produto in produtos:
            verif_produto = verifica_produto(produto.cod_produto, id_empresa, parametros.periodo)

            if verif_produto == True:
                infor_filiais = processa_produtos_filiais(
                    produto.cod_produto,
                    fornecedor.cod_fornecedor,
                    id_empresa,
                    leadtime,
                    t_reposicao,
                    parametros.periodo
                )

                infor_filiais['cod_produto'] = produto.cod_produto
                infor_filiais['desc_produto'] = produto.desc_produto
                infor_filiais['fornecedor'] = fornecedor.desc_fornecedor
                infor_filiais['cod_fornecedor'] = fornecedor.cod_fornecedor


                for index, row in infor_filiais.iterrows():
                    alertas_produtos = {
                        'filial': row.filial,
                        'cod_produto': row.cod_produto,
                        'desc_produto': row.desc_produto,
                        'saldo': row.saldo,
                        'sugestao_unidade': row.sugestao,
                        'valor_sugestao': row.valor_sugestao,
                        'condicao_estoque': row.condicao_estoque,
                        'estoque': row.estoque,
                        'qt_excesso': row.qt_excesso,
                        'vl_excesso': row.vl_excesso,
                        'curva': row.curva,
                        'custo': row.custo,
                        'fornecedor': row.fornecedor,
                        'cod_fornecedor': row.cod_fornecedor,
                    }

                    lista_alertas.append(alertas_produtos)
    return lista_alertas


@login_required
def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    id_empresa = request.user.usuario.empresa_id
    produtos = Alerta.objects.filter(empresa__id__exact=id_empresa)

    return render(request, template_name, {'produtos': produtos})


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
            valor_sug = locale.currency(valor, grouping=True)

            b = Alerta.objects.create(
                cod_filial=i['filial'],
                cod_produto=i['cod_produto'],
                desc_produto=i['desc_produto'],
                saldo=round(i['saldo'], 0),
                estado_estoque=i['condicao_estoque'],
                valor=valor_sug,
                sugestao=round(i['sugestao_unidade'], 0),
                estoque=round(i['estoque'], 0),
                qt_excesso=round(i['qt_excesso'], 0),
                vl_excesso=valor_excesso.replace("'", ""),
                curva=i['curva'],
                fornecedor=i['fornecedor'],
                cod_fornecedor=i['cod_fornecedor'],
                empresa=empresa
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
    p.drawString(mm(100), mm(245), "PREV. ESTOQUE")
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
            p.drawString(mm(101), mm(contador_y), f'{prod.estado_estoque}')
            p.drawString(mm(129), mm(contador_y), f'{prod.estoque}')
            p.drawString(mm(151), mm(contador_y), f'{prod.sugestao}')
            p.drawString(mm(176), mm(contador_y), f'{prod.valor}')

        else:
            contador_y = contador_y - 5
            p.drawString(mm(8), mm(contador_y), f'{prod.cod_filial}')
            p.drawString(mm(21), mm(contador_y), f'{prod.cod_produto} - {prod.desc_produto}')
            p.drawString(mm(101), mm(contador_y), f'{prod.estado_estoque}')
            p.drawString(mm(129), mm(contador_y), f'{prod.estoque}')
            p.drawString(mm(151), mm(contador_y), f'{prod.qt_excesso}')
            p.drawString(mm(176), mm(contador_y), f'{prod.vl_excesso}')

        if contador_y <= 10:
            p.showPage()
            p.setFont('Times-Roman', 8)
            contador_y = 285


    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# ROTINA DE EXECUÇÃO DE ALERTA
def rotina_alerta(request, id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    print(f"PROCESSANDO DADOS DE {empresa.nome_fantasia}")

    produtos = alertas(id_empresa)

    grafico_um = processa_grafico_um(produtos)
    dados_estoque = dados_estoque_home(produtos)

    alerta_db(id_empresa, produtos)

    db_grafico_um(id_empresa, grafico_um)
    db_dados_estoque(id_empresa, dados_estoque)


def rotina_email(request, id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)

    # SE HABILITADA A OPÇÃO DE ENVIO DE EMAIL - CADASTRO DA EMPRESA
    try:
        if empresa.envia_email:
            print(f"ENVIANDO EMAIL(S) DE {empresa.nome_fantasia}")
            send_email_alerta(request, id_empresa)
    except:
        print("NÃO FOI POSSIVEL ENVIAR O(S) EMAIL(S)")


#TODO FUNÇÃO DE TESTE - REMOVER
#TESTE
def teste(request, template_name='testando_alerta.html'):
    empresa = Empresa.objects.get(id=1)
    produtos = alertas(1)

    grafico_um = processa_grafico_um(produtos)
    dados_estoque = dados_estoque_home(produtos)

    alerta_db(1, produtos)

    db_grafico_um(1, grafico_um)
    db_dados_estoque(1, dados_estoque)

    # SE HABILITADA A OPÇÃO DE ENVIO DE EMAIL - CADASTRO DA EMPRESA
    if empresa.envia_email:
        send_email_alerta(request, 1)

    return render(request, template_name)
