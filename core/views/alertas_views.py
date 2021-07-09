from core.alertas.processa_produtos_alertas import *
from core.alertas.verificador import *
import numpy as np
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.models.empresas_models import *


def alertas():
    global alertas_produtos, infor_produtos_filiais, condicao
    id_empresa = 1 #TODO Automatizar empresa
    lista_alertas = []
    parametros = Parametro.objects.get(empresa_id=id_empresa)

    fornecedores = get_fornecedores(id_empresa)

    for fornecedor in fornecedores:
        print(fornecedor)
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

                if "TRUE" in condicao:
                    print("vai para o alerta")
                    alertas_produtos = infor_produtos_filiais.to_dict('records')
                    lista_alertas.append(alertas_produtos)

    return lista_alertas


def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    id_empresa = request.user.usuario.empresa_id
    produtos = Alerta.objects.filter(empresa__id__exact=id_empresa)

    return render(request, template_name, {'produtos': produtos})


def executar_alerta():
    produtos = alertas()
    id_empresa = 1  # TODO Automatizar empresa

    itens = Alerta.objects.all().filter(
        empresa__id__exact=id_empresa
    )
    if itens:
        itens.delete()

    for i in produtos:
        produto = i
        for a in produto:
            # lista_alerta.append(a)
            print(a['filial'])
            empresa = Empresa.objects.get(id=id_empresa)
            b = Alerta.objects.create(
                cod_filial=a['filial'],
                cod_produto=a['cod_produto'],
                desc_produto=a['desc_produto'],
                saldo=a['filial'],
                estado_estoque=a['condicao_estoque'],
                curva=a['curva'],
                fornecedor=a['fornecedor'],
                cod_fornecedor=a['cod_fornecedor'],
                empresa=empresa
                )
            b.save()


def email_alerta():

    produtos = alertas()
    lista_alerta = []
    for i in produtos:
        produto = i
        for a in produto:
            lista_alerta.append(a)


    to = "wellesoncolares@gmail.com"

    context = {
        'produtos': lista_alerta
    }

    html_content = render_to_string("email_template_alerta.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Alerta - Ruptura de Estoque",
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
