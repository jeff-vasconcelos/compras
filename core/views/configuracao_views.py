from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from core.models.parametros_models import Parametro
from api.models.fornecedor import Fornecedor
from django.contrib.auth.decorators import login_required
from core.forms.fornecedor_forms import FornecedorForm
from core.forms.parametros_form import ParametroForm
from core.forms.emails_forms import EmailForm
from core.models.parametros_models import Email


@login_required
def configuracao_painel(request, template_name='aplicacao/paginas/configuracao/configuracao.html'):
    empresa = request.user.usuario.empresa
    parametros = Parametro.objects.get(empresa__id=empresa.pk)

    contexto = {
        'parametro': parametros
    }
    return render(request, template_name, contexto)


@login_required
def email_painel(request, template_name='aplicacao/paginas/configuracao/emails.html'):
    empresa = request.user.usuario.empresa
    emails = Email.objects.filter(empresa__id=empresa.pk)

    contexto = {
        'emails': emails
    }
    return render(request, template_name, contexto)

@login_required
def fornecedores_painel(request, template_name='aplicacao/paginas/configuracao/fornecedores.html'):
    empresa = request.user.usuario.empresa
    fornecedores = Fornecedor.objects.filter(empresa__id=empresa.pk)

    contexto = {
        'fornecedores': fornecedores
    }
    return render(request, template_name, contexto)


@login_required
def editar_fornecedor_conf(request, pk, template_name='aplicacao/paginas/configuracao/fornec_edit.html'):
    if request.user.usuario.tipo == "Administrador":
        fornecedor = Fornecedor.objects.get(pk=pk)
        if request.method == 'POST':
            form = FornecedorForm(request.POST, instance=fornecedor)
            if form.is_valid():
                fornecedor = form.save(commit=False)
                fornecedor.save()
                messages.success(request, "Fornecedor atualizado com sucesso!")
                return redirect('fornecedores_painel')
            else:
                messages.error(request, "Ops, não foi possivel atualizar")
        else:
            form = FornecedorForm(instance=fornecedor)
        return render(request, template_name, {'form': form, 'fornecedor': fornecedor})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')



@login_required
def editar_parametro_conf(request, pk, template_name='aplicacao/paginas/configuracao/param_edit.html'):
    if request.user.usuario.tipo == "Administrador":
        parametro = Parametro.objects.get(pk=pk)
        if request.method == 'POST':
            form = ParametroForm(request.POST, instance=parametro)
            if form.is_valid():
                parametro = form.save(commit=False)
                parametro.save()
                messages.success(request, "Parametros atualizados com sucesso!")
                return redirect('configuracao_painel')
            else:
                messages.error(request, "Ops, não foi possivel atualizar")
        else:
            form = ParametroForm(instance=parametro)
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')


def adicionar_email_conf(request, template_name='aplicacao/paginas/configuracao/email_form.html'):
    if request.user.usuario.tipo == "Administrador":
        empresa = request.user.usuario.empresa
        try:
            if request.method == "POST":
                form = EmailForm(request.POST or None)
                if form.is_valid():

                    email = form.save(commit=False)
                    email.empresa = empresa
                    email.save()
                    messages.success(request, "E-mail cadastrado com sucesso!")
                    return redirect('email_painel')
                else:
                    messages.error(request, "Ops, não foi possivel cadastrar e-mail")
            else:
                form = EmailForm()
            return render(request, template_name, {'form': form})
        except Exception:
            messages.error(request, "Erro ao cadastrar e-mail, por favor verifique os campos informados!")
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')



def ver_emails_conf(request, template_name='aplicacao/paginas/configuracao/email_list.html'):
    if request.user.usuario.tipo == "Administrador":
        empresa = request.user.usuario.empresa
        emails = Email.objects.filter(empresa__id=empresa.pk)
        contexto = {
            'emails': emails
        }

        return render(request, template_name, contexto)


def remover_email_conf(request, pk):
    if request.user.usuario.tipo == "Administrador":
        email = Email.objects.get(pk=pk)
        email.delete()
        messages.error(request, "E-mail removido com sucesso!")
        return redirect('email_painel')
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')


def editar_email_conf(request, pk, template_name='aplicacao/paginas/configuracao/email_form.html'):
    if request.user.usuario.tipo == "Administrador":
        email = Email.objects.get(pk=pk)
        if request.method == 'POST':
            form = EmailForm(request.POST, instance=email)
            if form.is_valid():
                empresa = form.save(commit=False)
                empresa.save()
                messages.success(request, "E-mail atualizado com sucesso!")
                return redirect('email_painel')
            else:
                messages.error(request, "Ops, não foi possivel editar o e-mail")
        else:
            form = EmailForm(instance=email)
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')
